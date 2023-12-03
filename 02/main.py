class Game:
    def __init__(self, line):
        game = line.split(":")
        self.game_id = int(game[0].split(" ")[1])
        self.sets = self.parseSets(game[1])

    def parseSets(self, sets):
        sets = sets.split(";")
        for i in range(len(sets)):
            sets[i] = self.parseSet(sets[i].strip())
        return sets

    def parseSet(self, set):
        set = set.split(",")
        colors = {}
        for i in range(len(set)):
            colors.update(self.parseColor(set[i].strip()))
        return colors
    
    def parseColor(self, color):
        color = color.split(" ")
        return {
            color[1]: int(color[0])
        }
    
    def isPossible(self):
        for set in self.sets:
            if set.get('red', 0) > 12:
                return False
            if set.get('green', 0) > 13:
                return False
            if set.get('blue', 0) > 14:
                return False
        return True
    
    def power(self):
        red = 0
        green = 0
        blue = 0
        for set in self.sets:
            red = max(red, set.get('red', 0))
            green = max(green, set.get('green', 0))
            blue = max(blue, set.get('blue', 0))
        return red * green * blue


if __name__ == '__main__':
    file = open("input.txt", 'r')
    possibleSum = 0
    powerSum = 0
    while True:
        line = file.readline()
        if not line:
            break
        game = Game(line)
        
        if game.isPossible():
            possibleSum += game.game_id

        powerSum += game.power()

    print("Part 1 Answer: " + str(possibleSum))
    print("Part 2 Power: " + str(powerSum))