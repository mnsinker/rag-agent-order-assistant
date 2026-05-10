def validate_graph(node_to_deps, node_to_tools) -> None:
    _validate_cycle(node_to_deps)
    _validate_integrity(node_to_deps, node_to_tools)


def _validate_integrity(node_to_deps, node_to_tools) -> None:
    # 1. 检查: 每个 node 必须可被生产
    for node in node_to_deps:
        if node not in node_to_tools:
            raise ValueError(f'{node} has deps, but no tool produces it')

    # 2. 检查: 每个 dep 必须可被生产
    for node, deps in node_to_deps.items():
        for dep in deps:
            if dep not in node_to_tools: # 非source entity
                raise ValueError(f'{dep} is required, but no tool produces it')

    # 3. 检查: 孤立节点
    for node in node_to_deps:
        if node not in node_to_tools and not node_to_deps.get(node):
            print(f'[WARNING] {node} is unused source')


def _validate_cycle(node_to_deps) -> None:
    visited = set()
    path = set()

    def dfs(node):
        if node in path:
            raise ValueError(f'cycle detected: {node}')
        if node in visited:
            return

        path.add(node)
        for dep in node_to_deps.get(node, []):
            dfs(dep)
        path.remove(node)
        visited.add(node)

    for node in node_to_deps:
        dfs(node)

