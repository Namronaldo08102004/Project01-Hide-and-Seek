import os


def list_map(path: str) -> list[str]:
    """
    List all the maps in the given path
    """
    maps = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            maps.append(file)
    return maps


def read_map(path: str) -> list[list[int]]:
    """
    Read the map from the given path
    """
    maps = []
    obs = []
    row, col = 0, 0
    with open(path, "r") as file:
        # Get the number of rows and columns
        row, col = file.readline().split()
        row, col = int(row), int(col)
        if row <= 0 or col <= 0:
            raise ValueError("The number of rows and columns should be positive")

        # Read the map positioning
        for _ in range(row):
            maps.append(list(file.readline().split()))
        # Read the obstacles
        while (line := file.readline()) != "":
            obs.append(list(line.split()))
            if len(obs[-1]) != 4:
                raise Exception("Obstacles should have 4 arguments")

    # Convert to int
    for i in range(row):
        for j in range(col):
            maps[i][j] = int(maps[i][j])
    for i in range(len(obs)):
        for j in range(4):
            obs[i][j] = int(obs[i][j])

    # Placing the obstacles
    for o in obs:
        for i in range(o[0] - 1, o[2]):
            for j in range(o[1] - 1, o[3]):
                if i >= row or j >= col:
                    raise Exception("Obstacles should be placed within the map")
                if maps[i][j] != 0:
                    raise Exception("Obstacle should be placed at empty cells")
                maps[i][j] = 5

    return maps
