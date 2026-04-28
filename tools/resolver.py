import difflib
from errors.validation import ValidationError
from tools.base import Tool
from tools.registry import tools

def resolve_tool(tool_name: str) -> Tool | None:
    # 1. exact match
    if tool_name in tools:
        return tools[tool_name]

    # 2. similarity match
    scores = []
    for key, tool in tools.items():
        score = difflib.SequenceMatcher(None, tool_name, key).ratio()
        scores.append((score, key, tool))
    scores.sort(reverse=True)

    # 2.1 如top2差距太小 -> 认为有歧义 raise
    if len(scores) >= 2 and abs(scores[0][0] - scores[1][0]) < 0.05:
        raise ValidationError(f"ambiguous tool: {tool_name}")
    # 2.2 如分数未达到0.6 -> raise
    if scores[0][0] > 0.6:
        return scores[0][2]  # tool_obj
    raise ValidationError(f"tool not found: {tool_name}")

