def col(universe, x):
    return [universe[y][x] for y in range(len(universe))]

def row(universe, y):
    return universe[y]

def emptyCols(universe):
    emptyCols = []
    for x in range(len(universe[0])):
        if '#' not in col(universe, x):
            emptyCols.append(x)
    return emptyCols

def emptyRows(universe):
    emptyRows = []
    for y in range(len(universe)):
        if '#' not in row(universe, y):
            emptyRows.append(y)
    return emptyRows

def galaxies(universe, emptyCols, emptyRows, expandFactor):
    galaxies = []
    for y, row in enumerate(universe):
        previousEmptyRows = len([i for i in emptyRows if i < y])
        for x, point in enumerate(row):
            previousEmptyCols = len([i for i in emptyCols if i < x])
            if point == '#':
                galaxy_x = x + (previousEmptyCols * expandFactor) - previousEmptyCols
                galaxy_y = y + (previousEmptyRows * expandFactor) - previousEmptyRows
                galaxies.append((galaxy_x, galaxy_y))
    return galaxies

def distance(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def distances(galaxies):
    distances = []
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            distances.append(distance(galaxies[i], galaxies[j]))
    return distances

with open("input.txt", "r", encoding="utf-8") as file:
    universe = []
    for line in file:
        universe.append([*line.strip()])

expandFactor = 2
day1Galaxies = galaxies(universe, emptyCols(universe), emptyRows(universe), expandFactor)
distanceSum = sum(distances(day1Galaxies))
print(f"Distance Sum Part 1: {distanceSum}")

expandFactor = 1000000
day2Galaxies = galaxies(universe, emptyCols(universe), emptyRows(universe), expandFactor)
distanceSum = sum(distances(day2Galaxies))
print(f"Distance Sum Part 2: {distanceSum}")