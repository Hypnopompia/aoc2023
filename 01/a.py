import re

file = open('input.txt', 'r')
totalCalibrationValue = 0
while True:
    line = file.readline()
    if not line:
        break
    digits = re.findall(r'\d', line)
    calibrationValue = int(str(digits[0]) + str(digits[-1]))
    totalCalibrationValue += calibrationValue

print("Calibration value: " + str(totalCalibrationValue) + "\n")
