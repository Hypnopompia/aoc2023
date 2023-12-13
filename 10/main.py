from enum import Enum
from termcolor import colored
import fullcontrol as fc

class Map:
    def __init__(self, pipeMap):
        self.start = None
        pipeMap = pipeMap.split('\n')
        self.map = []
        self.mapPolygon = []

        for y in range(len(pipeMap)):
            row = [*pipeMap[y]]
            self.map.append([])
            for x in range(len(row)):
                self.map[y].append(Pipe(x, y, row[x]))
                if self.map[y][x].type == PipeType.START:
                    self.start = self.map[y][x]
                    self.start.connected = True

    def isValidCoordinate(self, coordinate):
        x, y = coordinate

        if not y in range(len(self.map)):
            return False
        
        if not x in range(len(self.map[y])):
            return False
    
        return True

    def getPipe(self, coordinate):
        x, y = coordinate

        if not self.isValidCoordinate(coordinate):
            return None

        return self.map[y][x]

    def getStartConnections(self):
        neighbors = []

        for direction in [self.start.north(), self.start.south(), self.start.east(), self.start.west()]:
            pipe = self.getPipe(direction)
            if pipe is not None:
                if self.start.coordinates() in pipe.getEnds():
                    neighbors.append(pipe)

        return neighbors

    def findConnectedPipes(self):
        lastPipe = self.start
        self.mapPolygon.append(self.start.coordinates())
        currentPipe = self.getStartConnections()[0]
        while currentPipe != self.start:
            self.mapPolygon.append(currentPipe.coordinates())
            currentPipe.connected = True
            nextPipe = self.getPipe(currentPipe.getOutputCoordinatesFromInputCoordinates(lastPipe.coordinates()))
            lastPipe = currentPipe
            currentPipe = nextPipe

    def findStepCount(self):
        steps = 1
        connections = self.getStartConnections()

        pathA_lastPipe = self.start
        pathA_currentPipe = connections[0]
        
        pathB_lastPipe = self.start
        pathB_currentPipe = connections[1]

        while pathA_currentPipe != pathB_currentPipe:
            steps += 1

            pathA_nextPipe = self.getPipe(pathA_currentPipe.getOutputCoordinatesFromInputCoordinates(pathA_lastPipe.coordinates()))
            pathA_lastPipe = pathA_currentPipe
            pathA_currentPipe = pathA_nextPipe

            pathB_nextPipe = self.getPipe(pathB_currentPipe.getOutputCoordinatesFromInputCoordinates(pathB_lastPipe.coordinates()))
            pathB_lastPipe = pathB_currentPipe
            pathB_currentPipe = pathB_nextPipe

        pathA_currentPipe.lastPoint = True

        return steps

    def tileIsInside(self, coordinates):
        # Uses raycasting method to determine if a point is inside a polygon (our pipe loop)
        # https://www.youtube.com/watch?v=l_UlG-oVxus

        intersections = 0
        x, y = coordinates

        for i in range(len(self.mapPolygon) - 1):
            x1, y1 = self.mapPolygon[i]
            x2, y2 = self.mapPolygon[i+1]

            if (y < y1) != (y < y2) and \
            x < (x2-x1)*(y-y1)/(y2-y1)+x1:
                intersections += 1

        return intersections % 2 == 1

    def findInsideTiles(self):
        insideTiles = 0
        for row in self.map:
            for pipe in row:
                if not pipe.connected:
                    pipe.inside = self.tileIsInside(pipe.coordinates())
                    if pipe.inside:
                        insideTiles += 1
        return insideTiles
                    
    def printPipeMap(self):
        for row in self.map:
            for pipe in row:
                print(pipe, end='')
            print()

    def savePipeGcode(self):
        x_offset = 20
        y_offset = 20
        scale = 1.5
        layers = 25

        filename = 'pipe_map'
        printer = 'ender_3'
        print_settings = {'extrusion_width': 0.5,'extrusion_height': 0.2, 'nozzle_temp': 210, 'bed_temp': 60, 'fan_percent': 100}



        startPoint = fc.Point(x=(self.mapPolygon[0][0]*scale)+x_offset, y=(self.mapPolygon[0][1]*scale)+y_offset, z=0.2)

        steps = []
        # steps.append(fc.ManualGcode(text="START_PRINT BED_TEMP=60 EXTRUDER_TEMP=210"))
        # steps.append(fc.Extruder(on=False))
        # steps.append(startPoint)

        for i in range(layers):
            steps.append(fc.Extruder(on=True))
            steps.extend([fc.Point(x=(point[0]*scale)+x_offset, y=(point[1]*scale)+y_offset, z=(i+1)*0.2) for point in self.mapPolygon])
            steps.append(startPoint)

        steps.append(fc.Extruder(on=False))

        steps.append(fc.ManualGcode(text="END_PRINT"))

        # fc.transform(steps, 'plot')

        fc.transform(steps, 'gcode', fc.GcodeControls(printer_name=printer, save_as=filename, initialization_data=print_settings))

class PipeType(Enum):
    NS = 1
    EW = 2
    NE = 3
    NW = 4
    SW = 5
    SE = 6
    GROUND = 7
    START = 8

class Pipe:
    def __init__(self, x, y, symbol):
        self.symbolTypeMap = {
            '|': PipeType.NS,
            '-': PipeType.EW,
            'L': PipeType.NE,
            'J': PipeType.NW,
            '7': PipeType.SW,
            'F': PipeType.SE,
            '.': PipeType.GROUND,
            'S': PipeType.START,
        }
        
        self.typeToASCII = {
            PipeType.NS: '│',
            PipeType.EW: '─',
            PipeType.NE: '└',
            PipeType.NW: '┘',
            PipeType.SW: '┐',
            PipeType.SE: '┌',
            PipeType.GROUND: ' ',
            PipeType.START: 'X',
        }

        self.x = x
        self.y = y
        self.symbol = symbol
        self.type = self.symbolTypeMap[symbol]
        self.connected = False
        self.inside = None
        self.lastPoint = False

    def coordinates(self):
        return self.x, self.y

    def north(self):
        return self.x, self.y-1,

    def south(self):
        return self.x, self.y+1,

    def east(self):
        return self.x+1, self.y,

    def west(self):
        return self.x-1, self.y,

    def getEnds(self):
        match self.type:
            case PipeType.NS:
                return [self.north(), self.south()]
            case PipeType.EW:
                return [self.east(), self.west()]
            case PipeType.NE:
                return [self.north(), self.east()]
            case PipeType.NW:
                return [self.north(), self.west()]
            case PipeType.SW:
                return [self.south(), self.west()]
            case PipeType.SE:
                return [self.south(), self.east()]
            case PipeType.GROUND:
                return []
                        
    def getOutputCoordinatesFromInputCoordinates(self, input):
        ends = self.getEnds()
        ends.remove(input)
        return ends[0]

    def __str__(self):
        char = self.typeToASCII[self.type]
        color = 'dark_grey'

        if self.type == PipeType.START:
            return colored(char, 'black', 'on_red')

        if self.connected:
            color = 'white'

        if self.lastPoint:
            return colored("E", 'black', 'on_red')

        if self.inside is not None:
            if self.inside:
                return colored('I', 'black', 'on_blue')
            else:
                return ' '
            
        return colored(char, color)


with open("input.txt") as file:
    pipeMap = Map(file.read().strip())
    
pipeMap.findConnectedPipes()
steps = pipeMap.findStepCount()
insideTiles = pipeMap.findInsideTiles()
pipeMap.printPipeMap()
pipeMap.savePipeGcode()
print(f"Steps: {steps}")
print(f"Inside Tiles: {insideTiles}")