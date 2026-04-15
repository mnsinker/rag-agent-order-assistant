from audit.audit_logger import AuditLogger
from errors.validation import ValidationError
from llm.client import call_llm_with_retry, call_llm
from utils.arg_utils import find_missing_dependencies, fill_args_from_context
from utils.make_response import make_response
from tools.get_all_tool_schemas import get_all_tool_schemas
from tools.registry import tools
from errors.tool import ExecutionError
from validators.llm_validator import validate_tool_args
from validators.parse_llm_ouput import safe_parse_llm_output
from validators.resolver import resolve_args, apply_param_correction
from validators.validator import validate_args_from_llm, validate_params, validate_structure, validate_tool_exists
from llm.responder import generate_final_result
audit = AuditLogger()


def decide_with_retry(query: str, tool_schemas: list, max_retry: int=2) -> dict | None:
    error_message = None
    tool_call = {}
    for i in range(max_retry):
        if error_message:
            llm_raw = call_llm_with_retry(query, tool_schemas, error_message)
        else:
            llm_raw = call_llm(query, tool_schemas)

        audit.log(step="llm_raw", input={"query": query, "retry": f"第{i+1}次try"}, output={"raw": llm_raw})
        tool_call = safe_parse_llm_output(llm_raw)
        error_message = validate_tool_args(tool_call) # 👉 验证

    if not error_message:
        return tool_call

    return None


def agent(query: str) -> dict:
    # STEP1. 决策: 用哪个tool
    tool_schemas: list = get_all_tool_schemas()
    tool_call = decide_with_retry(query, tool_schemas, max_retry=2)

    if not tool_call:
        return make_response(False, None, 'LLM planning failed')

    try:
        # 0️⃣ 检查 tool_call 的结构 (是否符合contract)
        validate_structure(tool_call)

        i = 0
        steps = tool_call['steps']
        MAX_STEPS = 50
        continue_bucket = set()
        done_bucket = set()
        tool_results = []
        while i < len(steps):
            # 0. 校验 MAX_STEPS
            if i >= MAX_STEPS:
                return make_response(False, None, 'maximum steps reached')

            step = steps[i]
            step_tool = step['tool']
            step_args = step['args']
            resolved_tool = validate_tool_exists(step_tool)

            # 🩸加进continue_bucket里
            continue_bucket.add(step_tool)

            # 1️⃣ validate
            validate_args_from_llm(resolved_tool, step_args)

            # 2️⃣ 如有deps: (deps = missing_steps;  dep = ms)
            missing_steps = find_missing_dependencies(resolved_tool, tool_results, tools)
            inserted = False
            if missing_steps:
                for ms in missing_steps:
                    if ms['tool'] in continue_bucket:   # if dep ∈ continued: 报错死循环
                        return make_response(False, step, f"cycle: {ms['tool']}")
                    if ms['tool'] not in done_bucket:   # if dep 不在 continued AND 不在 done 里
                        steps[i:i] = [ms]
                        inserted = True
                        break
            if inserted:
                continue

            # 3️⃣ 如无deps: args 处理
            resolved_args = resolve_args(resolved_tool, step_args)
            params = fill_args_from_context(resolved_tool, resolved_args, tool_results)
            params = apply_param_correction(query, params, resolved_tool)
            validate_params(resolved_tool, params)

            # 4️⃣ run
            audit.log(step="before_tool", tool=resolved_tool.name, input=params)
            result = resolved_tool.run(**params)
            tool_results.append(result)
            audit.log(step="after_tool", tool=resolved_tool.name, output=result)

            # 🩸cleanup
            continue_bucket.remove(step_tool)
            done_bucket.add(step_tool)
            i += 1
    except (ExecutionError, ValidationError) as e:
        audit.log(step="error", error=str(e))
        return make_response(False, None, str(e))

    final_answer = generate_final_result(query, tool_results)
    audit.log(step="final_answer", input={"query": query, "tool_results": tool_results}, output=final_answer)
    return make_response(True, final_answer)


# ==== 测试 ======
response = agent('帮我判断订单123有没有风险')
print('response: ', response)

# ===== 打印 audit ========

for log in audit.get_logs():
    print(log)

