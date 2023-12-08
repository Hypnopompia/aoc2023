import re

def getWinningDistances(gameTime, record):
    distances = []

    for holdTime in range(gameTime+1):
        distance = (gameTime - holdTime) * holdTime
        if distance > record:
            distances.append(holdTime)

    return distances

if __name__ == '__main__':
    file = open("input.txt", 'r')
    times = file.readline().strip().split(':')[1]
    times = [int(item) for item in re.findall(r'\d+', times)]
    distances = file.readline().strip().split(':')[1]
    distances = [int(item) for item in re.findall(r'\d+', distances)]

    marginOfError = 1

    for game in range(len(times)):
        winningDistances = getWinningDistances(times[game], distances[game])
        marginOfError *= len(winningDistances)

    print('Answer: ' + str(marginOfError))