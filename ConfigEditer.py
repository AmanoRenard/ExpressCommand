import tkinter as tk
from tkinter import messagebox
import json
import sys

class ConfigEditor:
    def __init__(self, master, config_path=None, title_name="配置编辑"):
        self.master = master
        master.title(title_name)
        
        # 初始化时记录初始尺寸
        self.base_height = 300  # 基础高度（包含按钮和边距）
        self.item_height = 40   # 每个配置项的预估高度
        
        # 处理关闭事件
        # master.protocol("WM_DELETE_WINDOW", self.safe_close)
        
        # 配置文件路径改为参数
        self.config_path = config_path or r"C:\Program Files\LogData\autoconfig.txt"
        
        # 加载配置
        self.config_data = self.load_config()
        if not self.config_data:
            return
        self.selection_map = {item["name"]: item for item in self.config_data["selection"]}
        self.fields = []
        
        self.create_widgets()

        # 创建界面后自动调整高度
        self.auto_adjust_window_height()

    def load_config(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("错误", f"配置文件加载失败: {str(e)}")
            return None
        
    def auto_adjust_window_height(self):
        """自动调整窗口高度"""
        # 计算实际内容高度
        content_height = len(self.config_data["selectable"]) * self.item_height
        total_height = self.base_height + content_height
        
        # 设置最小/最大高度限制
        min_height = 300
        max_height = 800
        final_height = min(max(total_height, min_height), max_height)
        
        # 获取当前窗口尺寸
        current_geometry = self.master.geometry().split("+")[0]
        current_width = current_geometry.split("x")[0]
        
        # 应用新高度
        self.master.geometry(f"{current_width}x{final_height}")

    def create_widgets(self):
        # 修改为统一管理控件
        self.content_frames = []
        
        for item in self.config_data["selectable"]:
            frame = tk.Frame(self.master)
            frame.pack(fill=tk.X, padx=5, pady=5)
            self.content_frames.append(frame)
            
            tk.Label(frame, text=item["text"]).pack(side=tk.LEFT)
            
            current_value = self.selection_map[item["name"]]["option"]
            
            # 修复下拉菜单显示问题
            if isinstance(item["options"], list):
                if all(isinstance(opt, bool) for opt in item["options"]):
                    var = tk.BooleanVar(frame, value=current_value)
                    tk.Checkbutton(frame, variable=var).pack(side=tk.RIGHT)
                    self.fields.append((item["name"], var, "bool"))
                else:
                    var = tk.StringVar(frame, value=current_value)  # 添加frame作为master参数
                    # 强制更新下拉菜单显示
                    menu = tk.OptionMenu(frame, var, *item["options"])
                    menu.pack(side=tk.RIGHT)
                    var.set(current_value)  # 显式设置当前值
                    self.fields.append((item["name"], var, "option"))
            else:
                var = tk.StringVar(frame, value=str(current_value))
                tk.Entry(frame, textvariable=var).pack(side=tk.RIGHT)
                self.fields.append((item["name"], var, "text"))

        # 添加底部按钮容器
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)
        tk.Button(self.button_frame, text="保存配置", command=self.save_config).pack()

    def save_config(self):
        try:
            for name, var, field_type in self.fields:
                value = var.get()
                if field_type == "bool":
                    value = bool(value)
                for item in self.config_data["selection"]:
                    if item["name"] == name:
                        item["option"] = value
                        break
            
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
            self.master.withdraw()
            messagebox.showinfo("成功", "配置保存成功\n请重新启动程序")
            
        except Exception as e:
            self.master.withdraw()
            messagebox.showerror("错误", f"保存失败: {str(e)}")
        finally:
            self.safe_close()

    def safe_close(self):
        """安全关闭窗口的方法"""
        self.master.destroy()
        self.master.quit()  # 确保终止主循环

def main(parent=None, config_path=None):
    """改进后的入口函数"""
    if parent:
        window = tk.Toplevel(parent)
        window.transient(parent)  # 设为工具窗口
    else:
        window = tk.Tk()
    window.withdraw()

    # 隐藏窗口图标（跨平台方案）
    window.wm_iconbitmap('')  # Windows系统

    
    # 先创建编辑器实例
    app = ConfigEditor(window, config_path)

    # 窗口样式设置
    window.resizable(False, False)  # 禁止调整大小
    window.attributes('-toolwindow', 1)  # 隐藏最大/最小化按钮（Windows）
    window.attributes('-topmost', True)
    window.lift()
    
    if not app.config_data:
        window.destroy()
        return
    
    # 精确计算高度（需在控件创建后）
    window.update_idletasks()  # 强制更新布局计算
    
    # 获取实际需求高度
    req_width = window.winfo_reqwidth()
    req_height = window.winfo_reqheight()
    
    # 相对于屏幕居中
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - req_width) // 2
    y = (screen_height - req_height ) // 2
    
    # 应用新位置（保持原有尺寸）
    window.geometry(f"{req_width}x{req_height}+{x}+{y}")
    window.deiconify()
    
    if not parent:
        window.mainloop()

if __name__ == "__main__":
    main()