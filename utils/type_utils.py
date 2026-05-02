from typing import Union, get_origin, get_args


def is_primitive(typ):
    PRIMITIVE = (str, int, float, bool)
    origin = get_origin(typ)

    # 场景1: typ 是 primitive
    if typ in PRIMITIVE:
        return True

    # 场景2: typ 是 Optional / Union ( eg. Optional[str], Union(str, None) )
    if origin is Union:
        args = get_args(typ)
        return all(arg in PRIMITIVE or arg is type(None) for arg in args)

    # 场景3: typ 是其他泛型 (list, dict, tuple, 自定义泛型)
    return False

