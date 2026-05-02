from typing import get_type_hints

from errors.validation import ValidationError
from tools.base import Tool
from tools.coupon_tool import check_coupon
from utils.extractors import extract_order_id

def build_args(tool: Tool, intent_args: dict) -> dict:
    PRIMITIVE = (str, int, float, bool, type(None))
    args = {}

    for k, v in intent_args.items(): # args = LLM's output
        # 0. validate: 非 primitive
        if not isinstance(v, PRIMITIVE):
            raise ValidationError(f"[{tool.name}] '{k}' must be primitive, but got {type(v).__name__}")

        # 1. 只取 当前tool 所需的 primitive 参数
        if k in tool.args and tool.args[k] in PRIMITIVE:
            args[k] = v

    return args



def build_params(
        tool: Tool,
        args: dict,
        tool_results: list,
        query: str
) -> dict:

    PRIMITIVES = (str, int, float, bool)
    params = {}

    for req_name, req_type in tool.args.items():
        # 1. model arg:
        if req_type not in PRIMITIVES:
            for r in reversed(tool_results):
                if isinstance(r, req_type):
                    params[req_name] = r
                    break

        # 2. primitive arg
        else:
            if req_name in args:
                params[req_name] = args[req_name]

        # 3. fallback (regex 进针对 primitive args)
            elif req_name == "order_id":
                if extracted := extract_order_id(query):
                    params[req_name] = extracted

    return params


def extract_args_from_signature(func) -> dict:
    hints = get_type_hints(func)

    requires = {}
    for name, typ in hints.items():
        if name == 'return':
            continue
        requires.update({name: typ})

    return requires


