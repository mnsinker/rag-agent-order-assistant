from planner.derive import derive_tool_io


def build_graph(tool_funcs: list) -> tuple[dict, dict]:
    """
    :param
        - tool_funcs: 所有 tool 的函数列表 (来自 tool registry)
    :return:
        - edges: {(Entity, Entity)}
        - entity_to_tools: {Entity: [tool_name]}
    """
    entity_to_deps = {}
    entity_to_tools = {}

    for func in tool_funcs:
        tool_io = derive_tool_io(func)
        tool_name = tool_io["tool"]
        requires = tool_io["requires"]   # List[Entity, Entity ...]
        provides = tool_io["provides"]   # Entity

        if provides is None: # 非空判断
            continue

        # entity_to_tools
        entity_to_tools.setdefault(provides, []).append(tool_name)

        # edges
        entity_to_deps.setdefault(provides, []).extend(requires)

    return entity_to_deps, entity_to_tools
