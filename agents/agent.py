from models.refund import RefundEligibility
from tools.registry import tools
from utils.make_response import make_response
from agents.mock_llm import mock_llm
from utils.get_all_tool_schemas import get_all_tool_schemas
from errors.validation import ValidationError
from errors.tool import ExecutionError


def agent(query: str) -> dict:
    print('[QUERY]: ', query)
    # step1. 决策: 用哪个tool
    tool_schemas = get_all_tool_schemas()
    tool_call = mock_llm(query, tool_schemas)
    print('[TOOL_CALL]: ', tool_call)


    # step2. 路由
    # 2.1 获得每个tool的tool_obj
    tool_results = []
    for step in tool_call["steps"]:
        tool_name = step['tool']
        tool_args = step['args']
        print(f'[TOOL] {tool_name} {tool_args}')
        tool_obj = tools.get(tool_name)
        if not tool_obj:
            return make_response(False, None, 'no matching tool')


        # step3. 调工具
        # 3.1 准备参数
        params = {}
        for required_arg, value in tool_args.items():
            if value is None:
                return make_response(False, None, f'missing or invalid param: {required_arg}')
            params[required_arg] = value # 参数的值 添加到 dict里, eg. order_id: '123'

        # 3.2 依赖参数 注入
        if tool_results:
            last_result = tool_results[-1]
            if 'eligibility' in tool_obj.args and isinstance(last_result, RefundEligibility):
                params['eligibility'] = last_result

        # 3.2 触发执行
        try:
            tool_result = tool_obj.run(**params) # 把准备好的param dict 喂给 run()
            print('[RESULT]: ', tool_result)
        except ValidationError as e:
            return make_response(False, None, e.message)
        except ExecutionError as e:
            return make_response(False, None, e.message)
        except Exception as e:
            return make_response(False, None, '系统异常')

        # 3.3 append
        tool_results.append(tool_result)

    return make_response(True, tool_results)



response = agent('订单456已发货吗?')
print('response: ', response)


