from errors.validation import ValidationError
from tools.base import Tool
from tools.registry import tools
from .resolver import resolve_tool
from dataclasses import dataclass

def validate_structure(tool_call: dict):
    '''
    validate:
    output层
    1. llm_output: 是个dict
    2. steps: 有"steps"字样
    3. steps: 是个list

    每个step层:
    1. 是个dict
    2. 有'tool'字样
    3. 有'args'字样
    4. args 是个dict

    注: 后续系统注入的dep_step的校验: 略
    '''
    # 1. 检查 整个dict 是否存在
    if not tool_call:
        raise ValidationError('LLM output is empty')
    # 2. 检查 "steps" 字样在不在
    if 'steps' not in tool_call:
        raise ValidationError("'steps' is missing")
    # 3. 检查 "steps" 是不是个list
    if not isinstance(tool_call["steps"], list):
        raise ValidationError("'steps' must be a LIST")

    for step in tool_call["steps"]:
        # 4. 检查 每个step 是不是个dict
        if not isinstance(step, dict):
            raise ValidationError("each step must be a dict")
        # 5. 检查 每个dict 里面是不是有 "tool" 字样
        if 'tool' not in step:
            raise ValidationError("'tool' is missing")
        # 6. 检查 每个dict 里面是不是有 "args" 字样
        if 'args' not in step:
            raise ValidationError("'args' is missing")
        # 7. 检查 每个args 是不是个dict
        if not isinstance(step['args'], dict):
            raise ValidationError("'args' must be a dict")


def validate_tool_exists(step_tool: str):
    resolved_tool = resolve_tool(step_tool)
    if not resolved_tool:
        raise ValidationError(f"tool {step_tool} does not exist")
    return resolved_tool


def validate_args_from_llm(resolved_tool: Tool, step_args: dict):
    '''
    validate llm_args
    1. arg_key: 不允许多
    2. arg_value: 不能是dataclass (LLM 不准提供 dataclass)
    '''
    # 1. 检查 args_key 是否多了 ((step_args > tool_obj.llm_args)
    for arg in step_args:
        if arg not in resolved_tool.llm_args:
            raise ValidationError(f"[{resolved_tool.name}] unexpected arg: {arg}")

    # 2. 检查 args_value 是否有 dataclass
    for dep_name, dep_type in resolved_tool.dependency_args.items():
        if dep_name in step_args:
            raise ValidationError(f"{dep_name} should not be provided by LLM")


def validate_params(resolved_tool: Tool, params: dict):
    '''
    检查:
    1. arg_key 是否多了
    2. arg_key 是否少了
    3. arg_value 是否为空
    4. arg_value 是否type正确
    '''
    args = {} # args = 应该有什么
    args.update(resolved_tool.llm_args)
    args.update(resolved_tool.dependency_args)

    for dep_name, dep_type in args.items():
        # 1.检查 arg_key 是否少了
        if dep_name not in params:
            raise ValidationError(f"missing param {dep_name}")
        # 2.检查 arg_value 是否为None
        if params[dep_name] is None:
            raise ValidationError(f"param {dep_name}: value is None")
        # 3.检查 arg_type 是否不对
        if not isinstance(params[dep_name], dep_type):
            raise ValidationError(f"param {dep_name} expected {dep_type.__name__}, but got {type(params[dep_name]).__name__}")


    for param_name, param_type in params.items():
        # 4.检查 arg_key 是否多了
        if param_name not in args:
            raise ValidationError(f"unexpected param {param_name}")
