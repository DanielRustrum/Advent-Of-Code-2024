from pprint import pprint
from alive_progress import alive_bar
from lib.getInput import getInput
import uuid

# Generate a random UUID (version 4)

id_order_of_creation = []

def printBlock(block):
    new_block = []
    for char in block:
        if char == ".":
            new_block.append(char)
        else:
            new_block.append(getIdEquivalent(char))
            
    with open("d9.log", "w+") as file:
        file.write(str(new_block))

def getNextId():
    my_uuid = uuid.uuid4() 
    id_order_of_creation.append(my_uuid)

    return my_uuid

def getIdEquivalent(id):
    id_index = id_order_of_creation.index(id)
    return id_index

def expandDisk(disk):
    id = getNextId()
    use_id = True
    block = []
    for number in disk:
        if use_id:
            for _ in range(int(number)):
                block.append(id)
            id = getNextId()
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
    return block[next_space:].count('.') == len(block[next_space:])

def fillGaps(block):
    filled_block = block
    with alive_bar(len(block)) as bar:
        for index in range(len(block)):
            bar()
            if "." not in block:
                break

            char_index = len(block) - 1 - index
            next_space = filled_block.index(".")

            if gapsFilled(filled_block, next_space):
                break
            else:
                filled_block = swapChar(filled_block, char_index, next_space)
    return filled_block

def checksumBlock(block):
    result = 0
    for index, id in enumerate(block):
        if id == ".":
            break
        result += index * getIdEquivalent(id)
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
    print("ExpandingDisk...")
    block = expandDisk(disk)
    printBlock(block)
    print("Filling...", len(block))
    filled = fillGaps(block)
    printBlock(filled)
    print("Doing CheckSum...")
    result = checksumBlock(filled)
    print("Done!")
    return result


# disk = getInput(9)[0]
disk = ["1010101010101010101010"][0]
print( Q1(disk) )