# config_accessor.py
import json
import tkinter as tk
from typing import Dict, Any

class ConfigFileOperator:
    """配置文件直接操作类"""
    def __init__(self, filepath: str = r"C:\Program Files\LogData\autoconfig.txt"):
        self.filepath = filepath
    
    def load_raw(self) -> Dict[str, Any]:
        """直接读取原始配置文件内容"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise IOError(f"配置文件读取失败: {str(e)}")
    
    def get_selection_value(self, name: str) -> Any:
        """直接获取指定配置项的值"""
        config = self.load_raw()
        for item in config['selection']:
            if item['name'] == name:
                return item['option']
        raise KeyError(f"配置项 {name} 不存在")
    
    def update_selection(self, name: str, value: Any) -> None:
        """直接更新配置文件"""
        config = self.load_raw()
        updated = False
        
        for item in config['selection']:
            if item['name'] == name:
                item['option'] = value
                updated = True
                break
        
        if not updated:
            raise KeyError(f"配置项 {name} 不存在")
        
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise IOError(f"配置文件写入失败: {str(e)}")

class ConfigAccessor(ConfigFileOperator):
    """增强版配置访问器（继承文件操作功能）"""
    def __init__(self, editor=None):
        super().__init__()
        self.editor = editor
        if editor is not None:
            self._build_field_map()
        
    def _build_field_map(self):
        """构建字段映射关系"""
        self.field_map = {}
        for name, var, field_type in self.editor.fields:
            self.field_map[name] = {
                'var': var,
                'type': field_type
            }
    
    def get(self, name):
        """获取参数值"""
        if name not in self.field_map:
            raise KeyError(f"Parameter '{name}' not found")
            
        field = self.field_map[name]
        return field['var'].get()
    
    def set(self, name, value):
        """设置参数值"""
        if name not in self.field_map:
            raise KeyError(f"Parameter '{name}' not found")
            
        field = self.field_map[name]
        if field['type'] == 'bool' and not isinstance(value, bool):
            raise TypeError(f"Parameter '{name}' requires boolean value")
        field['var'].set(value)
    
    def chain(self):
        """链式调用支持"""
        return self.ChainWrapper(self)
    
    class ChainWrapper:
        """链式调用包装器"""
        def __init__(self, accessor):
            self.accessor = accessor
            
        def get(self, name):
            return self.accessor.get(name)
            
        def set(self, name, value):
            self.accessor.set(name, value)
            return self