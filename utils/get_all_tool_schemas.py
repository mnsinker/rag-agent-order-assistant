from tools.registry import tools
def get_all_tool_schemas():
    collector_list = []

    for _, tool in tools.items():
        res = tool.to_schema()
        collector_list.append(res)
    return collector_list

list1 = get_all_tool_schemas()
print('list1', list1)

'''
response = 
[
  tool1_schema,
  tool2_schema
]
'''