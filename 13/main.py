from icecream import ic
from termcolor import colored

class Pattern:
    def __init__(self, pattern):
        self.pattern = pattern
        self.orientation = None
        self.mirrorCenter = None
        self.range = None

    def printPattern(self):
        print(f"Orientation: {self.orientation}")
        print(f"Center: {self.mirrorCenter}")
        print(f"Range: {self.range}")
        print()

        for y in range(self.height()):
            if self.orientation == 'h':
                if (self.mirrorCenter - self.range) <= y < (self.mirrorCenter + self.range):
                    inRange = True
                else:
                    inRange = False
                if y == self.mirrorCenter:
                    print(colored(''.ljust(self.width(), '-'), 'red'))

            for x in range(self.width()):
                if self.orientation == 'v':
                    if (self.mirrorCenter - self.range) <= x and x < (self.mirrorCenter + self.range):
                        inRange = True
                    else:
                        inRange = False
                
                    if x == self.mirrorCenter:
                        print(colored('|', 'red'), end='')

                if self.pattern[y][x] == '1':
                    if inRange:
                        print(colored('#', 'white'), end='')
                    else:
                        print(colored('#', 'grey'), end='')
                else:
                    print(' ', end='')
            print()
        print()

    def width(self):
        return len(self.pattern[0])
    
    def height(self):
        return len(self.pattern)

    def col(self, x):
        return [self.pattern[y][x] for y in range(len(self.pattern))]

    def colId(self, x):
        return int(''.join(self.col(x)), 2)

    def row(self, y):
        return self.pattern[y]

    def rowId(self, y):
        return int(''.join(self.row(y)), 2)

    def isMirrored(self, orientation, center, r):
        for offset in range(r):
            aOffset = center - offset
            bOffset = center + offset + 1

            if orientation == 'v':
                a = self.colId(aOffset)
                b = self.colId(bOffset)
            else:
                a = self.rowId(aOffset)
                b = self.rowId(bOffset)

            if a != b:
                return False

        return True


    def findMirror(self):
        for y in range(self.height()-1):
            if self.rowId(y) == self.rowId(y+1):
                r = min(self.height() - y - 1, y + 1)
                if self.isMirrored('h', y, r):
                    self.orientation = 'h'
                    self.mirrorCenter = y + 1
                    self.range = r

        for x in range(self.width()-1):
            if self.colId(x) == self.colId(x+1):
                r = min(self.width() - x - 1, x + 1)
                if self.isMirrored('v', x, r):
                    self.orientation = 'v'
                    self.mirrorCenter = x + 1
                    self.range = r

    def findMirrorValue(self):
        self.findMirror()
        return self.mirrorCenter if self.orientation == 'v' else self.mirrorCenter * 100
    

with open("input.txt", "r", encoding="utf-8") as file:
    totals = 0
    chunk = []
    for line in file:
        line = line.strip().replace(".", "0").replace("#", "1")
        if len(line) > 0:
            chunk.append([*line])
        else:
            pattern = Pattern(chunk)
            chunk = []
            total = pattern.findMirrorValue()
            pattern.printPattern()
            print(f"Total: {total}")
            print()
            print()
            totals += total

    print(f"Totals: {totals}")