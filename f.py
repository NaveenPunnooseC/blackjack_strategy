import random
import math

# Game Setup

def makedeck():
    """Return a shuffled deck"""
    #Makes a list with numbers 1-13, with 4 of each (13 cards per suite)
    deck = [r for r in range(1, 14)] * 4 
    random.shuffle(deck)
    return deck

def value(hand):
    """Return the best total value for your hand"""
    #Anything above 10 is counted as 10
    total = sum(min(c, 10) for c in hand)

    #Count the number of aces (1)s
    aces = hand.count(1)

    #If total with ace as 11 is less than 21, count ace as 11
    while aces > 0 and total + 10 <= 21:
        total += 10
        aces -= 1
    return total

def issoft(hand):
    """Return True if hand has an Ace counted as 11."""
    total = sum(min(c, 10) for c in hand)
    return (1 in hand) and total + 10 <= 21

# Strategies

def standardstrategy(hand, dealerup):
    """Return the move reccomended by the standard strategy"""
    v = value(hand)
    soft = issoft(hand)
    d = min(dealerup, 10)

    if v >= 17 and not soft: # value larger than or equal to 17 and not soft
        return "stand"

    if soft:
        if v >= 19:
            return "stand"
        elif v == 18:
            if 2 <= d <= 8:
                return "stand"
            else:
                return "hit"
        else:  # soft 17 or less
            return "hit"

    else:  # hard hands <= 16
        if v <= 11:
            return "hit"
        elif v == 12:
            if 4 <= d <= 6:
                return "stand"
            else:
                return "hit"
        elif 13 <= v <= 16:
            if 2 <= d <= 6:
                return "stand"
            else:
                return "hit"
        else:
            return "stand"  # safety fallback

def dealerstrategy(hand, dealerup):
    """Hit if value of hand is less than seventeen"""
    return "hit" if value(hand) <= 16 else "stand"

def randomstrategy(hand, dealerup):
    """Return either hit or stand, randomly"""
    return random.choice(["hit", "stand"])

def onehit(hand, dealerup, didhit):
    """If value is less than 13, hit exactly once"""
    if didhit: # checking if strategy has already hit before
        return "stand"
    
    # first move
    if value(hand) <= 13:
        return "hit"
    else:
        return "stand"
    
def greaterthandealer(hand, dealerup):
    """If your value is less than the dealers estimated value, hit"""
    v = value(hand)
    dealer = min(dealerup, 10) + 6.92 # dealer estunate
    if v < dealer:
        return "hit"
    else:
        return "stand"

# Playing & Testing

def play(strategy):
    """Run a round of blackjack, playing using inputed strategy"""
    deck = makedeck()

    #Needed for onehit strategy
    didhit = False 

    # deal cards
    hand = [deck.pop(), deck.pop()]
    dealerhand = [deck.pop(), deck.pop()]
    dealerup = dealerhand[0]

    #Player turn
    while True:  
        nparams = strategy.__code__.co_argcount

        if nparams == 2:
            move = strategy(hand, dealerup)
        else:
            move = strategy(hand, dealerup, didhit)

        if move == "stand":
            break
        
        #If hand is hit
        hand.append(deck.pop())

        if nparams == 3:
            didhit = True

        if value(hand) > 21:
            return "loss"
        
    # dealer turn    
    while dealerstrategy(dealerhand, dealerup) == "hit":
        dealerhand.append(deck.pop())
        if value(dealerhand) > 21:
            return "win"
        
    # compare hands
    hv = value(hand)
    dv = value(dealerhand)
    if hv < dv:
        return "loss"
    if hv > dv:
        return "win"
    if hv == dv:
        return "push"
    
def runsim(times, strategy):
    win = 0
    loss = 0
    push = 0

    #Running sim 
    for n in range(times):
        result = play(strategy)
        if result == "win":
            win += 1
        elif result == "loss":
            loss += 1
        else:
            push += 1
    
    #Percentage calculating
    total = win + loss + push
    return {
        "win%": win / total *100,
        "loss%": loss / total *100,
        "push%": push / total *100
    }

def runmanysims(nsims, hands_per_sim, strategy):
    """Run many simulations and return distribution statistics"""
    winrates = []

    for _ in range(nsims):
        result = runsim(hands_per_sim, strategy)
        winrates.append(result["win%"])

    mean = sum(winrates) / len(winrates)
    variance = sum((x - mean) ** 2 for x in winrates) / len(winrates)
    stddev = math.sqrt(variance)

    return {
        "mean_win%": mean,
        "std_dev": stddev,
        "min_win%": min(winrates),
        "max_win%": max(winrates),
        "winrates": winrates
    }