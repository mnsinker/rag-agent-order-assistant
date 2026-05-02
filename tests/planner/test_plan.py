from domain.entities.risk import Risk
from planner.graph_registry import get_graph
from planner.planner import plan_tools


def test_plan():
    entity_to_deps, entity_to_tools = get_graph()
    tools = plan_tools(target_entities=[Risk], existing_entities=set(), entity_to_deps=entity_to_deps, entity_to_tools=entity_to_tools)
    print(f'tools: {tools}')
    assert tools == ['get_order', 'get_user', 'get_user_credit', 'risk_check']