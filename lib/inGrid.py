def inGrid(grid, position):
    x, y = position
    
    return (
        0 <= x < len(grid[0]) and
        0 <= y < len(grid)
    )