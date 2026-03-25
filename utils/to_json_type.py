def to_json_type(py_type):
    mapping = {
        str: 'string',
        int: 'integer',
        float: 'number',
        bool: 'boolean',
        list: 'array',
        dict: 'object',
    }
    return mapping.get(py_type, 'string')


