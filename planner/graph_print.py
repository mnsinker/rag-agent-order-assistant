def print_graph(entity_to_deps):
    print("\n=======TOOL GRAPH======")

    for entity, deps in entity_to_deps.items():
        dep_names = [d.__name__ for d in deps]
        print(f'{dep_names} → {entity.__name__}')

