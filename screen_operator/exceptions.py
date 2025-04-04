# exceptions.py
class ScreenOperatorError(Exception):
    """基础异常类"""
    pass

class TemplateMatchTimeout(ScreenOperatorError):
    """模板匹配超时异常"""
    pass

class TemplateNotFound(ScreenOperatorError):
    """模板未找到异常"""
    pass