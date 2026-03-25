from tools.check_refund import check_refund
from utils.make_response import make_response
from utils.to_json_type import to_json_type

class Tool:
    def __init__(self, name, description, func, **kwargs):
        self.name = name
        self.description = description
        self.func = func
        self.args = kwargs # 创建tool_obj时, 定义所需的参数
    def run(self, **param): # 调方法时, agent传入的参数
        # 校验参数数据类型
        for required_arg, required_type in self.args.items():

            if required_arg not in param:
                raise Exception(f'missing param: {required_arg}')

            value = param[required_arg]
            if not isinstance(value, required_type):
                try:
                    value = required_type(value)
                except:
                    raise Exception(f'{required_arg} required type: {required_type}, but got: {type(value)}')
            param[required_arg] = value

        return self.func(**param)

    def to_schema(self):
        response = {'name': self.name, 'description': self.description}
        response['parameters'] = {}
        response['parameters']['type'] = 'object'
        response['parameters']['properties'] = {
            required_arg: {"type": to_json_type(required_type)} for required_arg, required_type in self.args.items()
        }
        response['parameters']['required'] = list(self.args.keys())
        return response


tool_obj = Tool('check_refund', 'check whether refundable', check_refund, order_id=str)
res = tool_obj.to_schema()
print(res)