from UI.Configs.config import *


def find_entity(mp: list[list[int]], person: int = 3) -> list[tuple[int, int]]:
    """
    Find the entity in the map
    """
    ls = []
    for i in range(len(mp)):
        for j in range(len(mp[0])):
            if mp[i][j] == person:
                ls.append((i, j))
    return ls


def getDirection(start: tuple[int, int], goal: tuple[int, int]) -> str:
    """
    Get the direction from the start to the goal
    Args:
        start (tuple[int, int]): starting position
        goal (tuple[int, int]): destination

    Returns:
        str: The moved direction
    """
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


# 4: seeker observation, 7: hider observation, 8: overlap observation
def recov_obser(mp: list[list[int]], loc: list[tuple]) -> list[list[int]]:
    """
    Recover the map from the observation
    """
    for x, y in loc:
        if mp[x][y] == 4 or mp[x][y] == 7 or mp[x][y] == 8:
            mp[x][y] = 0
    return mp


def assign_obser(
    mp: list[list[int]], loc: list[tuple], person: int = 3
) -> list[list[int]]:
    """
    Assign the observation to the map
    """
    for x, y in loc:
        if person == SEEKER and mp[x][y] == H_OBSERVABLE:
            mp[x][y] = OVERLAP
        elif person == HIDER and mp[x][y] == OBSERVABLE:
            mp[x][y] = OVERLAP
        if mp[x][y] == 0:
            if person == HIDER:
                mp[x][y] = H_OBSERVABLE
            elif person == SEEKER:
                mp[x][y] = OBSERVABLE
    return mp


def moveTiles(
    mp: list[list[int]], mv: str = None, loc: tuple[int, int] = (0, 0), person: int = 3
) -> list[list[int]]:
    """
    Move the seeker/hider following the given direction
    Args:
        mp (list[list[int]]): current map
        mv (str, optional): Direction. Defaults to None.
        loc (tuple[int, int], optional): Current location.
        person (int, optional): Hider/Seeker. Defaults to Seeker.

    Returns:
        list[list[int]]: The updated map
    """
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

    # The seeker catches the hider(s)
    if person == SEEKER and mp[nx][ny] == HIDER:
        mp[nx][ny] = 0
    # Hiders' suicide
    if person == HIDER and mp[nx][ny] == SEEKER:
        mp[x][y] = 0
        return mp
    # Swap
    mp[x][y], mp[nx][ny] = mp[nx][ny], mp[x][y]
    # mp[nx][ny] = person
    return mp


def setSeeker(mp: list[list[int]], loc: tuple[int, int]) -> list[list[int]]:
    """
    Set the seeker in the map
    """
    for x in range(len(mp)):
        for y in range(len(mp[0])):
            if mp[x][y] == SEEKER:
                mp[x][y] = 0
            # Delete old observation
            elif mp[x][y] == OBSERVABLE or mp[x][y] == OVERLAP:
                mp[x][y] = 0
    x, y = loc
    mp[x][y] = SEEKER # Placing
    return mp


def setHiders(mp: list[list[int]], loc: list[tuple[int, int]]) -> list[list[int]]:
    """
    Set the hiders in the map
    """
    for x in range(len(mp)):
        for y in range(len(mp[0])):
            if mp[x][y] == HIDER:
                mp[x][y] = 0
            # Del old observation
            elif mp[x][y] == H_OBSERVABLE or mp[x][y] == OVERLAP:
                mp[x][y] = 0
            # Del old annoucement
            elif mp[x][y] == ANNOUNCE:
                mp[x][y] = 0
    for x, y in loc:
        mp[x][y] = HIDER # Placing
    return mp
