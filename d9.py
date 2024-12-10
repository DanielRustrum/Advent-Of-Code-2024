from pprint import pprint
from alive_progress import alive_bar
from lib.getInput import getInput

def printBlock(block):
    new_block = []
    for char in block:
        new_block.append(char)

def getNextId(id):
    return id + 1

def expandDisk(disk):
    id = 0
    use_id = True
    block = []
    for number in disk:
        if use_id:
            for _ in range(int(number)):
                block.append(id)
            id = getNextId(id)
            use_id = False
        else:
            for _ in range(int(number)):
                block.append(".")
            use_id = True

    return block

def swapChar(swap, index1, index2):
    new_list = swap.copy()
    new_list[index1], new_list[index2] = new_list[index2], new_list[index1]
    return new_list

def gapsFilled(block, next_space):
    # This sucks at performance; too lazy too fix
    return block[next_space:].count('.') == len(block[next_space:])

def fillGaps(block):
    filled_block = block
    for index in range(len(block)):
        if "." not in block:
            break

        char_index = len(block) - 1 - index
        next_space = filled_block.index(".")

        if gapsFilled(filled_block, next_space):
            break
        else:
            filled_block = swapChar(filled_block, char_index, next_space)
    return filled_block

def fillGapWithChunks(block):
    right_index = len(block) - 1
    
    while True:
        id = None
        data_chunk = []
        space_chunk = []

        # Get next Data Chunk  
        while right_index >= 0:
            char = block[right_index]
            if char != '.' and (id == None or id == char):
                id = char
                data_chunk.append(right_index)
                right_index -= 1
            elif char == '.' and len(data_chunk) == 0:
                right_index -= 1
            else:
                break

        # Find Available Space for data chunk
        left_index = 0
        while left_index <= right_index:
            char = block[left_index]
            if char == '.':
                space_chunk.append(left_index)
                if len(space_chunk) == len(data_chunk):
                    # Get a list of needed spaces and swap them (paired) i.e. [(41, 2), (40, 3)]
                    for right_char_index, left_char_index in zip(data_chunk, space_chunk):
                        block = swapChar(
                            block, 
                            right_char_index, 
                            left_char_index
                        )
                    break
            else:
                space_chunk = []
            left_index += 1

        if right_index < 0:
            break

    return block

def checksumBlock(block):
    result = 0
    for index, id in enumerate(block):
        if id == ".":
            continue
        result += index * id
    return result

def Q1(disk):
    '''He shows you the disk map (your puzzle input) he's already generated. For example:

    2333133121414131402
    The disk map uses a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.

    So, a disk map like 12345 would represent a one-block file, two blocks of free space, a three-block file, four blocks of free space, and then a five-block file. A disk map like 90909 would represent three nine-block files in a row (with no free space between them).

    Each file on disk also has an ID number based on the order of the files as they appear before they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. Using one character for each block where digits are the file ID and . is free space, the disk map 12345 represents these individual blocks:

    0..111....22222
    The first example above, 2333133121414131402, represents these individual blocks:

    00...111...2...333.44.5555.6666.777.888899
    The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file blocks). For the disk map 12345, the process looks like this:

    0..111....22222
    02.111....2222.
    022111....222..
    0221112...22...
    02211122..2....
    022111222......
    The first example requires a few more steps:

    00...111...2...333.44.5555.6666.777.888899
    009..111...2...333.44.5555.6666.777.88889.
    0099.111...2...333.44.5555.6666.777.8888..
    00998111...2...333.44.5555.6666.777.888...
    009981118..2...333.44.5555.6666.777.88....
    0099811188.2...333.44.5555.6666.777.8.....
    009981118882...333.44.5555.6666.777.......
    0099811188827..333.44.5555.6666.77........
    00998111888277.333.44.5555.6666.7.........
    009981118882777333.44.5555.6666...........
    009981118882777333644.5555.666............
    00998111888277733364465555.66.............
    0099811188827773336446555566..............
    The final step of this file-compacting process is to update the filesystem checksum. To calculate the checksum, add up the result of multiplying each of these blocks' position with the file ID number it contains. The leftmost block is in position 0. If a block contains free space, skip it instead.

    Continuing the first example, the first few blocks' position multiplied by its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 1928.

    Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum? (Be careful copy/pasting the input for this puzzle; it is a single, very long line.)
    '''
    block = expandDisk(disk)
    filled = fillGaps(block)
    result = checksumBlock(filled)
    return result

def Q2(disk):
    '''
    The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

    This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

    The first example from above now proceeds differently:

    00...111...2...333.44.5555.6666.777.888899
    0099.111...2...333.44.5555.6666.777.8888..
    0099.1117772...333.44.5555.6666.....8888..
    0099.111777244.333....5555.6666.....8888..
    00992111777.44.333....5555.6666.....8888..
    The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

    Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?
    '''
    block = expandDisk(disk)
    filled = fillGapWithChunks(block)
    result = checksumBlock(filled)
    return result

disk = getInput(9)[0]
print( Q1(disk) )
print( Q2(disk) )