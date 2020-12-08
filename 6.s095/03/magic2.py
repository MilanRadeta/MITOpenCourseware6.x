#Programming for the Puzzled -- Srini Devadas
#You Can Read Minds (With a Little Calibration)
#Five random cards are chosen and one of them is hidden.
#Given four cards in a particular order, you can figure out what the fifth card is!

#Deck is are a list of strings, each string is a card
#The order of cards in the list matters.
# suits = ['♣', '♦', '♥', '♠']
from itertools import permutations

suits = ['C', 'D', 'H', 'S']
ranks = ['A'] + list(range(2, 11)) + ['J', 'Q', 'K']
deck = ['%s_%s' % (rank, s) for rank in ranks for s in suits]

def BaseAsistant(card_fun):
    print ('Cards are character strings as shown below.')
    print ('Ordering is:', deck)

    #Initialization
    cards, cind, cardsuits, cnumbers = [], [], [], []
    numsuits = [0, 0, 0, 0]
    pairsuit = None

    #Take cards as input from user/audience
    #Various data structures are filled in
    for i in range(5):
        n = card_fun(i)
        print(n)
        suit = n % 4
        cards.append(deck[n])
        cind.append(n)
        cardsuits.append(suit)
        cnumbers.append(n // 4)
        numsuits[suit] += 1
        if numsuits[suit] > 1:
            pairsuit = suit

    #Find two cards out of the 5 that have the same suit. Guaranteed to exist.
    cardh = [i for i in range(5) if cardsuits[i] == pairsuit]

    #Figure out which card needs to be hidden and what number to encode
    hidden, other, encode = outputFirstCard(cnumbers, cardh, cards)

    remindices = [cind[i] for i in range(5) if i not in (hidden, other)]

    #Order the three cards in ascending order
    sortList(remindices)

    #Given the number that needs to be encoded, order the cards appropriately
    outputNext3Cards(encode, remindices)

    return cards[hidden]

def ask_for_card(i):
    print ('Please give card', i+1, end = ' ')
    card = input('in above format:')
    return deck.index(card)

def random_card(number):
    def return_card(i):
        nonlocal number
        number = number * (i + 1) // (i + 2)
        return number % len(deck)
    return return_card


#Given 5 cards, Assistant hides an appropriate card
#He/she reads out the remaining four cards after choosing their order carefully!
def AssistantOrdersCards():
    BaseAsistant(ask_for_card)


#This procedure figures out which card should be hidden based on the distance
#between the two cards that have the same suit.
#It returns the hidden card, the first exposed card, and the distance
def outputFirstCard(numbers, oneTwo, cards):
    total_ranks = len(ranks)
    hidden = oneTwo[0]
    other = oneTwo[1]
    encode = (numbers[hidden] - numbers[other]) % total_ranks
    if encode <= 0 or encode > 6:
        hidden = oneTwo[1]
        other = oneTwo[0]
        encode = -encode % total_ranks

    print ('First card is:', cards[other])

    return hidden, other, encode



perms = list(permutations([0, 1, 2]))

#This procedure orders three cards depending on the number "code" that
#needs to be encoded. 
def outputNext3Cards(code, ind):
    second, third, fourth = perms[code - 1]
    second, third, fourth = ind[second], ind[third], ind[fourth]

    print ('Second card is:', deck[second])
    print ('Third card is:', deck[third])
    print ('Fourth card is:', deck[fourth])

    
#Sorts elements in tlist in ascending order.
def sortList(tlist):
    for i in range(0, len(tlist)-1):
        for j in range(i, len(tlist)):
            if tlist[i] > tlist[j]:
                tlist[i], tlist[j] = tlist[j], tlist[i]


#This procedure takes four cards encoded properly and determines the hidden card.
def MagicianGuessesCard():
    print ('Cards are character strings as shown below.')
    print ('Ordering is:', deck)
    suit, number = (None, None)
    cards, cind = [], []

    for i in range(4):
        n = ask_for_card(i)
        cards.append(deck[n])
        cind.append(n)
        if i == 0:
            suit = n % 4
            number = n // 4
            
    #Use the ordering of the last 3 cards to determine distance from 1st card
    encode = perms.index(cind) + 1

    #Knowing the number and the suit gives the card index and then string
    hiddennumber = (number + encode) % 13
    index = hiddennumber * 4 + suit

    print ('Hidden card is:', deck[index])


#This procedure is similar to AssistantOrdersCards() except it
#takes in a large number and "randomly" generates five cards.
def ComputerAssistant():
    number = 0
    while number < 99999:
        number = int(input('Please give random number' +
                               ' of at least 6 digits:'))

    hidden_card = BaseAsistant(random_card(number))

    guess = input('What is the hidden card?')
    if guess == hidden_card:
        print ('You are a Mind Reader Extraordinaire!')
    else:
        print ('Sorry, not impressed!')


# AssistantOrdersCards()
ComputerAssistant()