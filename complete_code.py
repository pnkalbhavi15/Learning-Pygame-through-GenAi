# Initial Code File
# Imports
import pygame
import sys
import os
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bidding Diamonds Cards Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)

# Define fonts
font = pygame.font.SysFont(None, 36)

# Load card images
def load_card_images():
    images_dir = "images"
    card_images = {}
    for filename in os.listdir(images_dir):
        if filename.endswith(".png"):
            card_images[filename[:-4]] = pygame.image.load(os.path.join(images_dir, filename))
    return card_images

CARD_IMAGES = load_card_images()

# Utility functions
def display_text(text, position, font_size=36, color=WHITE):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


# Draw button
def draw_button(text, rect, action=None, font_size=24):
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, LIGHT_GRAY, rect)  
        if clicked and action:
            action()  
    else:
        pygame.draw.rect(screen, GRAY, rect)
    display_text(text, (rect.x + 10, rect.y + 10), font_size)

# Function to display player's cards
def display_player_cards(player_cards):
    x_offset = 50
    for card_name in player_cards:
        screen.blit(CARD_IMAGES[card_name], (x_offset, 350))
        x_offset += 60

# Draw top menu bar
def draw_top_menu():
    pygame.draw.rect(screen, DARK_GRAY, pygame.Rect(0, 0, SCREEN_WIDTH, 50))
    draw_button("New Game", pygame.Rect(20, 10, 100, 30), main_menu, 20)
    draw_button("Quit", pygame.Rect(SCREEN_WIDTH - 120, 10, 100, 30), quit_game, 20)

# Define game
def define_game():
    display_text("Bidding Diamonds Cards Game", (20, 40), font_size=40)
    display_text("Rules:", (20, 100), font_size=28)
    display_text("1. Number of Players: 2-3 players compete.", (20, 130), font_size=24)
    display_text("2. Card Distribution:", (20, 160), font_size=24)
    display_text("- Each player receives a hand of 13 cards.", (40, 190), font_size=20)
    display_text("- One suit (clubs, hearts, spades, or diamonds) is assigned to each player.", (40, 210), font_size=20)
    display_text("3. Bidding Rounds:", (20, 240), font_size=24)
    display_text("- In each round, a diamond card is revealed.", (40, 270), font_size=20)
    display_text("- Players take turns bidding with a card from their assigned suit.", (40, 300), font_size=20)
    display_text("- The highest bidder wins the round.", (40, 330), font_size=20)
    display_text("4. Scoring:", (20, 360), font_size=24)
    display_text("- The winner earns points equal to the value of the revealed diamond card.", (40, 390), font_size=20)
    display_text("- Points are earned based on the number of diamonds won in each round.", (40, 420), font_size=20)
    display_text("5. Tie Cases:", (20, 450), font_size=24)
    display_text("- In the event of a tie bid, average points are awarded.", (40, 480), font_size=20)
    display_text("6. Game End:", (20, 510), font_size=24)
    display_text("- After 13 rounds, the player with the most accumulated diamonds wins the game.", (40, 540), font_size=20)

# Main menu
def main_menu():
    while True:
        screen.fill(BLACK)
        define_game()
        draw_button("Play Against Friends", pygame.Rect(100, 600, 180, 40), lambda: start_game(False), font_size=20)
        draw_button("Play Against Computer", pygame.Rect(400, 600, 180, 40), lambda: start_game(True), font_size=20)
        draw_button("Quit", pygame.Rect(700, 600, 180, 40), quit_game, font_size=20)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:  
                if pygame.Rect(350, 550, 300, 50).collidepoint(event.pos):
                    start_game()
                elif pygame.Rect(350, 620, 300, 50).collidepoint(event.pos):
                    quit_game()

# Main game loop
def start_game(AGAINST_COMPUTER):
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
        if not AGAINST_COMPUTER:
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
            screen.fill(BLACK)

            # Draw top menu bar
            draw_top_menu()

            # Display current player and prompt for bidding
            display_text(f"{player}'s turn to bid.", (20, 80))
            # Display diamond card
            display_text(f"Diamond Card : {diamond_card}", (20, 120))
            display_text(f"Click on the card you want to bid :", (20, 160))
            display_player_cards(cards)
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
        screen.fill(BLACK)

        # Draw top menu bar
        draw_top_menu()

        # Prompt user to enter the number of players
        if not AGAINST_COMPUTER:
            display_text("Enter number of players (2 or 3):", (20, 80))
        else:
            display_text("Enter number of players (1 or 2):", (20, 80))
        pygame.display.flip()

        num_players = None
        while (num_players not in [2, 3] and not AGAINST_COMPUTER) or (num_players not in [1, 2] and AGAINST_COMPUTER) :
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        num_players = 1
                    elif event.key == pygame.K_2:
                        num_players = 2
                    elif event.key == pygame.K_3:
                        num_players = 3
                    elif event.key == pygame.K_q:  # Quit if 'Q' key is pressed
                        quit_game()

        # Distribute cards to players
        if not AGAINST_COMPUTER:
            players_cards = distribute_cards(num_players)
        else:
            players_cards, computers_cards = distribute_cards(num_players)
        
        # Display player cards and announce assigned suits
        suit_announcement = {1: "clubs", 2: "hearts", 3: "spades", 4: "diamonds"}
        scores = {player: 0 for player in players_cards}
        for i, (player, cards) in enumerate(players_cards.items()):
            display_text(f"{player} has been assigned {suit_announcement[i+1]}", (20, 80 + (i + 1) * 40))
        if AGAINST_COMPUTER:
            display_text(f"Computer has been assigned {suit_announcement[3]}", (20, 80 + (3) * 40))
            scores["computer"] = 0
        
        # Display legend for bidding input
        legend_y = 300
        display_text("Legend for Bidding:", (20, legend_y), font_size=24, color=WHITE)
        display_text("Click on the card to bid", (20, legend_y + 40),
                     font_size= 20, color=WHITE)

        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds

        # Initialize the list of diamond cards
        diamond_cards = list(range(2, 11)) + ["jack", "queen", "king", "ace"]
        random.shuffle(diamond_cards)

        # Main game loop for 13 rounds
        for round_num in range(1, 14):
            highest_bid = {player: None for player in players_cards}  # Reset highest_bid for each round
            # Clear the screen
            screen.fill(BLACK)

            # Draw top menu bar
            draw_top_menu()

            # Display round number
            display_text(f"Round {round_num}", (20, 80))

            # Display diamond card for the round
            diamond_card = select_diamond_card()
            diamond_card_image = pygame.image.load(os.path.join("images", f"{diamond_card}_of_diamonds.png"))
            screen.blit(diamond_card_image, (300, 50))

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

            if AGAINST_COMPUTER:
                computers_bid = computers_bid_strategy(players_cards, computers_cards, diamond_card, diamond_cards)
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
            screen.fill(BLACK)

            # Draw top menu bar
            draw_top_menu()
            # Display round result
            display_text(f"Diamonds earned this round: {diamonds_earned}", (20, 250))
            for player, score in scores.items():
                display_text(f"{player}: {score} diamonds", (20, 300 + 40 * list(scores.keys()).index(player)))
                # Display cards bid by the player
                display_text(f"Cards bid: {highest_bid[player]}", (500, 300 + 40 * list(scores.keys()).index(player)))

            pygame.display.flip()
            pygame.time.delay(5000)  # Pause for 5 seconds before starting the next round

        # Announce the winner at the end of 13 rounds
        winner = max(scores, key=scores.get)
        display_text(f"{winner} wins with {scores[winner]} diamonds!", (20, 600))
        pygame.display.flip()
        pygame.time.delay(5000)  # Pause for 5 seconds

    # Quit Pygame
    pygame.quit()
    sys.exit()

def computers_bid_strategy(players_cards, computers_cards, diamond_card, remaining_diamond_cards):
    # If there are still remaining diamond cards, bid the highest available card if it's higher than the revealed diamond card
    if remaining_diamond_cards:
        # Get the numerical value of the revealed diamond card
        diamond_card_value = diamond_card if isinstance(diamond_card, int) else get_card_value(diamond_card)
        
        # Find the highest available card in the computer's hand
        max_card = max(computers_cards, key=lambda x: get_card_value(x))
        
        # Check if the highest available card is higher than the revealed diamond card
        if get_card_value(max_card) > diamond_card_value:
            return max_card
        else:
            # If the highest available card is not higher than the revealed diamond card,
            # bid the lowest available card that is higher than the revealed diamond card
            for card in sorted(computers_cards, key=lambda x: get_card_value(x)):
                if get_card_value(card) > diamond_card_value:
                    return card
            # If no card is found that is higher than the revealed diamond card, bid the lowest available card
            return min(computers_cards, key=lambda x: get_card_value(x))

    # If there are no remaining diamond cards, bid the lowest card in the computer's hand
    return min(computers_cards, key=lambda x: get_card_value(x))

def get_card_value(card_name):
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

# Function to quit the game
def quit_game():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
