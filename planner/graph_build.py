from typing import get_origin, Union, get_args
from planner.graph_validation import validate_graph
from tools.schema import derive_tool_schema
from utils.type_utils import is_primitive


def build_graph(tool_funcs: list) -> tuple[dict, dict]:
    """
    :param
        - tool_funcs: 所有 tool 的函数列表 (来自 tool registry)
    :return:
        - node_to_deps: {(Node, Node)}
        - node_to_tools: {Node: [tool_name]}
    """
    node_to_deps = {}
    node_to_tools = {}

    for func in tool_funcs:
        schema = derive_tool_schema(func)

        tool_name = schema["tool"]
        provides_node = schema["provides"]["node"]   # Node
        requires_nodes = []                    # List[Node, Node ...]

        if provides_node is None:
            raise ValueError(f"f{tool_name} missing provides node")


        for meta in schema["requires"].values():
            dto = meta.get("dto")

            if is_primitive(dto): # primitive -> 跳过, 不把 primitive arg 加入 graph
                continue
            required_node = meta["node"]

            if required_node is None:
                raise ValueError(f"f{dto} missing 'node' attribute")
            if required_node == provides_node:  # 校验: 如require的node == provides_node, 跳过, 防死循环
                continue
            if required_node not in requires_nodes:
                requires_nodes.append(required_node)


        # edges
        node_to_deps.setdefault(provides_node, []).extend(requires_nodes)
        # node_to_tools
        node_to_tools.setdefault(provides_node, []).append(tool_name)

    return node_to_deps, node_to_tools
