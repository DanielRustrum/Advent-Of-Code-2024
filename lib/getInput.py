def getInput(day):
    contents = []
    with open(f"inputs/d{day}.txt", "r+") as input_file:
        contents = input_file.readlines()
    return contents