import os
import json
import requests
from urllib.parse import quote

# 定义文件路径
log_data_dir = r"C:\Program Files\LogData"
autoversion_path = os.path.join(log_data_dir, "autoversion.txt")
autoconfig_path = os.path.join(log_data_dir, "autoconfig.txt")

# 定义目标内容
target_config = {
    "selectable": [
        {
            "text": "主题配色",
            "name": "color",
            "options": [
                "默认",
                "现代",
                "清新",
                "粉色",
                "白粉",
                "荧光",
                "冰川",
                "琥珀",
                "危机",
                "鸢尾"
            ]
        },
        {
            "text": "自动发送指令",
            "name": "auto_send",
            "options": [
                True,
                False
            ]
        },
        {
            "text": "自动复制地址（实验性功能）",
            "name": "auto_copy",
            "options": [
                True,
                False
            ]
        },
        {
            "text": "美化快递指令：自动换行",
            "name": "beauty_command",
            "options": [
                True,
                False
            ]
        },{
            "text": "群名：圆通",
            "name": "yt_window",
            "options": [
                "圆通速递-努创售后群"
            ]
        },{
            "text": "群名：邮政",
            "name": "yz_window",
            "options": [
                "努创邮政查件群"
            ]
        },{
            "text": "群名：极兔",
            "name": "jt_window",
            "options": [
                "丸仟极兔快递售后对接群"
            ]
        }
    ],
    "selection": [
        {
            "name": "color",
            "option": "默认"
        },
        {
            "name": "auto_send",
            "option": False
        },
        {
            "name": "auto_copy",
            "option": False
        },
        {
            "name": "beauty_command",
            "option": False
        },
        {
            "name": "yt_window",
            "option": "圆通速递-努创售后群"
        },
        {
            "name": "yz_window",
            "option": "努创邮政查件群"
        },
        {
            "name": "jt_window",
            "option": "丸仟极兔快递售后对接群"
        }
    ]
}

# 基础 URL（替换成你的 Vercel 部署域名）
BASE_URL = "https://version.chamiko.com"

def get_app_version(app_name: str, timeout=4) -> dict:
    """
    获取指定应用程序的最新版本
    
    参数:
        app_name: 程序名称(如 vscode/chrome/nodejs)
        timeout: 请求超时时间(秒)
    
    返回:
        {
            "success": True/False,
            "app": "程序名",
            "version": "版本号",
            "error": "错误信息(仅在失败时存在)"
        }
    """
    try:
        # URL 编码处理特殊字符
        safe_name = quote(app_name.strip())
        url = f"{BASE_URL}/get_version?name={safe_name}"
        
        response = requests.get(url, timeout=timeout, proxies={"http": None, "https": None})
        response.raise_for_status()  # 自动处理 4xx/5xx 错误
        
        data = response.json()
        
        # 处理业务逻辑错误（例如程序不存在）
        if "error" in data:
            return {
                "success": False,
                "error": data["error"],
            }
            
        return {
            "success": True,
            "version": data["version"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"网络请求失败: {str(e)}",
        }
    # except json.JSONDecodeError:
    #     return {
    #         "success": False,
    #         "error": "响应解析失败",
    #     }


# -1：使用过新版  0：正常  1：检测到新版本
def check_and_update_files(target_version) -> int:
    # 检查目录是否存在，不存在则创建
    if not os.path.exists(log_data_dir):
        os.makedirs(log_data_dir)
    
    # 检查是否需要更新文件
    need_update = False
    
    # 检查autoversion.txt是否存在或内容是否正确
    if not os.path.exists(autoversion_path):
        need_update = True
    else:
        with open(autoversion_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            data = None
            for i in range(3):
                data = get_app_version("ExpressCommand")
                if data["success"]:
                    break
            try:
                if int(content) > int(target_version):
                    return -1
                if data["success"]:
                    print(data["version"])
                    if int(data["version"]) > int(target_version):
                        return 1
                elif not data["success"]:
                    return 2
            except Exception:
                return 2


            except:
                pass
            if content != target_version:
                need_update = True
    
    # 检查autoconfig.txt是否存在
    if not os.path.exists(autoconfig_path):
        need_update = True
    
    # 如果需要更新，则写入文件
    if need_update:
        # 写入autoversion.txt
        with open(autoversion_path, 'w', encoding='utf-8') as f:
            f.write(target_version)
        
        # 写入autoconfig.txt
        with open(autoconfig_path, 'w', encoding='utf-8') as f:
            json.dump(target_config, f, ensure_ascii=False, indent=4)
        
        print("文件已更新")
    else:
        print("文件已是最新版本，无需更新")
    return 0

