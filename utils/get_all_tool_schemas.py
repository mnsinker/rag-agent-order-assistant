from tools.registry import tools
def get_all_tool_schemas() -> list:
    tool_schemas = []

    for _, tool in tools.items():
        schema = tool.to_schema()
        tool_schemas.append(schema)
    return tool_schemas



'''
response = 
[
  tool1_schema,
  tool2_schema
]
'''