from dataclasses import asdict, is_dataclass
from typing import Optional, Any

def make_response(success: bool, data: Optional[Any] = None, error: str = "") -> dict:
    # 1. 初始化 response
    response = {"success": success, "data": None, "error": error}

    # 2.快速返回 (卫语句)
    if data is None:
        return response

    # 3. 检查 data 类型, 必须是 dataclass 且 不能是类本身 (代码: if 与dataclass无关 或 是个类, 则...)
    # is_dataclass 对类本身 & 对象 都会返回True, 所以要排除 类本身 (类的类型 = type, 不是class)
    if not is_dataclass(data) or isinstance(data, type):
        raise TypeError(f"data must be an instance of DataclassBase, but got {type(data).__name__}")

    # 4. 赋值 & 返回
    response["data"] = asdict(data)
    return response

