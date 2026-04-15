from errors.validation import ValidationError
from tools.base import Tool
from validators.resolver import resolve_args


def match_dependency(result, dep_type) -> bool:
    return isinstance(result, dep_type)


def find_missing_dependencies(resolved_tool: Tool, tool_results: list, tools: dict) -> list:
    missing_steps = []
    seen = set()

    for dep_name, dep_type in resolved_tool.dependency_args.items():
        # 1 如果需要的, 已经在tool_results里有, 则跳过
        # (生成式写法 - any相当于从生成器里取值, 取到False就扔掉, 再取下一个r, 取到第一个True就ok了)
        if any(isinstance(r, dep_type) for r in tool_results):
            continue

        # 2.2 如果没有, 就补
        producer = None # 找生产者 tool
        for tool in tools.values():
            if tool.get_output_type() == dep_type:
                producer = tool
                break

        if not producer: # 如果在tools里没找到
            raise Exception(f"no tool can produce dependency {dep_type}")

        if producer.name not in seen: # 防止重复加到missing_steps里
            seen.add(producer.name)
            missing_steps.append({"tool": producer.name, "args": {}})

    return missing_steps



def fill_args_from_context(resolved_tool: Tool, resolved_args: dict, tool_results: list) -> dict:
    '''
    >> 尽量补args, 不负责补全;  arg的完整性在 validate_params 里保证
    目的: 把step里的args fill进去 -> 最终得到(返回)一个的args dict

    最终想得到: {'arg_name1': value1,  'arg_name2': value2}
            - arg_name: 从resolved_tool里的 .llm_args 和 .dependency_args 里来 (应该有哪些arg name)
            - arg_value: 从llm_output的 step_arg 里获得  +  从已有的tool_results里获得

    所以输入: resolved_tool, step_arg, tool_results
    所以输出: args: dict
    '''
    # 0. copy resolved_args
    args = dict(resolved_args)

    # 1.先满足 dependency
    for req_name, req_type in resolved_tool.dependency_args.items():
        found = False
        for r in reversed(tool_results):
            if isinstance(r, req_type):
                found = True
                args[req_name] = r
                break
        if not found:
            raise ValidationError(f"missing dependency in tool_results: {req_name}")

    # 2. 再从 context obj 里补: 衍生参数
    for req_name in resolved_tool.llm_args:
        for r in reversed(tool_results):
            if hasattr(r, req_name):
                args[req_name] = getattr(r, req_name)
                break
    # 3. fallback: 从 llm_output 里取值 (可以不写, 因为llm_output已经包含在args value里了)
    #     if req_name in args and args[req_name] is not None:
    #         continue

    return args