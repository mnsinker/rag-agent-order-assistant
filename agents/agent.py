from tools.registry import tools
from utils.make_response import make_response
from agents.intent import get_intent
from agents.extractors import extractors


def agent(query: str) -> dict:
    # step1. 决策: 用哪个tool
    intent = get_intent(query)
    if not intent:
        return make_response(False, None, 'intent not recognized')

    # step2. 路由
    tool_obj = tools.get(intent)
    if not tool_obj:
        return make_response(False, None, 'no matching tool')

    # step3. 调工具
    # 3.1 提取输入参数
    # 3.1.1 获取tool_obj所需参数, 再从query里去拿到, 再跑tool_obj.run(**params)
    params = {}
    for required_arg, _ in tool_obj.args.items():
        extractor_method = extractors.get(required_arg)

        if extractor_method is None:
            return make_response(False, None, f'no matching extractor for param {required_arg}')
        value = extractor_method(query)

        if value is None:
            return make_response(False, None, f'missing or invalid param: {required_arg}')
        params[required_arg] = value # 参数的值 添加到 dict里, eg. order_id: '123'


    # 3.2 触发执行
    try:
        return tool_obj.run(**params) # 把准备好的param dict 喂给 run()
    except Exception as e:
        return make_response(False, None, str(e))



response = agent('订单123已发货吗?')
print(f'response: {response}')


