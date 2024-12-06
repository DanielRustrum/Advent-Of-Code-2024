from pprint import pprint
from lib.getInput import getInput
from copy import deepcopy as copy
# URL: https://adventofcode.com/2024/day/6
class Map:
    def __init__(self, map, v_len, h_len):
        self.chart = map
        self.v_len = v_len
        self.h_len = h_len

def formatMap(map):
    new_map = []
    guard_position = (0, 0)
    for row, line in enumerate(map):
        new_map.append(list(line))
        if("^" in line):
            guard_position = (line.index("^"), row)

    return [
        Map(new_map, len(map), len(map[0])), 
        guard_position
    ]

def getMapToken(map, x, y):
    if x == -1 or x == map.h_len:
        return "!"
    if y == -1 or y == map.v_len:
        return "!"
    return map.chart[y][x]

def walk(map, direction, x, y, steps):
    if map.chart[y][x] != "x":
        new_step = steps + 1
        map.chart[y][x] = "x"
    else:
        new_step = steps

    if direction == "Up":
        y -= 1
    if direction == "Right":
        x += 1
    if direction == "Down":
        y += 1
    if direction == "Left":
        x -= 1


    return [x, y, new_step]

def traverseMap(map, start):
    steps = 0
    direction_facing = "Up"
    x, y = start
    failed_to_end = True

    for _ in range(20000):
        if direction_facing == "Up":
            next_token = getMapToken(map, x, y-1)
            if next_token == "#":
               direction_facing = "Right"
            if next_token in [".", "^", "x"]:
                x, y, steps = walk(map, direction_facing, x, y, steps)
            if next_token == "!":
                x, y, steps = walk(map, direction_facing, x, y, steps)
                failed_to_end = False
                break
        if direction_facing == "Right":
            next_token = getMapToken(map, x+1, y)
            if next_token == "#":
               direction_facing = "Down"
            if next_token in [".", "^", "x"]:
                x, y, steps = walk(map, direction_facing, x, y, steps)
            if next_token == "!":
                x, y, steps = walk(map, direction_facing, x, y, steps)
                failed_to_end = False
                break
        if direction_facing == "Down":
            next_token = getMapToken(map, x, y+1)
            if next_token == "#":
               direction_facing = "Left"
            if next_token in [".", "^", "x"]:
                x, y, steps = walk(map, direction_facing, x, y, steps)
            if next_token == "!":
                x, y, steps = walk(map, direction_facing, x, y, steps)
                failed_to_end = False
                break
        if direction_facing == "Left":
            next_token = getMapToken(map, x-1, y)
            if next_token == "#":
               direction_facing = "Up"
            if next_token in [".", "^", "x"]:
                x, y, steps = walk(map, direction_facing, x, y, steps)
            if next_token == "!":
                x, y, steps = walk(map, direction_facing, x, y, steps)
                failed_to_end = False
                break
    return [steps, failed_to_end]


def Q1(map):
    '''You start by making a map (your puzzle input) of the situation. For example:

    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
    The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

    Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

    If there is something directly in front of you, turn right 90 degrees.
    Otherwise, take a step forward.
    Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

    ....#.....
    ....^....#
    ..........
    ..#.......
    .......#..
    ..........
    .#........
    ........#.
    #.........
    ......#...
    Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

    ....#.....
    ........>#
    ..........
    ..#.......
    .......#..
    ..........
    .#........
    ........#.
    #.........
    ......#...
    Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#......v.
    ........#.
    #.........
    ......#...
    This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#........
    ........#.
    #.........
    ......#v..
    By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

    ....#.....
    ....XXXXX#
    ....X...X.
    ..#.X...X.
    ..XXXXX#X.
    ..X.X.X.X.
    .#XXXXXXX.
    .XXXXXXX#.
    #XXXXXXX..
    ......#X..
    In this example, the guard will visit 41 distinct positions on your map.

    Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?'''
    new_map, guard = formatMap(map)
    return traverseMap(new_map, guard)[0]

def Q2(map):
    '''While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

    Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

    Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

    To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

    In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

    Option one, put a printing press next to the guard's starting position:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ....|..#|.
    ....|...|.
    .#.O^---+.
    ........#.
    #.........
    ......#...
    Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:


    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    ......O.#.
    #.........
    ......#...
    Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    .+----+O#.
    #+----+...
    ......#...
    Option four, put an alchemical retroencabulator near the bottom left corner:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    ..|...|.#.
    #O+---+...
    ......#...
    Option five, put the alchemical retroencabulator a bit to the right instead:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    ....|.|.#.
    #..O+-+...
    ......#...
    Option six, put a tank of sovereign glue right next to the tank of universal solvent:

    ....#.....
    ....+---+#
    ....|...|.
    ..#.|...|.
    ..+-+-+#|.
    ..|.|.|.|.
    .#+-^-+-+.
    .+----++#.
    #+----++..
    ......#O..
    It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

    You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?
    '''
    formatted_map, guard = formatMap(map)
    result = 0
    for x in range(formatted_map.v_len):
        for y in range(formatted_map.h_len):
            print(x,y)
            if x == guard[0] and y == guard[1]:
                continue

            new_map = Map(copy(formatted_map.chart), formatted_map.v_len, formatted_map.h_len)
            new_map.chart[x][y] = "#"
            _, had_failed = traverseMap(new_map, guard)

            if had_failed:
                result += 1
    return result

map = getInput("6")
print( Q1(map))
print( Q2(map))