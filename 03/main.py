class Schematic:

    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.loadSchematic()

    def loadSchematic(self):
        self.schematic = []
        file = open(self.inputFile, 'r')
        while True:
            line = file.readline()
            if not line:
                break
            self.schematic.append(list(line.replace('\n','').replace('.', ' ')))

    def isSymbol(self, character):
        return not character.isnumeric() and not character == ' '

    def isGear(self, character):
        return character == '*'

    def findSymbols(self, onlyGears = False):
        symbols = []
        for y in range(len(self.schematic)):
            for x in (range(len(self.schematic[y]))):
                if (onlyGears and self.isGear(self.schematic[y][x])) or (not onlyGears and self.isSymbol(self.schematic[y][x])):
                    symbols.append({'x': x, 'y': y, 's': self.schematic[y][x]})
        return symbols

    def findPart(self, x, y):
        start = x
        end = x
        numberString = ''
        while start -1 >= 0 and self.schematic[y][start-1].isnumeric():
            start = start - 1
        while end +1 <= len(self.schematic[y]) and self.schematic[y][end].isnumeric():
            end = end + 1
        for i in range(start, end):
            numberString += self.schematic[y][i]

        # give each part a part_id so we can de-dupe them later
        return {
            'part_id': str(start) + ':' + str(y),
            'value': int(numberString)
        }
    
    def findAdjacentParts(self, symbol):
        x = symbol['x']
        y = symbol['y']
        adjacentParts = {}
        
        minY = max(0, y-1)
        maxY = min(len(self.schematic), y+1)
        minX = max(0, x-1)
        maxX = min(len(self.schematic[y]), x+1)

        # search for part numbers in adjacent areas
        for yIndex in range(minY, maxY+1):
            for xIndex in range(minX, maxX+1):
                if self.schematic[yIndex][xIndex].isnumeric():
                    # Found an adjactent part
                    part = self.findPart(xIndex, yIndex)
                    adjacentParts[part['part_id']] = {'s': symbol['s'], 'x': xIndex, 'y': yIndex, 'value': part['value']}
        return adjacentParts
            
    def findParts(self):
        allParts = {}
        symbols = self.findSymbols()
        for i in range(len(symbols)):
            symbol = symbols[i]
            parts = self.findAdjacentParts(symbol)
            allParts.update(parts)
        return allParts
    
    def findGears(self):
        allGears = {}
        onlyGears = True
        symbols = self.findSymbols(onlyGears)
        for i in range(len(symbols)):
            symbol = symbols[i]
            parts = self.findAdjacentParts(symbol)
            if len(parts) > 1:
                gear_id = str(symbol['x']) + ":" + str(symbol['y'])
                ratio = 1
                for part_id in parts:
                    ratio = ratio * parts[part_id]['value']
                allGears[gear_id] = {'x': symbol['x'], 'y': symbol['y'], 'ratio': ratio}
        return allGears
    
    def sumOfPartNumbers(self):
        sum = 0
        parts = self.findParts()
        for part_id in parts:
            sum = sum + parts[part_id]['value']
        return sum

    def sumOfGearRatios(self):
        sum = 0
        gears = self.findGears()
        for part_id in gears:
            sum = sum + gears[part_id]['ratio']
        return sum
    
    def printSchematic(self):
        print("Schematic:")
        for y in range(len(self.schematic)):
            print(self.schematic[y])
        print('')

    def printParts(self):
        print("Parts:")
        parts = self.findParts()
        for part_id in parts:
            print(" * " + part_id + ": " + str(parts[part_id]))
        print('')

    def printGears(self):
        print("Gears:")
        gears = self.findGears()
        for part_id in gears:
            print(" * " + part_id + ": " + str(gears[part_id]))
        print('')

    def printSumOfParts(self):
        print('Sum Of Parts: ' + str(self.sumOfPartNumbers()))

    def printSumOfGearRatios(self):
        print('Sum Of Gear Ratios: ' + str(self.sumOfGearRatios()))

schematic = Schematic('input.txt')
schematic.printSchematic()
schematic.printParts()
schematic.printGears()
schematic.printSumOfParts()
schematic.printSumOfGearRatios()
