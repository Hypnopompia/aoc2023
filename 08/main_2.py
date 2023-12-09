import math
from parse import *

def findStartingNodes(nodes):
    startingNodes = {}
    for nodeName, node in nodes.items():
        if nodeName[-1] == 'A':
            startingNodes[nodeName] = nodeName
    return startingNodes

def isFinishingNode(node):
    return node[-1] == 'Z'

def steps(routes, directions, currentNode):
    steps = 0

    while not isFinishingNode(currentNode):
        for direction in directions:
            steps += 1
            currentNode = nodes[currentNode][direction]
            if isFinishingNode(currentNode):
                break
    return steps

with open("input.txt", "r", encoding="utf-8") as file:
    directions = [0 if x=='L' else 1 for x in file.readline().strip()]
    
    nodes = {}
    for line in file:
        node = parse('{node} = ({left}, {right})', line.strip())
        if node is not None:
            nodes[node.named['node']] = [node.named['left'], node.named['right']]
    
    routes = findStartingNodes(nodes)

    allSteps = []
    for node in findStartingNodes(nodes):
        allSteps.append(steps(routes, directions, node))

    steps = math.lcm(*allSteps)
    print('Steps: ' + str(steps))