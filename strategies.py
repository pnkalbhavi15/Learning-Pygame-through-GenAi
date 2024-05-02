class ComputersBidStrategy:
    def __init__(self):
        pass

    def bid(self, players_cards, computers_cards, diamond_card, remaining_diamond_cards):
        # If there are still remaining diamond cards, bid the highest available card if it's higher than the revealed diamond card
        if remaining_diamond_cards:
            # Get the numerical value of the revealed diamond card
            diamond_card_value = diamond_card if isinstance(diamond_card, int) else self.get_card_value(diamond_card)
            
            # Find the highest available card in the computer's hand
            max_card = max(computers_cards, key=lambda x: self.get_card_value(x))
            
            # Check if the highest available card is higher than the revealed diamond card
            if self.get_card_value(max_card) > diamond_card_value:
                return max_card
            else:
                # If the highest available card is not higher than the revealed diamond card,
                # bid the lowest available card that is higher than the revealed diamond card
                for card in sorted(computers_cards, key=lambda x: self.get_card_value(x)):
                    if self.get_card_value(card) > diamond_card_value:
                        return card
                # If no card is found that is higher than the revealed diamond card, bid the lowest available card
                return min(computers_cards, key=lambda x: self.get_card_value(x))

        # If there are no remaining diamond cards, bid the lowest card in the computer's hand
        return min(computers_cards, key=lambda x: self.get_card_value(x))
    
    def get_card_value(self, card_name):
        # Define a dictionary to map card names to their numerical values
        card_values = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "jack": 11, "queen": 12, "king": 13, "ace": 14
        }
        
        # Extract the numerical value of the card from its name
        if isinstance(card_name, str):
            value_str = card_name.split("_")[0]
            return card_values.get(value_str, 0)
        else:
            return card_name  # Return the integer value directly if it's not a string

# Bidding Strategies (strategies.py): This file contains the bidding strategy for computer players. The ComputersBidStrategy class provides a method bid which determines the computer's bidding strategy based on the current game state.