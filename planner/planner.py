from domain.nodes.base import Node

def get_existing_nodes(tool_results: list) -> set[type[Node]]:
    nodes = set()
    for r in tool_results:
        node = getattr(type(r), "node", None)

        if node is None:
            raise ValueError(f"{type(r).__name__} missing 'node' attribute")

        nodes.add(node)
    return nodes


def plan_tools(
        target_nodes: list[type[Node]],
        existing_nodes: set[type[Node]],
        node_to_deps: dict[type[Node], list[type[Node]]],
        node_to_tools: dict[type[Node], list[str]],
) -> list[str]:

    """
    输入: target entities
    输出: 对应的 tools
    """

    path = set()
    done = set()
    tools_needed = []
    tools_seen = set()

    def resolve(node):
        # 0.1 检查是否: node已有 (ie.在tool_results里)
        if node in existing_nodes:
            return

        # 0.2 检查是否: 已经检查过了
        if node in done:
            return

        # 0.3 检查是否: 死循环
        if node in path:
            raise Exception(f"cycle detected: {node}")

        # 0.4 进入path
        path.add(node)

        # 1. 先找前置依赖
        for dep in node_to_deps.get(node, []):
            resolve(dep) # 先搞依赖

        # 2. 再获取自己对应的tool
        tool_list = node_to_tools.get(node, [])
        if not tool_list:
            raise ValueError(f"no tool can produce {node}")
        if len(tool_list) > 1:
            raise ValueError(f"multiple tools can produce {node.__name__}: {tool_list}."
                             f"split node semantics or define an explicit selection strategy.")
        t = tool_list[0] # 目前只加第1个tool. 未来选择策略(优先:缓存/本地DB/低延迟, 或LLM选)
        if t not in tools_seen:
            tools_needed.append(t)
            tools_seen.add(t)

        done.add(node)
        path.remove(node)


    # 🚀 主流程 (target_nodes里的每个node, 都需resolve (找dep 放到tool_results列表))
    for node in target_nodes:
        resolve(node)

    return tools_needed


