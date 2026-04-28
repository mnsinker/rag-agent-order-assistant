from typing import get_type_hints
from planner.dto_to_entity import DTO_TO_ENTITY

def derive_tool_io(func) -> dict:
    """
    从 tool signature 里推到:
    - requires: 这个 tool 需要哪些 Entity
    - provides: 这个 tool 生产哪个 Entity
    """
    # 0️⃣ 拿到 hints
    hints = get_type_hints(func)

    # 1️⃣找输出
    return_model = hints.get('return')
    provides = DTO_TO_ENTITY.get(return_model)

    # 2️⃣找输入
    requires = []
    for name, typ in hints.items():
        if name == 'return':
            continue
        entity = DTO_TO_ENTITY.get(typ)
        if entity:
            requires.append(entity)

    return {
        "tool": func.__name__,
        "requires": requires,
        "provides": provides,
    }
