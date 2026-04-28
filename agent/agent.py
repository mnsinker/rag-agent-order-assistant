from audit.audit_logger import AuditLogger
from errors.validation import ValidationError
from llm.client import call_llm_with_retry, call_llm
from planner.planner import plan_tools
from planner.graph_registry import get_graph
from planner.planner import get_existing_entities
from planner.intent_mapping import INTENT_TO_ENTITIES
from utils.arg_utils import build_params
from utils.make_response import make_response
from utils.tool_schemas_utils import get_all_tool_schemas
from errors.tool import ExecutionError
from utils.llm_utils import safe_parse_llm_output
from tools.resolver import resolve_tool
from utils.arg_utils import build_args
from validators.validator import validate_params, validate_structure
from llm.responder import generate_final_result
audit = AuditLogger()


def decide_with_retry(query: str, tool_schemas: list, max_retry: int=1) -> dict | None:
    error_message = None

    for i in range(max_retry):
        if error_message:
            llm_raw = call_llm_with_retry(query, tool_schemas, error_message)
        else:
            llm_raw = call_llm(query, tool_schemas)

        audit.log(step="llm_raw", input={"query": query, "retry": f"第{i+1}次try"}, output={"raw": llm_raw})
        intent_call = safe_parse_llm_output(llm_raw)
        error_message = validate_structure(intent_call)

        if not error_message:
            return intent_call

    return None


def agent(query: str) -> dict:
    # 0. 取第1个tool (因为目前是 single-intent system)
    tool_schemas: list = get_all_tool_schemas()
    intent_call = decide_with_retry(query, tool_schemas, max_retry=2)
    if not intent_call:
        return make_response(False, None, "LLM planning failed")

    try:
        # 0️⃣ 检查 tool_call 的结构 (是否符合contract)
        intent = intent_call["intent"]  # [WARNING] 只取第1个step, multi-step ignored
        intent_args = intent_call["args"]

        if intent not in INTENT_TO_ENTITIES:
            raise ValidationError(f"unknown intent: {intent}")

        # 1️⃣ PLANNING
        tool_results = []
        target_entities = INTENT_TO_ENTITIES[intent]
        existing_entities = get_existing_entities(tool_results)
        edges, entity_to_tools = get_graph()
        planned_tools = plan_tools(target_entities, existing_entities, edges, entity_to_tools)
        steps = [{"tool": t, "args": {}} for t in planned_tools]

        # 2️⃣ EXECUTION (三段式)
        for step in steps:
                tool = resolve_tool(step["tool"])  # 之前是validate_tool_exists ❗️
                args = build_args(tool, intent_args)  # 只为最终intent tool, build args
                params = build_params(tool, args, tool_results, query)
                validate_params(tool, params)

                # run
                audit.log(step="before_tool", tool=tool.name, input=params)
                result = tool.run(**params)
                tool_results.append(result)
                audit.log(step="after_tool", tool=tool.name, output=result)

    except (ExecutionError, ValidationError) as e:
        audit.log(step="error", error=str(e))
        return make_response(False, None, str(e))

    # 3️⃣ final answer
    final_answer = generate_final_result(query, tool_results)
    audit.log(step="final_answer", input={"query": query, "tool_results": tool_results}, output=final_answer)
    return make_response(True, final_answer)


# ==== 测试 ======
response = agent('帮我判断订单123有没有风险')
print('response: ', response)

# ===== 打印 audit ========

for log in audit.get_logs():
    print(log)

