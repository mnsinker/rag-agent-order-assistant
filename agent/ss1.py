# 初始化两个一模一样的字典
data_for_setdefault = {}
data_for_get = {}

entity = "Order"
tool = "get_order"


# setdefault 会返回列表，且如果键不存在，会把先列表存入字典
data_for_setdefault.setdefault(entity, []).append(tool)
print("--- 实验 A: 使用 setdefault ---")
print(f"字典现在变成了: {data_for_setdefault}")



# get 虽然也会返回列表，但如果键不存在，它返回的那个 [] 是临时的，没存进字典
data_for_get.get(entity, []).append(tool)
print("\n--- 实验 B: 使用 get ---")
print(f"字典现在变成了: {data_for_get}")
