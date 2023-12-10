def extrapolate(sequence):
    nextSequence = [sequence[i+1] - sequence[i] for i, reading in enumerate(sequence[:-1])]

    if all(r == 0 for r in nextSequence):
        print(f"0 {nextSequence}")
        return 0

    extrapolation = extrapolate(nextSequence) 
    print(f"{nextSequence[0]} - {extrapolation} = {nextSequence[0] - extrapolation} {nextSequence}")
    return nextSequence[0] - extrapolation
        

with open("input.txt", "r", encoding="utf-8") as file:
    histories = []
    for line in file:
        histories.append([int(x) for x in line.split()])

    predictions = 0
    for history in histories:
        extrapolation = extrapolate(history)
        prediction = history[0] - extrapolation
        print(f"{history[0]} - {extrapolation} = {prediction} {history}")
        print()
        predictions += prediction
    
    print(f"Predictions Total: {predictions}")
