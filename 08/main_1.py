from parse import *

with open("example_2.txt", "r", encoding="utf-8") as file:
    directions = [0 if x=='L' else 1 for x in file.readline().strip()]

    nodes = {}
    for line in file:
        node = parse('{node} = ({left}, {right})', line.strip())
        if node is not None:
            nodes[node.named['node']] = [node.named['left'], node.named['right']]
    
    
    currentNode = 'AAA'
    steps = 0

    while currentNode != 'ZZZ':
        for direction in directions:
            steps += 1
            currentNode = nodes[currentNode][direction]
            if currentNode == 'ZZZ':
                break

    print('Steps from AAA to ZZZ: ' + str(steps))
