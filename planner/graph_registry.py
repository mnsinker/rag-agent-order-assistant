from planner.graph_build import build_graph
from planner.graph_print import print_graph
from planner.graph_validation import validate_graph
from tools.registry import tools

_node_to_deps = None
_node_to_tools = None
_tool_funcs = [t.func for t in tools.values()]

def get_graph():
    global _node_to_deps, _node_to_tools # 修改全局变量

    if _node_to_deps is None:
        _node_to_deps, _node_to_tools = build_graph(_tool_funcs)
        validate_graph(_node_to_deps, _node_to_tools)

    return _node_to_deps, _node_to_tools


if __name__ == "__main__":
    _node_to_deps, _node_to_tools = get_graph()
    print_graph(_node_to_deps)