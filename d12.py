from lib.getInput import getInput
from lib.search.BFS import breadthFirstSearch
from lib.position import position
from lib.getPosition import getPosition
from lib.getAdjacent import getAdjacent

from queue import SimpleQueue
import time
from pprint import pprint

def findCorners(map, position, neighbours):
    pass

def findRegion(map, position, plots):
    max_plots = 4
    perimeter = 0

    regionalPlots = SimpleQueue()
    checked = set()
    plant = getPosition(map, position)

    regionalPlots.put(position)
    checked.add(position)

    def fetch(bfs_position):
        def isPlant(pos):
            nonlocal bfs_position
            return getPosition(map, pos) == getPosition(map, bfs_position)

        return getAdjacent(
            map, 
            position, 
            isPlant 
        )

    def compute(_, adjacent):
        nonlocal perimeter, max_plots
        perimeter += max_plots - len(adjacent)

    def condition(_, adjacent):
        return adjacent not in plots
    
    def target(position):
        nonlocal map, plant
        return getPosition(map, position) != plant
    

    [_, tracker] = breadthFirstSearch(
        position,
        fetch,
        compute = compute,
        condition = condition,
        target=target
    )

    visited = set([x for x in tracker.keys()])

    if len(visited) == 1 and position in plots:
        return [None, None]
    else:
        return [visited, perimeter]



def Q1(map):
    '''Each garden plot grows only a single type of plant and is indicated by a single letter on your map. When multiple garden plots are growing the same type of plant and are touching (horizontally or vertically), they form a region. For example:

    AAAA
    BBCD
    BBCC
    EEEC
    This 4x4 arrangement includes garden plots growing five different types of plants (labeled A, B, C, D, and E), each grouped into their own region.

    In order to accurately calculate the cost of the fence around a single region, you need to know that region's area and perimeter.

    The area of a region is simply the number of garden plots the region contains. The above map's type A, B, and C plants are each in a region of area 4. The type E plants are in a region of area 3; the type D plants are in a region of area 1.

    Each garden plot is a square and so has four sides. The perimeter of a region is the number of sides of garden plots in the region that do not touch another garden plot in the same region. The type A and C plants are each in a region with perimeter 10. The type B and E plants are each in a region with perimeter 8. The lone D plot forms its own region with perimeter 4.

    Visually indicating the sides of plots in each region that contribute to the perimeter using - and |, the above map's regions' perimeters are measured as follows:

    +-+-+-+-+
    |A A A A|
    +-+-+-+-+     +-+
                |D|
    +-+-+   +-+   +-+
    |B B|   |C|
    +   +   + +-+
    |B B|   |C C|
    +-+-+   +-+ +
            |C|
    +-+-+-+   +-+
    |E E E|
    +-+-+-+
    Plants of the same type can appear in multiple separate regions, and regions can even appear within other regions. For example:

    OOOOO
    OXOXO
    OOOOO
    OXOXO
    OOOOO
    The above map contains five regions, one containing all of the O garden plots, and the other four each containing a single X plot.

    The four X regions each have area 1 and perimeter 4. The region containing 21 type O plants is more complicated; in addition to its outer edge contributing a perimeter of 20, its boundary with each X region contributes an additional 4 to its perimeter, for a total perimeter of 36.

    Due to "modern" business practices, the price of fence required for a region is found by multiplying that region's area by its perimeter. The total price of fencing all regions on a map is found by adding together the price of fence for every region on the map.

    In the first example, region A has price 4 * 10 = 40, region B has price 4 * 8 = 32, region C has price 4 * 10 = 40, region D has price 1 * 4 = 4, and region E has price 3 * 8 = 24. So, the total price for the first example is 140.

    In the second example, the region with all of the O plants has price 21 * 36 = 756, and each of the four smaller X regions has price 1 * 4 = 4, for a total price of 772 (756 + 4 + 4 + 4 + 4).

    Here's a larger example:

    RRRRIICCFF
    RRRRIICCCF
    VVRRRCCFFF
    VVRCCCJFFF
    VVVVCJJCFE
    VVIVCCJJEE
    VVIIICJJEE
    MIIIIIJJEE
    MIIISIJEEE
    MMMISSJEEE
    It contains:

    A region of R plants with price 12 * 18 = 216.
    A region of I plants with price 4 * 8 = 32.
    A region of C plants with price 14 * 28 = 392.
    A region of F plants with price 10 * 18 = 180.
    A region of V plants with price 13 * 20 = 260.
    A region of J plants with price 11 * 20 = 220.
    A region of C plants with price 1 * 4 = 4.
    A region of E plants with price 13 * 18 = 234.
    A region of I plants with price 14 * 22 = 308.
    A region of M plants with price 5 * 12 = 60.
    A region of S plants with price 3 * 8 = 24.
    So, it has a total price of 1930.

    What is the total price of fencing all regions on your map?
    '''
    count = 0
    plots = set()
    plot_map = {}
    for y, row in enumerate(map):
        for x in range(len(row)):
            region, perimeter = findRegion(map, position(x, y), plots)
            if region:
                plant = getPosition(map, position(x, y))

                if plant in plot_map:
                    plot_map[plant] |= region
                else:
                    plot_map[plant] = region

                plots |= region
                count += len(region) * perimeter

    pprint(plot_map.keys())
    return count

map = getInput("12a")
print( Q1(map) )
