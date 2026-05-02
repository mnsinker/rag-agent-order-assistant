def validate_graph(entity_to_deps, entity_to_tools) -> None:
    _validate_cycle(entity_to_deps)
    _validate_integrity(entity_to_deps, entity_to_tools)


def _validate_integrity(entity_to_deps, entity_to_tools) -> None:
    # 1. 检查: 每个 entity 必须可被生产
    for entity in entity_to_deps:
        if entity not in entity_to_tools:
            raise ValueError(f'{entity} has deps, but no tool produces it')

    # 2. 检查: 每个dep 必须可被生产
    for entity, deps in entity_to_deps.items():
        for dep in deps:
            if dep not in entity_to_tools and entity_to_deps.get(dep): # 非source entity (如是source, 则entity_to_deps.get(dep) 会是 [] )
                raise ValueError(f'{dep} is required, but no tool produces it')

    # 3. 检查: 孤立节点
    for entity in entity_to_deps:
        if entity not in entity_to_tools and not entity_to_deps.get(entity):
            print(f'[WARNING] {entity} is unused source')


def _validate_cycle(entity_to_deps) -> None:
    visited = set()
    path = set()

    def dfs(node):
        if node in path:
            raise ValueError(f'cycle detected: {node}')
        if node in visited:
            return

        path.add(node)
        for dep in entity_to_deps.get(node, []):
            dfs(dep)
        path.remove(node)
        visited.add(node)


    for node in entity_to_deps:
        dfs(node)

