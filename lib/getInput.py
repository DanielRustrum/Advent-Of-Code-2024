def getInput(day):
    contents = []
    with open(f"inputs/d{day}.txt", "r+") as input_file:
        contents = input_file.readlines()
        file = []
        for line in contents:
            file.append( line.replace("\n", "") )
    return file