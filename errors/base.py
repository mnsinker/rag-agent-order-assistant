class ToolError(Exception):     # ToolError: 带结构的 Exception
    def __init__(self, message: str, code: str = None, data: dict = None):
        super().__init__(message)
        self.message = message  # 给人看的
        self.code = code        # 给机器判断用
        self.data = data or {}  # 上下文信息
