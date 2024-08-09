def calculate_score(hand):
    ranks = []
    suits = []
    suit_distribution = {"S" : 0, "D" : 0, "H" : 0, "C" : 0}
 
    for card in hand:
        if len(card) == 2:
            rank = card[0]
            suit = card[1]
        else:
            rank = card[0:2]
            suit = card[2]
        if rank == "J":
            rank = 11
        elif rank == "Q":
            rank = 12
        elif rank == "K":
            rank = 13
        elif rank == "A":
            rank = 14
        
        ranks.append(int(rank))
        suits.append(suit)
        suit_distribution[suit] += 1

    # All Spades
    if suits[0] == "S" and suits.count(suits[0]) == 13:
        return "You Literally Win"

    # The value of cards is as follows: {Card Rank : Point Value}
    spades_values = {2 : 0.5, 3 : 0.5, 4 : 0.5, 5 : 0.5, 6 : 0.5, 7 : 0.5,
                     8 : 1, 9 : 1, 10 : 2, 11 : 2, 12 : 3, 13 : 3, 14 : 4}
    high_card_values = {10 : 0.5, 11 : 1, 12 : 1.5, 13 : 2, 14 : 3}

    ## Calculating Spades Points and High Card Points ##
    spades_pts = 0
    high_card_pts = 0

    for i in range(len(ranks)):
        if suits[i] == "S":
            spades_pts += spades_values[ranks[i]]
        elif ranks[i] > 9:
            high_card_pts += high_card_values[ranks[i]]
    
    ## Calculating Distribution ##
    distribution = 0 # Balanced but bad distribution
    spades = suit_distribution["S"]
    diamonds = suit_distribution["D"]
    hearts = suit_distribution["H"]
    clubs = suit_distribution["C"]

    sorted_suits = sorted([spades, diamonds, hearts, clubs])
    
    if sorted_suits == [3,3,3,4] or sorted_suits == [2,3,4,4]:
        distribution = 2 # Well-balanced hand
    elif sorted_suits == [1,3,4,5] or sorted_suits == [2,3,3,5]:
        distribution = 1  # Slightly imbalanced hand
    elif sorted_suits[3] >= 6 and sorted_suits[0] >= 2:
        distribution = 1.5 if sorted_suits[3] == 6 else 2  # Strongly imbalanced but advantageous hand
    elif sorted_suits[3] >= 7:
        distribution = 1  # Extreme imbalance
    elif sorted_suits[3] == 8:
        distribution = 0.5  # Highly unbalanced
    
    ## Calculating Synergy ##
    synergy = 0

    # Face Card Synergy
    face_cards = [card for card in hand if card[0] in ['A', 'K', 'Q', 'J']] # Creates array of face cards from hand
    if len(face_cards) > 4:
        synergy += 1
    
    # Spade Synergy
    spade_cards = [card for card in hand if card[1] == "S"] # Creates array of spade cards from hand
    if len(spade_cards) > 4 and any(card[0] in ['A', 'K', 'Q'] for card in spade_cards):
        synergy += 1
    
    # Void or Singleton
    voids = sum(1 for count in suit_distribution.values() if count == 0) # Adds 1 for each suit that has no cards
    singletons = sum(1 for count in suit_distribution.values() if count == 1) # Adds 1 for each suit that has 1 card
    if voids > 0 or singletons > 0:
        synergy += 0.5 if voids == 1 or singletons == 1 else 1
    
    # Long Suit
    long_suits = sum(1 for count in suit_distribution.values() if count >= 5)
    if long_suits > 0:
        synergy += 0.5 if long_suits == 1 else 1
    
    ## Final Rating ##
    # Formula: ((Spades Points + High Card Points + Distribution + Synergy)/(Max Possible Points))*10, this rating is out of 10
    max_pts = 28
    score = ((spades_pts + high_card_pts + distribution + synergy)/(max_pts))*10
    return f"{score:.2f}"
