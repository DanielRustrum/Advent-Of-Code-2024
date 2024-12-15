from .inGrid import inGrid

def getAdjacent(grid, position, condition = lambda position: True):
    x, y = position
    
    adjacent = []
    directions = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    ]

    for direction in directions:
        if inGrid(grid, direction) and condition(position):
            adjacent.append(direction)

    return adjacent