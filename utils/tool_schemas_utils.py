from tools.registry import tools
def get_all_tool_schemas() -> list:
    tool_schemas = []

    for tool in tools.values():
        schema = tool.to_schema()
        tool_schemas.append(schema)
    return tool_schemas


''' 想要的效果: 
[
  {'name': 'check_refund',
  'description': 'check whether order is refundable',
  'parameters': {'type': 'object',
                  'properties': {'order_id': {'type': 'string'}},
                  'required': ['order_id']}},
  {'name': 'get_shipping_status',
  'description': 'check shipping status',
  'parameters': {'type': 'object',
                  'properties': {'order_id': {'type': 'string'}},
                  'required': ['order_id']}},
  {'name': 'create_refund',
  'description': 'execute refund',
  'parameters': {'type': 'object',
                  'properties': {'order_id': {'type': 'string'}, 'eligibility': {'type': 'string'}},
                  'required': ['order_id', 'eligibility']}}
]
'''