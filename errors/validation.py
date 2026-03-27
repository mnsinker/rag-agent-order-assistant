from .base import ToolError
class ValidationError(ToolError):
    def __init__(self, message='参数错误', data=None):
        super().__init__(message, code='VALIDATION_ERROR', data=data)