from validators.resolver import resolve_tool

def validate_tool_args(tool_call: dict) -> str|None:
    # 1. tool_call 整个dict 是否存在
    if not tool_call:
        return 'LLM output is empty'
    if 'steps' not in tool_call:
        return ("'steps' is missing")
    if not isinstance(tool_call['steps'], list):
        return ("'steps' must be a list")
    for step in tool_call['steps']:
        if 'tool' not in step:
            return ("'tool' is missing")
        if 'args' not in step:
            return ("'args' is missing")
        if not resolve_tool(step['tool']):
            return (f'unknown tool: {step["tool"]}')
    return None
