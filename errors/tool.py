from .base import ToolError
class ExecutionError(ToolError):
    def __init__(self, message="工具执行失败", data=None):
        super().__init__(message, code="EXECUTION_ERROR", data=data)