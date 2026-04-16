def find_path(source: str, target: str, relations: list):
    for r in relations:
        if r.source == source and r.target == target:
            return r

    return None