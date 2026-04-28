from planner.dto_to_entity import DTO_TO_ENTITY

def get_existing_entities(tool_results: list) -> set:
    entities = set()
    for r in tool_results:
        entity = DTO_TO_ENTITY.get(type(r))
        entities.add(entity)
    return entities


def plan_tools(
        target_entities: list[str],
        existing_entities: set,
        entity_to_deps: dict,
        entity_to_tools: dict
) -> list[str]:

    '''
    输入: target entities
    输出: 对应的 tools
    '''

    path = set()
    done = set()
    tools_needed = []
    tools_seen = set()

    def resolve(entity):
        # 0.1 检查是否: entity已有 (ie.在tool_results里)
        if entity in existing_entities:
            return

        # 0.2 检查是否: 已经检查过了
        if entity in done:
            return

        # 0.3 检查是否: 死循环
        if entity in path:
            raise Exception(f"cycle detected: {entity}")

        # 0.4 进入path
        path.add(entity)

        # 1. 先找前置依赖
        for dep in entity_to_deps.get(entity, []):
            resolve(dep) # 先搞依赖

        # 2. 再获取自己对应的tool
        tool_list = entity_to_tools.get(entity, [])
        if tool_list:
            t = tool_list[0] # 目前只加第1个tool. 未来选择策略(优先:缓存/本地DB/低延迟, 或LLM选)
            if t not in tools_needed:
                tools_needed.append(t)
                tools_seen.add(t)

        done.add(entity)
        path.remove(entity)


    # 🚀 主流程 (target_entities里的每个entity, 都需resolve (找dep 放到tool_results列表))
    for entity in target_entities:
        resolve(entity)

    return tools_needed


