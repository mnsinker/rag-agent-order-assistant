from dataclasses import asdict, is_dataclass
from typing import Optional, Any

def make_response(success: bool, data: Optional[Any] = None, error: str = "") -> dict:
    if data is None:
        parsed = None

    elif isinstance(data, list):
        parsed = [asdict(d) if is_dataclass(d) else d for d in data]

    elif is_dataclass(data):
        parsed = asdict(data)

    else:
        raise TypeError(f"Unsupported data type: {type(data)}")

    # 4. 赋值 & 返回
    return {
        "success": True,
        "data": parsed,
        "error": error
    }
