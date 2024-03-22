import os


def list_map(path: str):
    """
    List all the maps in the given path
    """
    maps = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            maps.append(file)
    return maps


def read_map(path: str):
    """
    Read the map from the given path
    """
    maps = []
    obs = []
    row, col = 0, 0
    with open(path, "r") as file:
        row, col = file.readline().split()
        row, col = int(row), int(col)

        for _ in range(row):
            maps.append(list(file.readline().split()))
        while (line := file.readline()) != "":
            obs.append(list(line.split()))

    # Convert to int
    for i in range(row):
        for j in range(col):
            maps[i][j] = int(maps[i][j])
    for i in range(len(obs)):
        for j in range(4):
            obs[i][j] = int(obs[i][j])

    # Placing the obstacles
    try:
        for o in obs:
            for i in range(o[0] - 1, o[2]):
                for j in range(o[1] - 1, o[3]):
                    maps[i][j] = 5
    except:
        pass

    return maps

