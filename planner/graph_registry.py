from planner.graph_build import build_graph
from tools.registry import tools

_entity_to_deps = None
_entity_to_tools = None
_tool_funcs = [t.func for t in tools.values()]

def get_graph():
    global _entity_to_deps, _entity_to_tools # 修改全局变量

    if _entity_to_deps is None:
        _entity_to_deps, _entity_to_tools = build_graph(_tool_funcs)

    return _entity_to_deps, _entity_to_tools
