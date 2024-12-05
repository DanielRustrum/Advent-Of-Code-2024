from lib.getInput import getInput
# URL: https://adventofcode.com/2024/day/4
    
def Q1(word_search):
    '''As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

    This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


    ..X...
    .SAMX.
    .A..A.
    XMAS.S
    .X....
    The actual word search will be full of letters instead. For example:

    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
    In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

    ....XXMAS.
    .SAMXMS...
    ...S..A...
    ..A.A.MS.X
    XMASAMX.MM
    X.....XA.A
    S.S.S.S.SS
    .A.A.A.A.A
    ..M.M.M.MM
    .X.X.XMASX
    Take a look at the little Elf's word search. How many times does XMAS appear?
    '''
    vertical_length = len(word_search)
    horizontal_length = len(word_search[0])

    #  Create Direction Vectors
    # (-1, -1)   (-1, 0)   (-1, 1)
    # (0, -1)               (0, 1)
    # (1, -1)    (1, 0)     (1, 1)
    directions = []
    for hori_direction in range(-1, 2):
        for verti_direction in range(-1, 2):
            if hori_direction != 0 or verti_direction != 0:
                directions.append((hori_direction, verti_direction))

    def has_xmas(verti_index, hori_index, direction):
        hori_direction, verti_direction = direction
        for xmas_character_index, character in enumerate("XMAS"):
            
            # gets the vertical index of the xmas character in relation to our current character
            verti_character_offset = verti_index + xmas_character_index * hori_direction
            hori_character_offset = hori_index + xmas_character_index * verti_direction
            
            # Check if out of bounds
            if not (
                0 <= verti_character_offset < vertical_length and 
                0 <= hori_character_offset < horizontal_length
            ):
                return False
            
            # Check if character offset is the character we expected
            if word_search[verti_character_offset][hori_character_offset] != character:
                return False
        return True

    # Count up every cell and every direction
    count = 0
    for verti_index in range(vertical_length):
        for hori_index in range(horizontal_length):
            for direction in directions:
                count += has_xmas(verti_index, hori_index, direction)
    
    return count

def Q2(word_search):
    ''''''
    vertical_length = len(word_search)
    horizontal_length = len(word_search[0])

    def has_xmas(verti_index, hori_index):
        # Check if out of bounds, Checking from the Letter A so the bound are stricker
        if not (
            1 <= verti_index < vertical_length - 1 and 
            1 <= hori_index < horizontal_length - 1
        ):
            return False

        # Check For Center Character
        if word_search[verti_index][hori_index] != "A":
            return False
        
        # Get Diagonals
        # 1 . 2
        # . A .
        # 2 . 1
        diagonal_1 = [ 
            word_search[verti_index-1][hori_index-1],
            word_search[verti_index+1][hori_index+1]
        ]
        diagonal_2 = [ 
            word_search[verti_index+1][hori_index-1],
            word_search[verti_index-1][hori_index+1]
        ]


        # Check if character offset is the character we expected
        return (
            diagonal_1 in [["M", "S"], ["S", "M"]] and
            diagonal_2 in [["M", "S"], ["S", "M"]]
        )

    # Count up every cell and every direction
    count = 0
    for verti_index in range(vertical_length):
        for hori_index in range(horizontal_length):
            count += has_xmas(verti_index, hori_index)
    
    return count

word_search = getInput("4")



print( Q1(word_search) )
print( Q2(word_search) )
