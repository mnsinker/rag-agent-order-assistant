from domain.nodes.risk import RiskResult
from planner.graph_registry import get_graph
from planner.planner import plan_tools


def test_plan():
    node_to_deps, node_to_tools = get_graph()
    tools = plan_tools(target_nodes=[RiskResult], existing_nodes=set(), node_to_deps=node_to_deps, node_to_tools=node_to_tools)
    print(f'tools: {tools}')
    assert tools == ['get_order', 'get_user', 'get_user_credit', 'risk_check']