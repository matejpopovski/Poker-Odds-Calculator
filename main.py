import tkinter as tk
from PIL import Image, ImageTk
import os
import math  

def create_poker_table():
    # Initialize the main window
    root = tk.Tk()
    root.title("Poker Table")

    # Set window size
    canvas_width = 800
    canvas_height = 600
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Color the entire window green (table felt color)
    canvas.configure(bg="green")

    # Draw the red oval table
    table_width = 600
    table_height = 400
    table_x0 = (canvas_width - table_width) // 2
    table_y0 = (canvas_height - table_height) // 2
    table_x1 = table_x0 + table_width
    table_y1 = table_y0 + table_height
    canvas.create_oval(table_x0, table_y0, table_x1, table_y1, outline="red", width=5)

    # Calculate positions for 9 players in an oval layout
    center_x = canvas_width // 2
    center_y = canvas_height // 2
    radius_x = table_width // 2 - 50
    radius_y = table_height // 2 - 50
    num_players = 9

    # Draw positions for each player (smaller card placeholder squares)
    for i in range(num_players):
        angle = 2 * math.pi * i / num_players
        pos_x = center_x + radius_x * math.cos(angle)
        pos_y = center_y + radius_y * math.sin(angle)

        # Create smaller rectangles for the player's 2 cards
        card_width = 30  # Smaller card width
        card_height = 50  # Smaller card height
        card_x0 = pos_x - card_width // 2
        card_y0 = pos_y - card_height // 2
        card_x1 = card_x0 + card_width * 2  # Space for two cards side by side
        card_y1 = card_y0 + card_height

        canvas.create_rectangle(card_x0, card_y0, card_x1, card_y1, outline="black", width=2)

        # Add labels for player numbers
        canvas.create_text(pos_x, pos_y - card_height//2 - 10, text=f"Player {i+1}", fill="white", font=("Helvetica", 12))

    return canvas, root

def display_card_images(root):
    # Frame for card images
    card_frame = tk.Frame(root, bg="green")
    card_frame.pack(side=tk.BOTTOM)

    # Path to the folder containing card images
    card_folder = 'images/cards'

    # List of card filenames
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    card_images = []

    # Load each card image and display it in a grid
    for row, suit in enumerate(suits):
        for col, rank in enumerate(ranks):
            image_path = os.path.join(card_folder, f'{rank}_of_{suit}.png')
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((50, 70))  # Resize the image to fit in the grid
                card_image = ImageTk.PhotoImage(img)
                card_images.append(card_image)  # Store the image reference

                # Create a label to hold the card image
                label = tk.Label(card_frame, image=card_image, bg="green")
                label.grid(row=row, column=col, padx=5, pady=5)

    return card_images

if __name__ == "__main__":
    canvas, root = create_poker_table()
    card_images = display_card_images(root)
    root.mainloop()
