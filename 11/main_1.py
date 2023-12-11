def rotateRight(universe):
    return list(zip(*universe[::-1]))

def rotateLeft(universe):
    return list(zip(*universe))[::-1]

def expandUniverse(universe):
    universeExpanded = []
    for row in universe:
        universeExpanded.append(row)
        if '#' not in row:
            universeExpanded.append(row)
    return universeExpanded

def galaxies(universe):
    galaxies = []
    for y, row in enumerate(universe):
        for x, point in enumerate(row):
            if point == '#':
                galaxies.append((x,y))
    return galaxies

def distance(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def distances(galaxies):
    distances = []
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            distances.append(distance(galaxies[i], galaxies[j]))
    return distances

def printUniverse(universe):
    for row in universe:
        for point in row:
            print(point, end='')
        print()
    print()

with open("input.txt", "r", encoding="utf-8") as file:
    universe = []
    for line in file:
        universe.append([*line.strip()])

universeExpanded = rotateLeft(expandUniverse(rotateRight(expandUniverse(universe))))
distanceSum = sum(distances(galaxies(universeExpanded)))
print(f"Distance Sum: {distanceSum}")