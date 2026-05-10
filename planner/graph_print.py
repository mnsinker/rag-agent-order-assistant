
def print_graph(node_to_deps):
    print("\n=======TOOL GRAPH======")

    for node, deps in node_to_deps.items():
        dep_names = [d.__name__ for d in deps]
        category = getattr(getattr(node, "meta", None), "category", "unknown")
        print(f'{dep_names} → {node.__name__} [{category}]')

