import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox
import pyperclip
import time
import re
import win32gui
import win32con
import win32api
import sys
import portalocker

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab, Image

from pynput import keyboard
import threading

from config_accessor.core import ConfigAccessor
from screen_operator.core import ScreenOperator
from checkVersion import check_and_update_files
from ConfigEditer import main as ConfigMain
from ListAllWindows import update_group_names

from pathlib import Path

VERSION = "20250407"

SRC_PATH = Path.absolute(Path(__file__)).parent # 获取临时目录路径对象
SOFT_PATH = Path.cwd()

import pystray

# By Chamiko
# Chamiko@Chamiko.com
# 版本：v2.5-0404

global tray_icon
check_update = check_and_update_files(VERSION)
config = ConfigAccessor()

WINDOW_CONFIG = {
    #1: {"type": "class", "value": "WeChatMainWndForPC", "name": "微信"},
    1: {"type": "title", "value": config.get_selection_value("yt_window"), "name": config.get_selection_value("yt_window")},
    2: {"type": "title", "value": config.get_selection_value("yz_window"), "name": config.get_selection_value("yz_window")},
    3: {"type": "title", "value": "钉钉", "name": "钉钉"},
    4: {"type": "title", "value": config.get_selection_value("jt_window"), "name": config.get_selection_value("jt_window")}
}

if (config.get_selection_value("color") == "默认"):
    MODERN_STYLE = {
        "bg_color": "#FFFFFF",        # Windows标准浅灰背景
        "text_color": "#000000",      # 系统文字深灰
        "accent_color": "#0078D4",    # Fluent蓝（Windows主色）
        "entry_bg": "#FFFFFF",       # 纯白输入框
        "font": ("微软雅黑", 10),     # 保持Windows字体规范
        "hover_effect": True,          # 标准悬停效果
        "hover_color": "#DDDDDD",      # 浅蓝悬停背景
        "window_shadow": "#DDDDDD"  # 半透明系统投影
    }
elif (config.get_selection_value("color") == "现代"):
    MODERN_STYLE = {
        "bg_color": "#2D2D2D",        # 深灰背景
        "text_color": "#E6E6E6",      # 浅灰文字
        "accent_color": "#4CAF50",    # 扁平绿
        "entry_bg": "#3A3A3A",        # 输入框背景
        "font": ("等线", 10),     # 现代字体
        "hover_effect": True,          # 启用悬停效果
        "hover_color": "#3A3A3A",
        "window_shadow": "#1A1A1A"
    }
elif (config.get_selection_value("color") == "粉色"):
    MODERN_STYLE = {
        "bg_color": "#ffd1ed",        # 浅樱花粉背景 (原深灰#2D2D2D)
        "text_color": "#6D4C67",      # 浪漫紫粉文字 (原浅灰#E6E6E6)
        "accent_color": "#FF6B8B",    # 樱花粉强调色 (原绿#4CAF50)
        "entry_bg": "#FFE5EF",        # 浅玫瑰粉输入框 (原灰#3A3A3A)
        "font": ("微软雅黑", 10),     # 维持原始字体设定
        "hover_effect": True,          # 保持悬停效果
        "hover_color": "#ff89aa",
        "window_shadow": "#cdb4dd"
    }
elif (config.get_selection_value("color") == "清新"):
    MODERN_STYLE = {
        "bg_color": "#F0F7E6",        # 柔白背景（带10%青绿调）
        "text_color": "#3A5F40",      # 竹青色文字
        "accent_color": "#6CBE47",    # 新芽绿强调色
        "entry_bg": "#D8EED3",        # 薄荷雾输入框
        "font": ("微软雅黑", 10),     # 保持字体一致
        "hover_effect": True,          # 维持悬停效果
        "hover_color": "#A5D795",      # 青苹果悬停色
        "window_shadow": "#cfe5c2"     # 苔藓投影
    }
elif (config.get_selection_value("color") == "荧光"):
    MODERN_STYLE = {
        "bg_color": "#0A0A1A",        # 极夜蓝黑背景
        "text_color": "#00FEFE",      # 电子荧光青
        "accent_color": "#BC13FE",    # 霓虹紫（经典赛博色）
        "entry_bg": "#2A0A34",        # 暗物质紫输入框
        "font": ("微软雅黑 Bold", 10),  # 增加粗体
        "hover_effect": True,          # 强化悬停效果
        "hover_color": "#FF1C9E",      # 故障粉悬停
        "window_shadow": "#4B0082"     # 深紫投影
    }
elif (config.get_selection_value("color") == "冰川"):
    MODERN_STYLE = {
        "bg_color": "#F5F9FC",        # 冰川雾蓝背景
        "text_color": "#2E526E",      # 深海靛蓝文字
        "accent_color": "#6A8EA8",    # 岩石灰蓝强调色
        "entry_bg": "#E0E9F0",        # 晨雾输入框
        "font": ("等线", 10, "italic"), # 增加斜体
        "hover_effect": True,
        "hover_color": "#C4D4E3",     # 褪色丹宁悬停
        "window_shadow": "#93A5B7",   # 旧报纸投影
    }
elif (config.get_selection_value("color") == "琥珀"):
    MODERN_STYLE = {
        "bg_color": "#1A120B",        # 碳化琥珀基底（深棕）
        "text_color": "#F0E6D1",      # 沙漏流沙色（带5%透明度）
        "accent_color": "#FF6B35",    # 熔岩裂纹橙（Pantone 2024年度色）
        "entry_bg": "#3E2723",        # 树脂层积纹理（含0.2%噪点）
        "font": ("微软雅黑", 11),     # 宋体粗版增强质感
        "hover_effect": True,          # 模拟树脂反光
        "hover_color": "#FF9F1C",      # 氧化铜绿渐变
        "window_shadow": "#2B1B17"    # 古木投影
    }
elif (config.get_selection_value("color") == "危机"):
    MODERN_STYLE = {
        "bg_color": "#1A0005",        # 极夜红（含5%蓝黑杂质）
        "text_color": "#FF0033",      # 病毒荧光红（CIE 1931 x=0.673 y=0.299）
        "accent_color": "#CC0200",    # 动脉喷溅红（Pantone 18-1663TPX）
        "entry_bg": "#33000D",        # 凝血沉淀层（含0.5%噪点纹理）
        "font": ("微软雅黑 Bold", 11, "italic"), # 倾斜字体制造不安感
        "hover_effect": True,          # 强化脉动效果
        "hover_color": "#8A0000",      # 腐化铁锈红（Delta E >12变化量）
        "window_shadow": "#4D000F",    # 血痂投影
    }
elif (config.get_selection_value("color") == "鸢尾"):
    MODERN_STYLE = {
        "bg_color": "#1A0A2B",        # 鸢尾夜幕（带3%青调）
        "text_color": "#E6D7FF",      # 月光紫（含10%透明度）
        "accent_color": "#8A2BE2",    # 拜占庭紫（RGB 138,43,226）
        "entry_bg": "#2E1A47",        # 天鹅绒衬里（0.5px丝绒纹理）
        "font": ("等线 Light", 11),     # 细体字增强优雅感
        "hover_effect": True,          # 花瓣展开动效
        "hover_color": "#BA55D3",      # 三色堇过渡色
        "window_shadow": "#4B0082",    # 紫水晶投影
    }
elif (config.get_selection_value("color") == "白粉"):
    MODERN_STYLE = {
        "bg_color": "#FFF4F4",        # 初雪玫瑰基底（含0.5%粉调）
        "text_color": "#6D1B1B",      # 勃艮第酒红（CMYK 30,100,70,40）
        "accent_color": "#FF206E",    # 霓虹蔷薇红（Pantone Vibrant Red）
        "entry_bg": "#FFE3E8",        # 玫瑰糖霜层（CSS径向渐变）
        "font": ("微软雅黑 Light", 10), # 强化文字存在感
        "hover_effect": True,          # 模拟花瓣颤动
        "hover_color": "#FF5C8A",      # 绽放过渡色
        "window_shadow": "#FFB6C1",  # 半透明薄纱投影
    }
IS_BEATUY = config.get_selection_value("beauty_command")

# 屏幕参数
screen_width, screen_height = pyautogui.size()
region = (0, 0, screen_width, 500)
THRESHOLD = 0.8
# 加载目标图片
try:
    target = cv2.imread(str(SRC_PATH / "img/dingkd.png"), cv2.IMREAD_GRAYSCALE)
    if target is None:
        raise FileNotFoundError
except Exception as e:
    raise SystemExit(f"错误：无法加载目标图片 - {str(e)}")
    
def check_image():
    screenshot = ImageGrab.grab(bbox=region)
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(screenshot_gray, target, cv2.TM_CCOEFF_NORMED)
    return np.any(res >= THRESHOLD)

def simulate_paste(auto_send_enabled, command):
    if command.startswith("7") or command.startswith("申"): 
        if not check_image():
            return
    time.sleep(0.2)
    # 模拟按下 Ctrl 键
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    # 模拟按下 V 键
    win32api.keybd_event(ord('V'), 0, 0, 0)
    # 释放 V 键
    win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
    # 释放 Ctrl 键
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    if "*" in command:
        return
    time.sleep(0.1)

    # 自动发送功能：添加回车键
    if auto_send_enabled:
        win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
        win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)

def find_window(config):
    def class_callback(hwnd, _):
        if (win32gui.IsWindowVisible(hwnd) and 
            win32gui.GetClassName(hwnd) == config["value"]):
            win_list.append(hwnd)
        return True

    def title_callback(hwnd, _):
        if (win32gui.IsWindowVisible(hwnd) and 
            config["value"] in win32gui.GetWindowText(hwnd)):
            win_list.append(hwnd)
        return True

    win_list = []
    if config["type"] == "class":
        win32gui.EnumWindows(class_callback, None)
    elif config["type"] == "title":
        win32gui.EnumWindows(title_callback, None)
    
    if win_list:
        return max(win_list, key=lambda h: win32gui.GetWindowRect(h)[2]-win32gui.GetWindowRect(h)[0])
    return 0

def activate_window(hwnd):
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.BringWindowToTop(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        return True
    except Exception as e:
        print(f"激活失败：{str(e)}")
        return False

def check_single_instance():
    """更可靠的单实例检测方法"""
    # 生成跨用户的全局锁文件路径
    lock_path = Path(r"C:\Program Files\LogData\command.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)  # 自动创建目录
    
    try:
        # 必须用'a+'模式打开，避免文件不存在时报错
        lock_file = open(lock_path, 'a+', encoding='utf-8')
        # 非阻塞锁（LOCK_NB是关键）
        portalocker.lock(lock_file, portalocker.LOCK_EX | portalocker.LOCK_NB)
        # 保留引用防止垃圾回收释放锁
        check_single_instance.lock_file = lock_file  # type: ignore
        print(f"成功获取文件锁：{lock_path}")
        return True
    except (portalocker.exceptions.LockException, PermissionError) as e:
        print(f"单实例检测失败，已有程序在运行：{e}")
        return False

class ExpressCommandGenerator:
    def __init__(self):
        # ​**​* 必须第一时间检查 ​**​*
        if not check_single_instance():
            # 增强提示
            import tkinter.messagebox as msgbox
            msgbox.showwarning("重复启动", "程序已在后台运行，请勿重复启动！")
            sys.exit(1)  # 非0退出码表示异常退出

        # 原有初始化代码
        # ...

class ExpressCommandGenerator:
    def __init__(self):
        # --- 加载动画
        # 创建启动画面
        self.splash_root = tk.Tk()
        self.splash_root.overrideredirect(True)
        self.splash_root.attributes("-topmost", True)
        self.splash_root.attributes("-alpha", 0.5)  # 半透明效果
        
        # 加载启动图片
        try:
            splash_image = Image.open(str(SRC_PATH / "img/loading.png"))
            self.splash_photo = ImageTk.PhotoImage(splash_image)
        except Exception as e:
            print(f"启动图加载失败: {str(e)}")
            self.splash_photo = None

        # 计算居中位置
        screen_width = self.splash_root.winfo_screenwidth()
        screen_height = self.splash_root.winfo_screenheight()
        if self.splash_photo:
            img_width = self.splash_photo.width()
            img_height = self.splash_photo.height()
        else:
            img_width = 400
            img_height = 300
            
        x = (screen_width - img_width) // 2
        y = (screen_height - img_height) // 3  # 靠上1/3位置

        # 创建主容器
        splash_frame = tk.Frame(self.splash_root, 
                              bg=MODERN_STYLE["bg_color"],
                              borderwidth=0)
        splash_frame.pack()
        
        # 添加图片（如果加载成功）
        if self.splash_photo:
            tk.Label(splash_frame, 
                    image=self.splash_photo, 
                    borderwidth=0).pack()
        else:
            # 备用加载提示
            tk.Label(splash_frame, 
                    text="程序初始化中...",
                    font=("微软雅黑", 14),
                    bg=MODERN_STYLE["bg_color"],
                    fg=MODERN_STYLE["text_color"]).pack(pady=20)
            
        
        # 设置窗口位置
        self.splash_root.geometry(f"{img_width}x{img_height}+{x}+{y}")
        self.splash_root.update()
        # ---


        if not check_single_instance():
            messagebox.showwarning("警告", "程序已在后台运行！")
            self.splash_root.destroy()
            sys.exit(0)

        if check_update == -1:
            messagebox.showwarning("警告", "您安装过最新版，请勿使用旧版！")
            self.splash_root.destroy()
            sys.exit(0)
        elif check_update == 1:
            messagebox.showwarning("提示", "检测到新版本，点击确认更新！")
            from CheckRestart import write_and_run_update_script
            self.splash_root.destroy()
            write_and_run_update_script()
            sys.exit(0)
        elif check_update == 2:
            messagebox.showwarning("提示", "连接服务器失败，请检查网络！")
            self.splash_root.destroy()
            sys.exit(0)
        elif isinstance(check_update, str):
            msg_path = Path(r"C:\Program Files\LogData\ExpressCommandMsg.txt")
            msg = None
            if not msg_path.exists():
                msg = check_update
            else:
                if check_update != msg_path.read_text(encoding='utf-8').strip():
                    msg = check_update

            if msg:
                msg_path.write_text(msg, encoding='utf-8')
                self.show_info(msg)
        self.current_action = None
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口

        # --- 关闭图片
        # 模拟初始化过程（实际应替换为真实初始化步骤）
        time.sleep(1)  # 模拟耗时操作
        # 关闭启动画面
        self.splash_root.destroy()
        # ---

        self.menu_window = None
        self.auto_send_enabled = False
        self.read_autosend_config()
        
        # 设置全局热键监听
        self.listener = None
        self.setup_hotkey_listener()
        # 是否监听
        self.listening = False
        
        # 保证程序不退出的特殊循环
        self.root.mainloop()

    def setup_hotkey_listener(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f4:
                    # 确保在主线程操作GUI
                    self.root.after(0, self.show_main_menu)
            except AttributeError:
                pass

        def start_listener():
            nonlocal on_press
            with keyboard.Listener(on_press=on_press) as listener:
                self.listener = listener
                listener.join()

        # 在独立线程中运行监听器
        threading.Thread(target=start_listener, daemon=True).start()
        threading.Thread(target=self.create_tray_icon, daemon=True).start()

    def read_autosend_config(self):
        try:
            self.auto_send_enabled = config.get_selection_value("auto_send")
        except Exception as e:
            self.show_error(f"配置文件错误：{str(e)}")
            self.auto_send_enabled = False

    def show_main_menu(self):
        self.listening = False
        if self.menu_window:
            self.menu_window.destroy()
        self.menu_window = tk.Toplevel(self.root)
        
        # 无边框设置
        self.menu_window.attributes('-topmost', True)
        self.menu_window.overrideredirect(True)  # 关键修改[2](@ref)
        self.menu_window.configure(bg=MODERN_STYLE["bg_color"])

        self.menu_window.grab_set()  # 捕获所有输入事件
        self.menu_window.update_idletasks()  # 先刷新
        self.menu_window.focus_force()      # 再设置焦点
        self.menu_window.focus_set()  # 确保窗口获得焦点
        self.menu_window.lift()
        
        # 新增按钮检测
        self.menu_window.bind('<Key>', self.on_key_press)
        self.menu_window.bind('<Map>', lambda e: self.menu_window.focus_force())
        self.menu_window.update_idletasks()
        
        # 窗口阴影模拟（使用tkinter原生组件）
        shadow_frame = tk.Frame(self.menu_window, bg=MODERN_STYLE["window_shadow"])
        shadow_frame.pack(padx=3, pady=3)
        
        # 拖拽区域（替换原有geometry设置）
        mouse_x = self.root.winfo_pointerx() + 10
        mouse_y = self.root.winfo_pointery() + 10
        self.menu_window.geometry(f"+{mouse_x}+{mouse_y}")
        title_bar = tk.Frame(shadow_frame, bg=MODERN_STYLE["bg_color"], cursor="hand2")
        title_bar.pack(fill="x")
        title_bar.bind("<Button-1>", self._start_drag)
        title_bar.bind("<B1-Motion>", self._on_drag)
        
        # 关闭按钮（新增）
        close_btn = tk.Button(title_bar, text="✕", command=self.on_menu_close, 
                             font=("微软雅黑", 8), fg=MODERN_STYLE["text_color"],
                             bg=MODERN_STYLE["bg_color"], relief="flat", borderwidth=0)
        close_btn.pack(side="right")
        
        options = [
            ("1.拦截", 1), ("2.召回", 2), ("3.取消拦截", 3),
            ("4.核实称重", 4), ("5.催件", 5), ("6.联系取件", 6),
            ("7.反馈未收到货", 7), ("8.修改地址", 8), ("9.修改联系方式", 9),
            ("10.修改设置", 10)
        ]
        
        for text, value in options:
            btn = tk.Button(shadow_frame, text=text, 
                           command=lambda v=value: self.handle_choice(v),
                           bg=MODERN_STYLE["bg_color"],
                           fg=MODERN_STYLE["text_color"],
                           activebackground=MODERN_STYLE["accent_color"],
                           font=MODERN_STYLE["font"],
                           relief="flat",
                           borderwidth=0,
                           padx=10)
            btn.pack(pady=3, fill="x")
            
            # 悬停效果[2](@ref)
            if MODERN_STYLE["hover_effect"]:
                btn.bind("<Enter>", lambda e: e.widget.config(bg=MODERN_STYLE["hover_color"]))
                btn.bind("<Leave>", lambda e: e.widget.config(bg=MODERN_STYLE["bg_color"]))
        self.menu_window.protocol("WM_DELETE_WINDOW", self.on_menu_close)

        self.menu_window.after(100, self._force_focus)  # 延迟确保窗口初始化完成
    
    def _force_focus(self):
        """强制聚焦的补充方法"""
        self.menu_window.focus_force()  # 强制聚焦
        self.menu_window.grab_set_global()  # 全局捕获输入
        self.menu_window.update_idletasks()  # 强制刷新窗口状态

    def on_menu_close(self):
        self.listening = False
        if self.menu_window:
            self.menu_window.destroy()
            self.menu_window = None
        # self.root.deiconify()
        # self.root.focus_force()

    def on_key_press(self, event):
        """处理键盘事件"""
        key_mapping = {
            # 主键盘数字键
            '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9, '0': 10,
            # 小键盘数字键
            'KP_1': 1, 'KP_2': 2, 'KP_3': 3, 'KP_4': 4,
            'KP_5': 5, 'KP_6': 6, 'KP_7': 7, 'KP_8': 8,
            'KP_9': 9, 'KP_0': 10
        }
        
        if event.keysym in key_mapping:
            choice = key_mapping[event.keysym]
            self.handle_choice(choice)
            return "break"  # 阻止事件继续传播
        
    def _start_drag(self, event):
        # 获取触发事件的标题栏，并找到对应的Toplevel窗口
        title_bar = event.widget
        shadow_frame = title_bar.master
        dialog = shadow_frame.master  # Toplevel窗口
        # 将拖拽起始坐标保存到对话框实例中
        dialog._drag_start_x = event.x
        dialog._drag_start_y = event.y

    def _on_drag(self, event):
        # 获取事件相关的窗口
        title_bar = event.widget
        shadow_frame = title_bar.master
        dialog = shadow_frame.master  # Toplevel窗口
        # 计算新坐标
        dx = event.x - dialog._drag_start_x
        dy = event.y - dialog._drag_start_y
        new_x = dialog.winfo_x() + dx
        new_y = dialog.winfo_y() + dy
        dialog.geometry(f"+{new_x}+{new_y}")

    def handle_choice(self, choice):
        self.menu_window.destroy()
        if choice == 10:
            update_group_names()
            ConfigMain(self.root)
            return
        self.current_action = choice
        if choice in (1, 2, 3, 4, 5, 6, 7):
            self.handle_normal_command()
        elif choice in (8, 9):
            self.handle_modify_command()
        # self.cleanup()

    def handle_normal_command(self):
        pyperclip.copy("")
        tracking_number = self.wait_for_clipboard("请复制快递单号")
        if not tracking_number:
            return
        
        try:
            if self.is_post(tracking_number):
                contact_info = self.wait_for_clipboard("请复制联系方式及地址")

                if not contact_info:
                    return
                action_text = self.get_action_text()
                action_text = "重量" if action_text == "核实称重" else action_text
                if IS_BEATUY:
                    command = f"{tracking_number}\n    {action_text}\n{contact_info}"
                else:
                    command = f"{tracking_number} {action_text} {contact_info}"
            elif self.is_jt(tracking_number):
                action_text = self.get_action_text()
                if action_text == "催件" or action_text == "召回":
                    contact_info = self.wait_for_clipboard("请复制联系方式及地址")
                    if not contact_info:
                        return
                    if IS_BEATUY:
                        command = f"{tracking_number}\n    {action_text}\n{contact_info}"
                    else:
                        command = f"{tracking_number} {action_text} {contact_info}"
                else:
                    command = f"{tracking_number} {self.get_action_text()}"
            else:
                command = f"{tracking_number} {self.get_action_text()}"
            
            pyperclip.copy(command)
            config = 0
            if tracking_number.startswith("YT") or tracking_number.startswith("圆通"):
                config = WINDOW_CONFIG[1]
            elif tracking_number.startswith("9") or tracking_number.startswith("邮政"):
                config = WINDOW_CONFIG[2]
            elif tracking_number.startswith("7") or tracking_number.startswith("申通"):
                config = WINDOW_CONFIG[3]
            elif tracking_number.startswith("JT") or tracking_number.startswith("极兔"):
                config = WINDOW_CONFIG[4]
            if config:
                hwnd = find_window(config)
                if hwnd:
                    activate_window(hwnd)
                    simulate_paste(self.auto_send_enabled, command)  # 修改调用方式
        except Exception as e:
            self.show_error(f"生成指令失败：{str(e)}")

    def handle_modify_command(self):
        pyperclip.copy("")
        try:
            tracking_number = self.wait_for_clipboard("请复制快递单号")
            if not tracking_number:
                return
            jt = self.is_jt(tracking_number)
            old_info = None
            if jt:
                if self.get_action_text() == "修改联系方式":
                    self.show_error("极兔请选择修改地址！")
                    return
            else:
                old_info = self.wait_for_clipboard("请复制联系方式及地址")
                if not old_info:
                    return
            new_content = self.get_new_content_input()
            if new_content:
                if jt:
                    if IS_BEATUY:
                        command = f"{tracking_number}\n    {self.get_action_text()}\n{new_content}"
                    else:
                        command = f"{tracking_number} {self.get_action_text()} {new_content}"
                else:
                    if IS_BEATUY:
                        command = f"{tracking_number}\n{old_info}\n    {self.get_action_text()}\n{new_content}"
                    else:
                        command = f"{tracking_number} {old_info} {self.get_action_text()} {new_content}"
                pyperclip.copy(command)
                config = 0
                if tracking_number.startswith("YT") or tracking_number.startswith("圆通"):
                    config = WINDOW_CONFIG[1]
                elif tracking_number.startswith("9") or tracking_number.startswith("邮政"):
                    config = WINDOW_CONFIG[2]
                elif tracking_number.startswith("7") or tracking_number.startswith("申通"):
                    config = WINDOW_CONFIG[3]
                elif tracking_number.startswith("JT") or tracking_number.startswith("极兔"):
                    config = WINDOW_CONFIG[4]
                if config:
                    hwnd = find_window(config)
                    if hwnd:
                        activate_window(hwnd)
                        simulate_paste(self.auto_send_enabled, command)  # 修改调用方式
        except Exception as e:
            self.show_error(f"处理修改请求失败: {str(e)}")

    def wait_for_clipboard(self, prompt):
        original = pyperclip.paste()
        # self.show_info(prompt)
        if prompt == "请复制联系方式及地址" and config.get_selection_value("auto_copy") == True:
            operator = ScreenOperator(confidence=0.85, move_duration=0.01)
            operator.execute_workflow(
                open_address_img=str(SRC_PATH / "img/OpenAddress.png"),
                copy_imgs=[str(SRC_PATH / "img/CopyAddress1.png"), str(SRC_PATH / "img/CopyAddress2.png"), str(SRC_PATH / "img/ClickCopy.png")],
                right_panel_width=400
            )
        start_time = time.time()
        self.listening = True
        while time.time() - start_time < 10:
            if self.listening == False:
                return
            current = pyperclip.paste()
            if current != original:
                return current.strip()
            time.sleep(0.1)
            self.root.update()
        return None

    def get_action_text(self):
        actions = {
            1: "拦截", 2: "召回", 3: "取消拦截",
            4: "核实称重", 5: "催件", 6: "联系收件人取件",
            7: "消费者反馈未收到货", 8: "修改地址", 9: "修改联系方式"
        }
        return actions[self.current_action]

    def is_post(self, tracking_number):
        return re.match(r'^(9|邮).+$', tracking_number)
        
    def is_jt(self, tracking_number):
        return re.match(r'^(J|极).+$', tracking_number)

    def create_custom_input_dialog(self):
        result = [None]  # 初始化结果变量
        dialog = tk.Toplevel(self.root)
        dialog.overrideredirect(True)
        dialog.configure(bg=MODERN_STYLE["bg_color"])
        dialog.attributes('-topmost', True)
        
        # 阴影效果
        shadow_frame = tk.Frame(dialog, bg=MODERN_STYLE["window_shadow"])
        shadow_frame.pack(padx=3, pady=3)
        
        # 可拖拽标题栏（扩大高度并填满顶部）
        title_bar = tk.Frame(shadow_frame, 
                            bg=MODERN_STYLE["bg_color"], 
                            cursor="hand2",
                            height=30)  # 增加高度
        title_bar.pack(fill="x", pady=(0, 10))  # 下方增加间距使标题栏与内容区分
        title_bar.bind("<Button-1>", self._start_drag)
        title_bar.bind("<B1-Motion>", self._on_drag)  # 修正此处绑定到_on_drag
        
        # 输入框区域（增加弹性布局）
        content_frame = tk.Frame(shadow_frame, bg=MODERN_STYLE["bg_color"])
        content_frame.pack(fill="both", expand=True)  # 关键修改：允许扩展
        
        # 窗口居中
        dialog.update_idletasks()  # 强制更新窗口尺寸
        dialog_width = 400
        dialog_height = 230
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        text_box = tk.Text(content_frame, 
                          wrap=tk.WORD,
                          height=6,  # 适当减少高度
                          bg=MODERN_STYLE["entry_bg"],
                          fg=MODERN_STYLE["text_color"],
                          insertbackground=MODERN_STYLE["text_color"],
                          relief="flat",
                          font=MODERN_STYLE["font"])
        text_box.pack(padx=10, pady=(0,10), fill="both", expand=True)  # 减少下方间距
        
        # 确认按钮
        def on_confirm():
            content = text_box.get("1.0", tk.END).strip()
            if not content:
                # self.show_error("输入内容不能为空")
                return
            result[0] = content
            dialog.destroy()
        
        confirm_btn = tk.Button(shadow_frame, 
                               text="确认", 
                               command=on_confirm,
                               bg=MODERN_STYLE["accent_color"],
                               fg=MODERN_STYLE["text_color"],
                               activebackground=MODERN_STYLE["accent_color"],
                               relief="flat",
                               borderwidth=0,
                               font=("微软雅黑", 12))
        confirm_btn.pack(pady=5)
        
        text_box.focus_set()
        dialog.grab_set()
        self.root.wait_window(dialog)
        return result[0]

    def get_new_content_input(self):
        return self.create_custom_input_dialog()

    def show_info(self, message):
        messagebox.showinfo("提示", message)

    def show_error(self, message):
        messagebox.showerror("错误", message)

    def cleanup(self):
        """确保完全退出程序"""
        global tray_icon
        tray_icon.stop()
        if self.root.winfo_exists():
            try:
                # 销毁所有窗口
                for window in self.root.winfo_children():
                    window.destroy()
                # 终止主循环
                self.root.quit()
                # 销毁根窗口
                self.root.destroy()
            except tk.TclError:
                pass
        # 强制退出进程
        sys.exit(0)

    
    def create_tray_icon(self):
        # 从图片文件中加载图标
        image = Image.open(str(SRC_PATH / "img/icon.ico"))
        # 创建系统托盘菜单
        menu = (
            # pystray.MenuItem("", lambda: open_app()),
            pystray.MenuItem("退出程序", lambda: self.cleanup()),
        )
        # 创建系统托盘图标
        global tray_icon
        tray_icon = pystray.Icon("ExpressCommand", image, "快递指令", menu)
        # 设置图标的提示文本
        tray_icon.tooltip = "快递指令"
        # 显示系统托盘图标
        tray_icon.run()
    



if __name__ == "__main__":
    ExpressCommandGenerator()