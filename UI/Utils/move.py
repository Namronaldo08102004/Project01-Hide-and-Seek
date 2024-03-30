def find_entity(mp: list, person: int = 3):
    """
    Find the entity in the map
    """
    ls = []
    for i in range(len(mp)):
        for j in range(len(mp[0])):
            if mp[i][j] == person:
                ls.append((i, j))
    return ls


def getDirection(start: tuple[int, int], goal: tuple[int, int]):
    diff = (goal[0] - start[0], goal[1] - start[1])

    if diff == (0, 0):  # ? If the start and the goal are the same
        return None
    elif diff == (0, 1):  # ? If the goal is to the right of the start
        return "r"
    elif diff == (0, -1):  # ? If the goal is to the left of the start
        return "l"
    elif diff == (1, 0):  # ? If the goal is below the start
        return "d"
    elif diff == (-1, 0):  # ? If the goal is above the start
        return "u"
    elif diff == (1, 1):  # ? If the goal is to the bottom right of the start
        return "br"
    elif diff == (1, -1):  # ? If the goal is to the bottom left of the start
        return "bl"
    elif diff == (-1, 1):  # ? If the goal is to the top right of the start
        return "tr"
    elif diff == (-1, -1):  # ? If the goal is to the top left of the start
        return "tl"


# 4: seeker observation, 7: hider observation
def recov_obser(mp: list, loc: list[tuple]):
    """
    Recover the map from the observation
    """
    for x, y in loc:
        if mp[x][y] == 4 or mp[x][y] == 7:
            mp[x][y] = 0
    return mp


def assign_obser(mp: list, loc: list[tuple], person: int = 3):
    """
    Assign the observation to the map
    """
    for x, y in loc:
        if mp[x][y] == 0:
            if person == 2:
                mp[x][y] = 7
            elif person == 3:
                mp[x][y] = 4
    return mp


def moveTiles(mp: list, mv: str = None, loc: tuple = (0, 0), person: int = 3) -> list[list[int]]:
    # u, d, l, r, tl, tr, bl, br
    if mv == None:
        return mp
    (
        x,
        y,
    ) = loc
    nx, ny = x, y
    if mv == "d" and x < len(mp) - 1:
        nx, ny = x + 1, y
    elif mv == "u" and x > 0:
        nx, ny = x - 1, y
    elif mv == "r" and y < len(mp[0]) - 1:
        nx, ny = x, y + 1
    elif mv == "l" and y > 0:
        nx, ny = x, y - 1
    elif mv == "bl" and x < len(mp) - 1 and y > 0:
        nx, ny = x + 1, y - 1
    elif mv == "br" and x < len(mp) - 1 and y < len(mp[0]) - 1:
        nx, ny = x + 1, y + 1
    elif mv == "tl" and x > 0 and y > 0:
        nx, ny = x - 1, y - 1
    elif mv == "tr" and x > 0 and y < len(mp[0]) - 1:
        nx, ny = x - 1, y + 1

    if person == 3 and mp[nx][ny] == 2:
        mp[nx][ny] = 0
    mp[x][y], mp[nx][ny] = mp[nx][ny], mp[x][y]
    return mp
