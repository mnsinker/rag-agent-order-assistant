from errors.base import ToolError
from tools.schema import derive_tool_schema
from utils.to_json_type import to_json_type
from errors.validation import ValidationError
from errors.tool import ExecutionError
from utils.type_utils import is_primitive


class Tool:
    def __init__(self, name, description, func, **kwargs):
        self.name = name
        self.description = description
        self.func = func
        schema = derive_tool_schema(func)
        self.args = {arg_name: arg_info["dto"] for arg_name, arg_info in schema['requires'].items()}

    def run(self, **param): # 调方法时, agent传入的参数
        # 1. validate params' data type
        for required_arg, required_type in self.args.items():
            if required_arg not in param:
                raise ValidationError(message=f'missing param: {required_arg}')
            value = param[required_arg]
            if not isinstance(value, required_type):
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
        schema = derive_tool_schema(self.func)
        properties = {}
        required = []

        for name, meta in schema['requires'].items():
            dto = meta["dto"]

            if is_primitive(dto): # 只保留 primitive 给 llm
                properties[name] = {"type": to_json_type(dto)}
                required.append(name)

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            }
        }
