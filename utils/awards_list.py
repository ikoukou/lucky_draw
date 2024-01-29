def get_awards_list(tup: tuple):
    li = []
    for t in tup:
        key = t["id"]
        for value in range(len(t["awards_list"])):
            name = f"target_{key}-{value}"
            li.append(name)
    return li


def get_awards_total(dic: dict):
    total = 0
    for i in dic:
        total += i["count"]
    return total


def get_index(name: str):
    result = name.split('-')
    return int(result[0][-1]), int(result[1])
