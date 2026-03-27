from errors.base import ToolError
from tools.check_refund import check_refund
from utils.to_json_type import to_json_type
from errors.validation import ValidationError
from errors.tool import ExecutionError

class Tool:
    def __init__(self, name, description, func, **kwargs):
        self.name = name
        self.description = description
        self.func = func
        self.args = kwargs # 创建tool_obj时, 定义所需的参数
    def run(self, **param): # 调方法时, agent传入的参数
        # 1. validate params' data type
        for required_arg, required_type in self.args.items():
            if required_arg not in param:
                raise ValidationError(message=f'missing param: {required_arg}')
            value = param[required_arg]
            if not isinstance(value, required_type):
                try:
                    value = required_type(value)
                except:
                    raise ValidationError(message=f'{required_arg} required type: {required_type}, but got: {type(value)}')
            # 2. add pairs (required_arg: value) in dict
            param[required_arg] = value

        # 3. tool.run(...)
        try:
            return self.func(**param)
        except ToolError:
            raise
        except Exception as e:
            raise ExecutionError(str(e))

    def to_schema(self):
        response = {'name': self.name, 'description': self.description}
        response['parameters'] = {}
        response['parameters']['type'] = 'object'
        response['parameters']['properties'] = {
            required_arg: {"type": to_json_type(required_type)} for required_arg, required_type in self.args.items()
        }
        response['parameters']['required'] = list(self.args.keys())
        return response

