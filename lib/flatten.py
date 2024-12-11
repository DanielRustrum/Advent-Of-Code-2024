def flattenList(deep_list):
    result = []
    for value in deep_list:
        if type(value) == list:
            for item in value:
                result.append(item)
        else:
            result.append(value)
    return result