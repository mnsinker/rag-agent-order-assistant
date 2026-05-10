from typing import get_type_hints, get_origin, Union, get_args

from utils.type_utils import is_primitive


def get_node_from_type(typ):
    """
    primitive       -> None
    DTO             -> DTO.node
    Optional[DTO]   -> DTO.node
    """
    # case 1. primitive
    if is_primitive(typ):
        return None

    origin = get_origin(typ)
    # case 2. Union / Optional
    if origin is Union:
        args = [arg for arg in get_args(typ) if arg is not type(None)] # 过滤掉NoneType, 剩下的就是真实的类型参数
        if len(args) != 1:
            raise ValueError(f"{typ} must have exactly one argument")
        return getattr(args[0], "node", None)

    # case 3. DTO (直接获取)
    return getattr(typ, "node", None)


def derive_tool_schema(func) -> dict:
    # 0️⃣ 拿到 hints
    hints = get_type_hints(func)

    if "return" not in hints:
        raise ValueError(f"{func.__name__} must have a 'return type'")

    # 1️⃣ 拿输出
    provides_dto = hints["return"]
    provides = {
        "dto": provides_dto,
        "node": get_node_from_type(provides_dto)
    }

    # 2️⃣ 拿输入
    requires = {}
    for name, typ in hints.items():
        if name == "return":
            continue
        requires[name] = {
            "dto": typ,
            "node": get_node_from_type(typ)
        }

    return {
        "tool": func.__name__,
        "requires": requires,
        "provides": provides,
    }


