import pygame
import sys
import os
import random
from ui import UI
from strategies import ComputersBidStrategy

class Gameplay:
    def __init__(self):
        self.ui = UI()
        self.computers_bid_strategy = ComputersBidStrategy()
    @staticmethod
    def start_game(against_computer):
        # Function to select a random unique diamond card for the round
        def select_diamond_card():
            return diamond_cards.pop()  

        # Function to distribute cards to each player
        def distribute_cards(num_players):
            suits = ["clubs", "hearts", "spades", "diamonds"]
            random.shuffle(suits)
            players_cards = {f"Player {i + 1}": [] for i in range(num_players)}
            card_names = [
                "2_of_clubs", "3_of_clubs", "4_of_clubs", "5_of_clubs", "6_of_clubs", "7_of_clubs", "8_of_clubs", 
                "9_of_clubs", "10_of_clubs", "jack_of_clubs", "queen_of_clubs", "king_of_clubs", "ace_of_clubs",
                "2_of_hearts", "3_of_hearts", "4_of_hearts", "5_of_hearts", "6_of_hearts", "7_of_hearts", "8_of_hearts", 
                "9_of_hearts", "10_of_hearts", "jack_of_hearts", "queen_of_hearts", "king_of_hearts", "ace_of_hearts",
                "2_of_spades", "3_of_spades", "4_of_spades", "5_of_spades", "6_of_spades", "7_of_spades", "8_of_spades", 
                "9_of_spades", "10_of_spades", "jack_of_spades", "queen_of_spades", "king_of_spades", "ace_of_spades",
                "2_of_diamonds", "3_of_diamonds", "4_of_diamonds", "5_of_diamonds", "6_of_diamonds", "7_of_diamonds", 
                "8_of_diamonds", "9_of_diamonds", "10_of_diamonds", "jack_of_diamonds", "queen_of_diamonds", "king_of_diamonds", 
                "ace_of_diamonds"
            ]
            for i in range(num_players):
                for card_name in card_names[i * 13: (i + 1) * 13]:
                    players_cards[f"Player {i + 1}"].append(card_name)
            if not against_computer:
                return players_cards
            computers_cards = []
            for card_name in card_names[2 * 13 : (3) * 13]:
                computers_cards.append(card_name)
            return players_cards, computers_cards

        # Function to handle bidding loop for each player
        def bidding_loop(player, cards):
            bidding_card = None
            clock = pygame.time.Clock()  
            running = True  
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for i, card_name in enumerate(cards):
                            card_rect = pygame.Rect(50 + i * 60, 400, 50, 70)  
                            if card_rect.collidepoint(mouse_pos):
                                bidding_card = card_name
                                running = False 
                                break

                # Clear the screen
                UI.screen.fill(UI.BLACK)

                # Draw top menu bar
                UI.draw_top_menu()

                # Display current player and prompt for bidding
                UI.display_text(f"{player}'s turn to bid.", (20, 80))
                # Display diamond card
                UI.display_text(f"Diamond Card : {diamond_card}", (20, 120))
                UI.display_text(f"Click on the card you want to bid :", (20, 160))
                UI.display_player_cards(cards)
                pygame.display.flip()

                clock.tick(30)  # Limit frame rate to avoid high CPU usage

            return bidding_card

        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen
            UI.screen.fill(UI.BLACK)

            # Draw top menu bar
            UI.draw_top_menu()

            # Prompt user to enter the number of players
            if not against_computer:
                UI.display_text("Enter number of players (2 or 3):", (20, 80))
            else:
                UI.display_text("Enter number of players (1 or 2):", (20, 80))
            pygame.display.flip()

            num_players = None
            while (num_players not in [2, 3] and not against_computer) or (num_players not in [1, 2] and against_computer) :
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            num_players = 1
                        elif event.key == pygame.K_2:
                            num_players = 2
                        elif event.key == pygame.K_3:
                            num_players = 3
                        elif event.key == pygame.K_q:  # Quit if 'Q' key is pressed
                            UI.quit_game()

            # Distribute cards to players
            if not against_computer:
                players_cards = distribute_cards(num_players)
            else:
                players_cards, computers_cards = distribute_cards(num_players)
            
            # Display player cards and announce assigned suits
            suit_announcement = {1: "clubs", 2: "hearts", 3: "spades", 4: "diamonds"}
            scores = {player: 0 for player in players_cards}
            for i, (player, cards) in enumerate(players_cards.items()):
                UI.display_text(f"{player} has been assigned {suit_announcement[i+1]}", (20, 80 + (i + 1) * 40))
            if against_computer:
                UI.display_text(f"Computer has been assigned {suit_announcement[3]}", (20, 80 + (3) * 40))
                scores["computer"] = 0
            
            # Display legend for bidding input
            legend_y = 300
            UI.display_text("Legend for Bidding:", (20, legend_y), font_size=24, color=UI.WHITE)
            UI.display_text("Click on the card to bid", (20, legend_y + 40),
                        font_size= 20, color=UI.WHITE)

            pygame.display.flip()
            pygame.time.delay(3000)  # Pause for 3 seconds

            # Initialize the list of diamond cards
            diamond_cards = list(range(2, 11)) + ["jack", "queen", "king", "ace"]
            random.shuffle(diamond_cards)

            # Main game loop for 13 rounds
            for round_num in range(1, 14):
                highest_bid = {player: None for player in players_cards}  # Reset highest_bid for each round
                # Clear the screen
                UI.screen.fill(UI.BLACK)

                # Draw top menu bar
                UI.draw_top_menu()

                # Display round number
                UI.display_text(f"Round {round_num}", (20, 80))

                # Display diamond card for the round
                diamond_card = select_diamond_card()
                diamond_card_image = pygame.image.load(os.path.join("images", f"{diamond_card}_of_diamonds.png"))
                UI.screen.blit(diamond_card_image, (300, 50))

                # Update the display
                pygame.display.flip()
                pygame.time.delay(2000)  # Pause for 2 seconds

                # Main bidding loop
                for player, cards in players_cards.items():
                    bidding_card = bidding_loop(player, cards)
                    if bidding_card in cards:
                        highest_bid[player] = bidding_card
                        players_cards[player].remove(bidding_card)
                    else:
                        # Handle invalid bidding card input
                        print("Invalid bidding card input!")  # Adjust this to your needs

                if against_computer:
                    computers_bid = ComputersBidStrategy.bid(players_cards, computers_cards, diamond_card, diamond_cards)
                    highest_bid["computer"] = computers_bid
                    computers_cards.remove(computers_bid)
                # Define a dictionary to map card names to their numerical values
                card_values = {
                    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                    "jack": 11, "queen": 12, "king": 13, "ace": 14
                }

                # After the bidding loop, determine the highest bid based on numerical values
                max_bid_value = max(highest_bid.values(), key=lambda x: card_values.get(x.split("_")[0]))
                players_with_max_bid = [player for player, bid in highest_bid.items() if bid.split("_")[0] == max_bid_value.split("_")[0]]

                diamonds_earned = 0  # Initialize with a default value
                # Calculate diamonds earned for the round
                if players_with_max_bid:
                    print("Players with max bid:", players_with_max_bid)
                    if len(players_with_max_bid) == 1:
                        print("Only one player with max bid")
                        if isinstance(diamond_card, int):
                            diamonds_earned = diamond_card  # If it's already a number, no need for conversion
                        else:
                            if diamond_card == "ace":
                                diamonds_earned = 14
                            elif diamond_card == "king":  # Prioritize king over queen
                                diamonds_earned = 13
                            elif diamond_card == "queen":
                                diamonds_earned = 12
                            elif diamond_card == "jack":
                                diamonds_earned = 11
                            else:
                                diamonds_earned = int(diamond_card.split("_")[0])
                        # Add all diamonds to the player with the highest bid
                        scores[players_with_max_bid[0]] += diamonds_earned
                    else:
                        print("Multiple players with max bid")
                        if isinstance(diamond_card, int):
                            diamonds_earned_per_player = diamond_card / len(players_with_max_bid)  # Adjust for multiple players
                        else:
                            if diamond_card == "ace":
                                diamonds_earned_per_player = 14 / len(players_with_max_bid)
                            elif diamond_card == "king":  # Prioritize king over queen
                                diamonds_earned_per_player = 13 / len(players_with_max_bid)
                            elif diamond_card == "queen":
                                diamonds_earned_per_player = 12 / len(players_with_max_bid)
                            elif diamond_card == "jack":
                                diamonds_earned_per_player = 11 / len(players_with_max_bid)
                            else:
                                diamonds_earned_per_player = int(diamond_card.split("_")[0]) / len(players_with_max_bid)
                        print("Diamonds earned per player:", diamonds_earned_per_player)
                        for player in players_with_max_bid:
                            scores[player] += diamonds_earned_per_player
                        diamonds_earned = diamonds_earned_per_player * len(players_with_max_bid)

                else:
                    diamonds_earned = 0  # No players with valid bid, no diamonds earned
                # Clear the screen
                UI.screen.fill(UI.BLACK)

                # Draw top menu bar
                UI.draw_top_menu()
                # Display round result
                UI.display_text(f"Diamonds earned this round: {diamonds_earned}", (20, 250))
                for player, score in scores.items():
                    UI.display_text(f"{player}: {score} diamonds", (20, 300 + 40 * list(scores.keys()).index(player)))
                    # Display cards bid by the player
                    UI.display_text(f"Cards bid: {highest_bid[player]}", (500, 300 + 40 * list(scores.keys()).index(player)))

                pygame.display.flip()
                pygame.time.delay(5000)  # Pause for 5 seconds before starting the next round

            # Announce the winner at the end of 13 rounds
            winner = max(scores, key=scores.get)
            UI.display_text(f"{winner} wins with {scores[winner]} diamonds!", (20, 600))
            pygame.display.flip()
            pygame.time.delay(5000)  # Pause for 5 seconds

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gameplay = Gameplay()

# Gameplay Logic (gameplay.py): This file contains the main game logic, including the initialization of the game, handling the start of the game, and any other game-related functionality. The start_game method handles the start of the game based on whether the player chooses to play against a computer or against friends.