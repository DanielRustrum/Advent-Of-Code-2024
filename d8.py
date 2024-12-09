from pprint import pprint
from lib.getInput import getInput
from copy import deepcopy as copy

def parseFrequencyMap(map):
    freq_map = {}

    for row, line in enumerate(map):
        for col, char in enumerate(line):
            if char != ".":
                if char not in freq_map:
                    freq_map[char] = set()
                freq_map[char].add((row, col))
    
    return freq_map

def inBound(location, h_bound, v_bound):
    return (
        location[0] >= 0 and
        location[1] >= 0 and
        location[0] < v_bound and
        location[1] < h_bound
    )

def getNodeSlope(location_a, location_b):
    dif_row = location_a[0] - location_b[0]
    dif_col = location_a[1] - location_b[1]

    return (dif_row, dif_col)

def getAntiNodes(
        locations,
        location_a, 
        location_b,
        base_slope,
        slope, 
        h_bound, 
        v_bound, 
        check_resonance
):
    possible_locations = set()

    lower_a_row = location_a[0] - slope[0] 
    lower_b_row = location_b[0] - slope[0]  
    upper_a_row = location_a[0] + slope[0]  
    upper_b_row = location_b[0] + slope[0]  

    lower_a_col = location_a[1] - slope[1] 
    lower_b_col = location_b[1] - slope[1] 
    upper_a_col = location_a[1] + slope[1] 
    upper_b_col = location_b[1] + slope[1] 

    lower_a = (lower_a_row, lower_a_col)
    lower_b = (lower_b_row, lower_b_col)
    upper_a = (upper_a_row, upper_a_col)
    upper_b = (upper_b_row, upper_b_col)

    if (check_resonance or lower_a not in locations) and inBound(lower_a, v_bound, h_bound):
        possible_locations.add(lower_a)
    if (check_resonance or lower_b not in locations) and inBound(lower_b, v_bound, h_bound):
        possible_locations.add(lower_b)
    if (check_resonance or upper_a not in locations) and inBound(upper_a, v_bound, h_bound):
        possible_locations.add(upper_a)
    if (check_resonance or upper_b not in locations) and inBound(upper_b, v_bound, h_bound):
        possible_locations.add(upper_b)


    if check_resonance and (
        inBound(lower_a, v_bound, h_bound) or
        inBound(lower_b, v_bound, h_bound) or
        inBound(upper_a, v_bound, h_bound) or
        inBound(upper_b, v_bound, h_bound)
    ):
        return possible_locations | getAntiNodes(
            locations,
            location_a,
            location_b,
            base_slope,
            (slope[0] + base_slope[0], slope[1] + base_slope[1]),
            h_bound,
            v_bound,
            check_resonance
        )
    else:
        return possible_locations


def printMap(map, at):
    from copy import deepcopy as copy

    mod_map = copy(map)
    pprint(mod_map)

    for coord in at:

        if coord[1] < 0: 
            mod_map[coord[0]] = "#" + mod_map[coord[0]]
        if coord[1] > len(mod_map[coord[0]]): 
            mod_map[coord[0]] = mod_map[coord[0]] + "#"

        mod_map[coord[0]] = mod_map[coord[0]][:coord[1]] + "#" + mod_map[coord[0]][coord[1] + 1:]

    pprint(mod_map)

def checkFrequencies(map, h_bound, v_bound, check_resonance=False):
    possible_locations = set()
    for _, locations in map.items():
        locations = list(locations)
        for location_index_a in range(len(locations)):
            for location_index_b in range(len(locations)):
                if location_index_a == location_index_b:
                    continue

                location_a = locations[location_index_a]
                location_b = locations[location_index_b]

                slope = getNodeSlope(location_a, location_b)

                anti_locations = getAntiNodes(
                    locations,
                    location_a,
                    location_b,
                    slope,
                    slope,
                    h_bound,
                    v_bound,
                    check_resonance
                )

                possible_locations = possible_locations | anti_locations

    return possible_locations

    
def Q1(map):
    '''Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............
    The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

    So, for these two antennas with frequency a, they create the two antinodes marked with #:

    ..........
    ...#......
    ..........
    ....a.....
    ..........
    .....a....
    ..........
    ......#...
    ..........
    ..........
    Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

    ..........
    ...#......
    #.........
    ....a.....
    ........a.
    .....a....
    ..#.......
    ......#...
    ..........
    ..........
    Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

    ..........
    ...#......
    #.........
    ....a.....
    ........a.
    .....a....
    ..#.......
    ......A...
    ..........
    ..........
    The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

    ......#....#
    ...#....0...
    ....#0....#.
    ..#....0....
    ....0....#..
    .#....A.....
    ...#........
    #......#....
    ........A...
    .........A..
    ..........#.
    ..........#.
    Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

    Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?
    '''
    freq_map = parseFrequencyMap(map)
    possible = checkFrequencies(freq_map, len(map[0]), len(map))
    return len(possible)

def Q2(map):
    '''After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

    So, these three T-frequency antennas now create many antinodes:

    T....#....
    ...T......
    .T....#...
    .........#
    ..#.......
    ..........
    ...#......
    ..........
    ....#.....
    ..........
    In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

    The original example now has 34 antinodes, including the antinodes that appear on every antenna:

    ##....#....#
    .#.#....0...
    ..#.#0....#.
    ..##...0....
    ....0....#..
    .#...#A....#
    ...#..#.....
    #....#.#....
    ..#.....A...
    ....#....A..
    .#........#.
    ...#......##
    Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?
    '''
    freq_map = parseFrequencyMap(map)
    possible = checkFrequencies(freq_map, len(map[0]), len(map), True)
    printMap(map, possible)
    return len(possible)

map = getInput("8")
print( Q1(map) )
print( Q2(map) )