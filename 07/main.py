from collections import Counter

class Hand:
    def __init__(self, hand, bet):
        self.hand = hand
        self.bet = bet
        
        counter = Counter(self.hand)
        
        self.counts = sorted(list(counter.values()), reverse=True)
        self.type = ''.join([str(cnt) for cnt in self.counts])
        self.cardWeights = list(map("23456789TJQKA".index, self.hand))

        self.jokerCounter = Counter(self.hand.replace('J',''))
        self.jokerMostCommon = sorted(list(self.jokerCounter.most_common()), reverse=True, key=lambda x: x[1])
        if len(self.jokerMostCommon):
            self.jokerHand = self.hand.replace('J', self.jokerMostCommon[0][0])
        else:
            self.jokerHand = self.hand
        self.jokerCounter = Counter(self.jokerHand)
        self.jokerCounts = sorted(list(self.jokerCounter.values()), reverse=True)
        self.jokerType = ''.join([str(cnt) for cnt in self.jokerCounts])
        self.jokerCardWeights = list(map("J23456789TQKA".index, self.hand))

    def __repr__(self):
        return repr((self.hand, self.bet, self.counts, self.cardWeights))
    
    def weight(self):
        return (self.type, self.cardWeights)

    def jokerWeight(self):
        return (self.jokerType, self.jokerCardWeights)


if __name__ == '__main__':
    file = open("input.txt", 'r')

    hands = []

    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip().split()
        hands.append(Hand(line[0], int(line[1])))

    hands = sorted(hands, key=lambda hand: hand.weight())

    totalWinnings = 0;
    for i, hand in enumerate(hands):
        rank = i + 1
        totalWinnings += rank * hand.bet

    print("Total Winnings: " + str(totalWinnings))

    hands = sorted(hands, key=lambda hand: hand.jokerWeight())

    jokerWinnings = 0;
    for i, hand in enumerate(hands):
        rank = i + 1
        jokerWinnings += rank * hand.bet

    print("Joker Winnings: " + str(jokerWinnings))