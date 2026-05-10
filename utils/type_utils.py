from types import UnionType
from typing import Union, get_origin, get_args


def is_primitive(typ):
    PRIMITIVES = (str, int, float, bool)
    origin = get_origin(typ)

    # 场景1: typ 是 primitive
    if typ in PRIMITIVES:
        return True

    # 场景2: typ 是 Optional / Union
    # Python <=3.9 style: typing.Union
    # Python 3.10+ style: str | None -> types.UnionType
    if origin is Union or origin is UnionType:
        args = get_args(typ)
        return all(arg in PRIMITIVES or arg is type(None) for arg in args)

    # 场景3: typ 是其他泛型 (list, dict, tuple, 自定义泛型)
    return False

