def extrapolate(sequence):
    nextSequence = [sequence[i+1] - sequence[i] for i, reading in enumerate(sequence[:-1])]

    if all(r == 0 for r in nextSequence):
        print(f"{nextSequence} 0 = 0")
        return 0

    extrapolation = extrapolate(nextSequence) 
    print(f"{nextSequence} {nextSequence[-1]} + {extrapolation} = {extrapolation + nextSequence[-1]}")
    return extrapolation + nextSequence[-1]
        

with open("input.txt", "r", encoding="utf-8") as file:
    histories = []
    for line in file:
        histories.append([int(x) for x in line.split()])

    predictions = 0
    for history in histories:
        extrapolation = extrapolate(history)
        prediction = history[-1] + extrapolation
        print(f"{history} {history[-1]} + {extrapolation} = {prediction}")
        print()
        predictions += prediction
    
    print(f"Predictions Total: {predictions}")
