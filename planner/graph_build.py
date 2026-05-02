from typing import get_origin, Union, get_args

from planner.graph_validation import validate_graph
from tools.schema import derive_tool_schema
from utils.type_utils import is_primitive


def build_graph(tool_funcs: list) -> tuple[dict, dict]:
    """
    :param
        - tool_funcs: 所有 tool 的函数列表 (来自 tool registry)
    :return:
        - edges: {(Entity, Entity)}
        - entity_to_tools: {Entity: [tool_name]}
    """
    PRIMITIVES = (str, int, float, bool)
    entity_to_deps = {}
    entity_to_tools = {}

    for func in tool_funcs:
        schema = derive_tool_schema(func)

        tool_name = schema["tool"]
        provides_entity = schema["provides"]["entity"]   # Entity
        requires_entities = []                           # List[Entity, Entity ...]

        if provides_entity is None:
            raise ValueError(f"f{tool_name} missing provides entity")

        for meta in schema["requires"].values():
            dto = meta.get("dto")

            # 场景1. primitive -> 跳过, 不把 primitive arg 加入 graph
            if is_primitive(dto):
                continue
            # 场景2. Optional / Union
            if get_origin(dto) is Union:
                args = [arg for arg in get_args(dto) if arg is not type(None)] # 过滤掉 None 的 arg
                if len(args) != 1:
                    raise ValueError(f"f{dto} Union type not supported to have more than one argument")
                entity = getattr(args[0], "entity", None)
            # 场景3. 普通DTO
            else:
                entity = getattr(dto, "entity", None)
            # 校验:
            if entity is None:
                raise ValueError(f"{meta['dto']} missing 'entity' attribute")
            # 校验: 如require的entity == provides_entity, 跳过, 防死循环
            if entity == provides_entity:
                continue
            requires_entities.append(entity)

        # edges
        entity_to_deps.setdefault(provides_entity, []).extend(requires_entities)
        # entity_to_tools
        entity_to_tools.setdefault(provides_entity, []).append(tool_name)

    return entity_to_deps, entity_to_tools
