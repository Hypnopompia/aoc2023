from parse import *
import re

class Seeds:
    def __init__(self, seeds, categories):
        self.seeds = seeds
        self.categories = categories

    def getLowestSeedLocation(self):
        return min(self.getSeedLocations())

    def getSeedLocations(self):
        locations = []
        for seed in self.seeds:
            locations.append(self.getTargetValue(seed))
        return locations

    def getTargetValue(self, id, categoryName = 'seed'):
        category = self.categories[categoryName]
        result = category.resolve(id)
        
        if category.target == 'location':
            return result
        
        return self.getTargetValue(result, category.target)

class Category:
    def __init__(self, category, target):
        self.category = category
        self.target = target
        self.maps = []

    def addMap(self, map):
        self.maps.append(Map(map))

    def resolve(self, seed):
        for i, map in enumerate(self.maps):
            if map.matches(seed):
                return map.target(seed)
        return seed

class Map:
    def __init__(self, map):
        self.source_start = map[1]
        self.source_end = map[1] + map[2] - 1
        self.destination_start = map[0]
        self.destination_end = map[0] + map[2] - 1

    def matches(self, seed):
        return self.source_start <= seed <= self.source_end

    def target(self, seed):
        return self.destination_start + seed - self.source_start

if __name__ == '__main__':
    file = open("input.txt", 'r')

    loadingCategory = ''
    categories = {}

    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip()

        if 'seeds' in line:
            seeds = [int(item) for item in re.findall(r'\d+', line)]
        if 'map' in line:
            newMap = parse('{category}-to-{target} map:', line)
            if newMap is not None:
                loadingCategory = newMap.named['category']
                categories[loadingCategory] = Category(loadingCategory, newMap.named['target'])

        maps = re.findall(r'\d+', line)
        if loadingCategory != '' and len(maps) > 0:
            maps = [int(item) for item in maps]
            categories[loadingCategory].addMap(maps)

    seeds = Seeds(seeds, categories)
    print("Lowest Seed Location: " + str(seeds.getLowestSeedLocation()))
