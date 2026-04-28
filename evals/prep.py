from tools.registry import tools


def print_dependencies():
    for name, tool in tools.items():
        llm_args = list(getattr(tool, "llm_args", {}).keys())
        dep_args = {k: v.__name__ for k, v in getattr(tool, "dependency_args", {}).items()}
        output_type = getattr(tool, "output_type").__name__

        print(f'''
        {name}: 
        llm_args: {llm_args}
        dep_args: {dep_args}
        output_type: {output_type}
        ''')


print_dependencies()

