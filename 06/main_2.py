import re

def getWinningDistances(gameTime, record):
    distances = 0

    for holdTime in range(gameTime+1):
        distance = (gameTime - holdTime) * holdTime
        if distance > record:
            distances += 1

    return distances

if __name__ == '__main__':
    file = open("input.txt", 'r')
    time = int(file.readline().strip().split(':')[1].replace(' ', ''))
    distance = int(file.readline().strip().split(':')[1].replace(' ', ''))

    possibleTimes = getWinningDistances(time, distance)

    print('Answer: ' + str(possibleTimes))