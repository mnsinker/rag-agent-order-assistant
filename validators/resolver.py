import difflib
from errors.validation import ValidationError
from tools.base import Tool
from tools.registry import tools
from utils.extractors import extract_order_id

def resolve_tool(name: str) -> Tool | None:
    # 1. exact match
    if name in tools:
        return tools[name]

    # 2. similarity match
    scores = []
    for key, tool in tools.items():
        score = difflib.SequenceMatcher(None, name, key).ratio()
        scores.append((score, key, tool))
    scores.sort(reverse=True)

    # 2.1 如top2差距太小 -> 认为有歧义 返回None
    if len(scores) >= 2 and abs(scores[0][0] - scores[1][0]) < 0.05:
        return None
    # 2.2 如分数未达到0.6 -> 返回None
    if scores[0][0] > 0.6:
        return scores[0][2]  # tool_obj
    return None



def resolve_args(resolved_tool:Tool, step_args: dict) -> dict:
    resolved_args = {}
    for arg_name, arg_value in step_args.items(): # args = LLM's output
        # 1. exact match
        if arg_name in resolved_tool.llm_args:
            resolved_args[arg_name] = arg_value
            continue

        # 2. similarity match
        best_score = 0
        best_match = None
        for param in resolved_tool.llm_args:
            score = difflib.SequenceMatcher(None, arg_name, param).ratio()
            if score > best_score:
                best_score = score
                best_match = param

        # 3. threshold
        if best_score > 0.5:
            resolved_args[best_match] = arg_value
        else:
            raise ValidationError(f"[WARN] unknown param: {arg_name}")

    return resolved_args


def apply_param_correction(query: str, params: dict, resolved_tool: Tool) -> dict:
    if "order_id" in resolved_tool.llm_args and not params.get("order_id"):     # 需要 "order_id', 但params里又没有
        if extracted := extract_order_id(query):
            params["order_id"] = extracted
    return params

