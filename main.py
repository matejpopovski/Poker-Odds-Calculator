import random
from itertools import combinations

def get_valid_input(prompt, valid_range):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_range:
                return value
            else:
                print(f"Input must be between {valid_range[0]} and {valid_range[-1]}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_cards_input(player_count, board=False):
    cards = []
    for i in range(1, player_count + 1 if not board else 2):
        if not board:
            prompt = f"Enter two cards for Player {i} (e.g., 'As Ks'): "
        else:
            prompt = "Enter cards for the board (3, 4, or 5 cards e.g., 'As Ks Qd'): "
        
        while True:
            user_input = input(prompt).strip().split()
            if board and len(user_input) in [3, 4, 5]:
                cards = user_input
                return cards
            elif not board and len(user_input) == 2:
                cards.append(user_input)
                break
            else:
                print("Invalid number of cards. Try again.")
    return cards

def calculate_winning_percentage(player_hands, board_cards):
    # Placeholder for actual computation
    # You'd integrate a poker equity calculator or Monte Carlo simulation
    return random.randint(10, 90)  # Simulates a random percentage for simplicity

def main():
    print("Welcome to the Texas Hold'em Poker Calculator!")
    
    # Step 1: Number of players
    num_players = get_valid_input("Enter the number of players (2-9): ", range(2, 10))
    
    # Step 2: Get player hands
    player_hands = get_cards_input(num_players)
    print(f"Player hands: {player_hands}")
    
    # Step 3: Get board cards
    board_cards = get_cards_input(1, board=True)
    print(f"Board cards: {board_cards}")
    
    # Step 4: Calculate winning percentage
    winning_percentage = calculate_winning_percentage(player_hands, board_cards)
    print(f"\nYour % of winning is {winning_percentage}%.")

if __name__ == "__main__":
    main()

