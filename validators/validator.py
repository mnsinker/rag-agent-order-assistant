from errors.validation import ValidationError
from tools.base import Tool


def validate_structure(intent_call: dict):
    '''
    validate:
        1. intent_call:
            是个dict
        2. intent:
            有"intent"字样
            type = str
        3. args:
            有 "args" 字样
            type = dict
    return:
        None (合法)
        str (错误信息, 当 raise_error=False 时)
    '''
    # 1.1 检查 整个intent_call 是否存在
    if not intent_call:
        return "LLM output is empty"
    # 1.2 检查 intent_call 是否为dict
    if not isinstance(intent_call, dict):
        return "LLM output should be a dict"

    # 2.1 检查 "intent" 字样在不在
    if "intent" not in intent_call:
        return "'intent' is missing"
    # 2.2 检查 intent 是否为str
    if not isinstance(intent_call["intent"], str):
        return "'intent' should be a str"

    args = intent_call["args"]
    # 3.1 检查 "args" 字样在不在
    if args is None:
        return "'args' is missing"
    # 3.2 args 必须是个dict
    if not isinstance(args, dict):
        return "args should be dict"

    return None




def validate_args_from_llm(tool: Tool, step_args: dict):
    '''
    validate args
    1. arg_key: 不允许多
    2. arg_value: 不能是dataclass (LLM 不准提供 dataclass)
    '''
    # 1. 检查 args_key 是否多了 (step_args > tool_obj.args)
    extra_args = set(step_args) - set(tool.args)
    if extra_args:
        raise ValidationError(f"[{tool.name}] got unexpected arg: {extra_args}")

    # 2. 检查 arg_value 必须是 primitive args (白名单)
    for arg_name, arg_value in step_args.items():
        if not isinstance(arg_value, (str, int, float, bool, type(None))):
            raise ValidationError(f"{tool.name} arg '{arg_name}' should be primitive, but got {type(arg_value)}")


def validate_params(resolved_tool: Tool, params: dict):
    '''
    只检查 primitive_args (系统 plan_from_ontology() 已保证 dep_args):
    1. arg_key 是否多了
    2. arg_key 是否少了
    3. arg_value 是否为空
    4. arg_value 是否type正确
    '''
    required_args = resolved_tool.args # 只校验 primitive_args
    # 1. 检查 arg_key 是否少了 ①
    extra_args = set(params) - set(required_args)
    if extra_args:
        raise ValidationError(f"[{resolved_tool.name}] got unexpected args: {extra_args}")

    for arg_name, arg_type in required_args.items():
        # 2.检查 arg_key 是否少了
        if arg_name not in params:
            raise ValidationError(f"[{resolved_tool.name}] missing param '{arg_name}'")
        # 3.检查 arg_value 是否为None
        param_value = params[arg_name]
        if param_value is None:
            raise ValidationError(f"[{resolved_tool.name}] param '{arg_name}': value is None")
        # 4.检查 arg_type 是否不对
        if not isinstance(param_value, arg_type):
            raise ValidationError(f"[{resolved_tool.name}] param '{arg_name}' expected {arg_type.__name__}, but got {type(param_value).__name__}")
