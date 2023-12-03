import re

digitMap = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

file = open('input.txt', 'r')
totalCalibrationValue = 0
while True:
    line = file.readline()
    if not line:
        break
    
    pattern = re.compile("(?=(" + "|".join(digitMap.keys()) + "))")
    digits = re.findall(pattern, line)

    for i in range(len(digits)):
        digits[i] = digitMap[digits[i]]

    calibrationValue = int(str(digits[0]) + str(digits[-1]))
    totalCalibrationValue += calibrationValue

print("Calibration value: " + str(totalCalibrationValue) + "\n")
