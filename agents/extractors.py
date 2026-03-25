import regex as re

def extract_order_id(query: str) -> str | None:
    match = re.search(r'\d{3,10}', query)
    return match.group() if match else None


extractors = {
    'order_id': extract_order_id
}


