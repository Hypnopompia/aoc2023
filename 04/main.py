from parse import *
import re

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

if __name__ == '__main__':
    file = open("input.txt", 'r')
    totalScore = 0
    cards = []
    while True:
        line = file.readline().strip()
        if not line:
            break
        card = parse('Card {card_id}: {winning_numbers} | {have_numbers}', line).named
        card['winning_numbers'] = re.findall(r'\d+', card['winning_numbers'])
        card['have_numbers'] = re.findall(r'\d+', card['have_numbers'])
        card['winning_count'] = len(intersection(card['winning_numbers'], card['have_numbers']))
        card['copies'] = 1
        cards.append(card)
    
        score = 1 if card['winning_count'] else 0
        if card['winning_count'] > 1:
            score = score << card['winning_count']-1
        totalScore += score

    totalCopies = 0
    for i, card in enumerate(cards):
        for j in range(card['copies']):
            for k in range(i+1, i+card['winning_count']+1):
                cards[k]['copies'] += 1
        totalCopies += card['copies']

    print("Score: " + str(totalScore))
    print("Copies: " + str(totalCopies))
