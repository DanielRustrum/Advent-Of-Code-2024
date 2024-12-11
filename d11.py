from lib.getInput import getInput
from copy import copy
from lib.flatten import flattenList
from functools import cache

NON_ZEROS = ["1","2","3","4","5","6","7","8","9"]

def noLeadingZeros(string):
    for index, char in enumerate(string):
        if char in NON_ZEROS:
            return string[index:]

        if index == len(string)-1:
            return char

def blink(stones):
    stone_copy = copy(stones)
    for stone_index in range(len(stones)):
        stone = stones[stone_index]
        
        # Rule 1
        if stone == "0":
            stone_copy[stone_index] = "1"
            continue

        # Rule 2
        if len(stone) % 2 == 0:
            middle_index = int(len(stone) / 2)
            left = noLeadingZeros(stones[stone_index][:middle_index])
            right = noLeadingZeros(stones[stone_index][middle_index:])

            stone_copy[stone_index] = [left, right]
            continue
        
        # Rule 3
        stone_copy[stone_index] = str(
            int(stone) * 2024
        )

    return flattenList(stone_copy)

def formatStones(stones):
    return [int(stone) for stone in stones]

# Same Issue as Computing Factorial Stores Results so you don't Compute the Same Computations
# Memoize Function
@cache
def blinkStone(stone, steps):

    # Reached End count stone
    if steps == 0:
        return 1

    # Rule 1 Stone Changes
    if stone == 0:
        return blinkStone(1, steps - 1)

    # Rule 2 Stone Splits
    stone_string = str(stone)
    length = len(stone_string)
    if length % 2 == 0:
        middle_index = length // 2
        left = int(stone_string[:middle_index])
        right = int(stone_string[middle_index:])

        return blinkStone(left, steps-1) + blinkStone(right, steps-1)
    
    # Rule 3
    return blinkStone(stone * 2024, steps - 1)


def Q1(stones):
    '''Sometimes, the number engraved on a stone changes. Other times, a stone might split in two, causing all the other stones to shift over a bit to make room in their perfectly straight line.

    As you observe them for a while, you find that the stones have a consistent behavior. Every time you blink, the stones each simultaneously change according to the first applicable rule in this list:

    If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
    No matter how the stones change, their order is preserved, and they stay on their perfectly straight line.

    How will the stones evolve if you keep blinking at them? You take a note of the number engraved on each stone in the line (your puzzle input).

    If you have an arrangement of five stones engraved with the numbers 0 1 10 99 999 and you blink once, the stones transform as follows:

    The first stone, 0, becomes a stone marked 1.
    The second stone, 1, is multiplied by 2024 to become 2024.
    The third stone, 10, is split into a stone marked 1 followed by a stone marked 0.
    The fourth stone, 99, is split into two stones marked 9.
    The fifth stone, 999, is replaced by a stone marked 2021976.
    So, after blinking once, your five stones would become an arrangement of seven stones engraved with the numbers 1 2024 1 0 9 9 2021976.

    Here is a longer example:

    Initial arrangement:
    125 17

    After 1 blink:
    253000 1 7

    After 2 blinks:
    253 0 2024 14168

    After 3 blinks:
    512072 1 20 24 28676032

    After 4 blinks:
    512 72 2024 2 0 2 4 2867 6032

    After 5 blinks:
    1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32

    After 6 blinks:
    2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2
    In this example, after blinking six times, you would have 22 stones. After blinking 25 times, you would have 55312 stones!

    Consider the arrangement of stones in front of you. How many stones will you have after blinking 25 times?
    '''
    stone_copy = copy(stones)
    for _ in range(25):
        stone_copy = blink(stone_copy)
    return len(stone_copy)

def Q2(stones):
    '''The Historians sure are taking a long time. To be fair, the infinite corridors are very large.

    How many stones would you have after blinking a total of 75 times?
    '''
    count = 0
    steps = 75
    
    for stone in formatStones(stones):
        count += blinkStone(stone, steps)
    return count

stones = getInput(11)[0].split(" ")
# stones =  "125 17".split(" ")
print( Q1(stones) )
print( Q2(stones) )
