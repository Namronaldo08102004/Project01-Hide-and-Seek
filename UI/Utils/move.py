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

def moveTiles(mp: list, mv: str = None, loc: tuple = (0, 0)) -> list[int]:
    # u, d, l, r, tl, tr, bl, br
    if mv == None:
        return mp
    x, y, = loc
    if mv == "d" and x < len(mp) - 1:
        mp[x][y], mp[x + 1][y] = mp[x + 1][y], mp[x][y]
    elif mv == "u" and x > 0:
        mp[x][y], mp[x - 1][y] = mp[x - 1][y], mp[x][y]
    elif mv == "r" and y < len(mp[0]) - 1:
        mp[x][y], mp[x][y + 1] = mp[x][y + 1], mp[x][y]
    elif mv == "l" and y > 0:
        mp[x][y], mp[x][y - 1] = mp[x][y - 1], mp[x][y]
    elif mv == "bl" and x < len(mp) - 1 and y > 0:
        mp[x][y], mp[x + 1][y - 1] = mp[x + 1][y - 1], mp[x][y]
    elif mv == "br" and x < len(mp) - 1 and y < len(mp[0]) - 1:
        mp[x][y], mp[x + 1][y + 1] = mp[x + 1][y + 1], mp[x][y]
    elif mv == "tl" and x > 0 and y > 0:
        mp[x][y], mp[x - 1][y - 1] = mp[x - 1][y - 1], mp[x][y]
    elif mv == "tr" and x > 0 and y < len(mp[0]) - 1:
        mp[x][y], mp[x - 1][y + 1] = mp[x - 1][y + 1], mp[x][y]
    return mp
    