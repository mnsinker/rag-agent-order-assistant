def get_intent(query: str):
    mapping = { # "intent" <-> 'query keywords'
        'refund': ['退', '退款', '不想要'],
        'shipping': ['发货', '到哪了', '快递']
    }

    for intent, keywords in mapping.items():
        # 挨个比较每个keyword 是否在query里出现过, 如任一一个匹配 则返回intent
        if any(w in query for w in keywords):
            return intent
    return None


