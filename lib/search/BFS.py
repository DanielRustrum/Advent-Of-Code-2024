from collections import deque
def breadthFirstSearch(
        start, 
        fetch,
        target = lambda node: False,
        compute = lambda node: None,
        condition = lambda node, adjacant: True    
):
    queue = deque()
    tracker = {}
    tracker[start] = None

    queue.append(start)

    while queue:
        current_node = queue.popleft()

        if target(current_node):
            return [current_node, tracker]

        fetched = fetch(current_node)
        compute(current_node, fetched)

        for adjacant in fetched:
            if adjacant not in tracker and condition(current_node, adjacant):
                tracker[adjacant] = current_node
                queue.append(adjacant)

    return [None, tracker]