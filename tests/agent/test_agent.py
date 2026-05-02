from agent.agent import agent

def test_agent_refund():
    result = agent("订单123能退款吗")
    print(f"result: {result}")
    assert result["success"] is True


def test_agent_risk():
    result = agent("帮我判断订单123有无风险")
    print(f"result: {result}")
    assert result["success"] is True






