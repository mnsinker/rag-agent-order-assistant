from typing import get_type_hints


def derive_tool_schema(func) -> dict:
    # 0️⃣ 拿到 hints
    hints = get_type_hints(func)

    if "return" not in hints:
        raise ValueError(f"{func.__name__} must have a 'return type'")

    # 1️⃣ 拿输出
    provides_dto = hints["return"]
    provides = {
        "dto": provides_dto,
        "entity": getattr(provides_dto, "entity", None)
    }

    # 2️⃣ 拿输入
    requires = {}
    for name, typ in hints.items():
        if name == "return":
            continue
        requires[name] = {
            "dto": typ,
            "entity": getattr(typ, "entity", None)
        }

    return {
        "tool": func.__name__,
        "requires": requires,
        "provides": provides,
    }


