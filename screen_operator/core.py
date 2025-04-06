# core.py
import pyautogui
import cv2
import numpy as np
import time
import logging
from .exceptions import *

class ScreenOperator:
    def __init__(self, 
                 confidence=0.8, 
                 search_interval=0.2,
                 move_duration=0.3):
        """
        初始化屏幕操作器
        :param confidence: 模板匹配置信度阈值 (0~1)
        :param search_interval: 搜索间隔时间（秒）
        :param move_duration: 鼠标移动动画时长（秒）
        """
        self.confidence = confidence
        self.search_interval = search_interval
        self.move_duration = move_duration
        self.logger = logging.getLogger(__name__)
        
        # 验证依赖库是否正确安装
        try:
            pyautogui.size()
        except Exception as e:
            raise ImportError("pyautogui初始化失败，请确保GUI环境可用") from e

    def capture_region(self, region):
        """
        截取指定屏幕区域
        :param region: (left, top, width, height) 元组
        :return: OpenCV格式图像
        """
        adjusted_region = self._validate_region(region)
        screenshot = pyautogui.screenshot(region=adjusted_region)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    def find_template(self, template_path, region=None, image=None):
        """
        在屏幕或图像中查找模板
        :param template_path: 模板图片路径
        :param region: 屏幕区域 (left, top, width, height)
        :param image: 如果提供则使用该图像代替截屏
        :return: (中心点坐标, 匹配度) 或 None
        """
        template = self._load_template(template_path)
        
        try:
            screen_img = (image if image is not None 
                        else self.capture_region(region) if region 
                        else self.capture_region((0, 0, *pyautogui.size())))
        except ValueError as e:
            self.logger.warning(f"区域截取失败: {str(e)}")
            return None
        
        result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= self.confidence:
            h, w = template.shape[:2]
            center = (
                max_loc[0] + w // 2 + (region[0] if region else 0),
                max_loc[1] + h // 2 + (region[1] if region else 0)
            )
            return center, max_val
        return None

    def smart_click(self, template_path, region=None, timeout=2):
        """
        智能点击操作（带超时和重试）
        :return: 点击成功的中心坐标
        :raises: TemplateMatchTimeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if result := self.find_template(template_path, region):
                center, confidence = result
                self.logger.info(f"匹配成功 {template_path} 置信度 {confidence:.2f}")
                self._safe_move_click(center)
                return center
            
            self.logger.debug(f"未找到 {template_path}，等待重试...")
            time.sleep(self.search_interval)
        
        raise TemplateMatchTimeout(f"在 {timeout} 秒内未找到模板 {template_path}")

    def execute_workflow(self, open_address_img, copy_imgs, right_panel_width=0):
        """执行完整工作流程"""
        # 第一步：动态计算安全区域
        x, y = pyautogui.position()
        screen_width, screen_height = pyautogui.size()
        if right_panel_width == 0:
            right_panel_width = screen_width
        
        # 计算右侧可用宽度（至少保留10像素边界）
        right_space = screen_width - x - 10
        capture_width = min(500, right_space) if right_space > 0 else 0
        
        if capture_width < 50:  # 如果剩余空间太小
            self.logger.warning("鼠标太靠近右边界，无法执行操作")
            return False
        
        region = (x + 1, max(0, y - 25), capture_width, 50)
        
        try:
            self.smart_click(open_address_img, region, timeout=0.5)
        except (TemplateMatchTimeout, ValueError) as e:
            self.logger.error(f"打开地址操作失败: {str(e)}")
            return False
        
        # 等待新窗口
        time.sleep(0.3)
        
        # 第二步：右侧面板操作
        screen_width = pyautogui.size().width
        right_region = (
            screen_width - right_panel_width,
            0,
            right_panel_width,
            pyautogui.size().height
        )
        
        for img in copy_imgs:
            try:
                self.smart_click(img, right_region, timeout=3)
                time.sleep(0.1)
            except TemplateMatchTimeout as e:
                self.logger.warning(f"跳过未找到的 {img}")
                break
            time.sleep(0.1)

    # 以下为内部方法
    def _validate_region(self, region):
        """改进后的屏幕区域验证方法"""
        screen_width, screen_height = pyautogui.size()
        left, top, width, height = region
        
        # 调整宽度不超过屏幕边界
        if left + width > screen_width:
            width = screen_width - left
        # 调整高度不超过屏幕边界
        if top + height > screen_height:
            height = screen_height - top
        
        # 最终校验
        if (width <= 0 or height <= 0 or
            left >= screen_width or top >= screen_height or
            any(v < 0 for v in [left, top])):
            raise ValueError(f"调整后仍无效的区域: {region}")
        
        return (left, top, width, height)  # 返回调整后的区域

    def _load_template(self, template_path):
        """加载模板图片并校验"""
        template = cv2.imread(template_path)
        if template is None:
            self.logger.error(f"模板文件加载失败: {template_path}")
            raise TemplateNotFound(f"无法读取模板文件: {template_path}")
        return template

    def _safe_move_click(self, coordinates):
        """带异常处理的移动点击"""
        try:
            pyautogui.moveTo(
                coordinates[0], 
                coordinates[1], 
                duration=self.move_duration
            )
            time.sleep(0.05)
            pyautogui.click()
            time.sleep(0.01)
            pyautogui.click()
            self.logger.debug(f"已点击坐标 {coordinates}")
        except pyautogui.FailSafeException:
            self.logger.warning("触发了故障保护机制，终止操作")
            raise