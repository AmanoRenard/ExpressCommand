import win32gui
import win32con
import json

def get_taskbar_apps():
    """获取任务栏正在运行的应用程序窗口（等效alt+tab可见列表）"""
    titles = []
    
    def callback(hwnd, _):
        # 必须满足的条件
        if not win32gui.IsWindowVisible(hwnd):
            return
        
        # 排除工具窗口
        if win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOOLWINDOW:
            return
        
        # 排除没有标题的窗口
        title = win32gui.GetWindowText(hwnd).strip()
        if not title:
            return
        
        # 关键判断：检查窗口是否拥有所有者（是否是顶层窗口）
        if win32gui.GetWindow(hwnd, win32con.GW_OWNER) != 0:
            return
        
        # 排除系统进程
        if title in ["Program Manager", "Windows Input Experience"]:
            return
        
        titles.append(title)
    
    win32gui.EnumWindows(callback, None)
    
    # 去重并保持顺序
    seen = set()
    return [x for x in titles if not (x in seen or seen.add(x))]

def update_group_names():
    taskbar_apps = get_taskbar_apps()
    # print("当前任务栏应用：", taskbar_apps)  # 调试用
    
    with open(r'C:\Program Files\LogData\autoconfig.txt', 'r+', encoding='utf-8') as f:
        config = json.load(f)
        for item in config['selectable']:
            if item['text'].startswith('群名：'):
                item['options'] = taskbar_apps
        f.seek(0)
        json.dump(config, f, ensure_ascii=False, indent=4)
        f.truncate()

if __name__ == '__main__':
    update_group_names()