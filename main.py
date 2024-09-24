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

    # Draw the oval table
    table_width = 600
    table_height = 400
    table_x0 = (canvas_width - table_width) // 2
    table_y0 = (canvas_height - table_height) // 2
    table_x1 = table_x0 + table_width
    table_y1 = table_y0 + table_height
    canvas.create_oval(table_x0, table_y0, table_x1, table_y1, outline="green", width=5)

    # Calculate positions for 9 players in an oval layout
    center_x = canvas_width // 2
    center_y = canvas_height // 2
    radius_x = table_width // 2 - 50
    radius_y = table_height // 2 - 50
    num_players = 9

    # Draw positions for each player
    for i in range(num_players):
        angle = 2 * math.pi * i / num_players
        pos_x = center_x + radius_x * math.cos(angle)
        pos_y = center_y + radius_y * math.sin(angle)

        # Create a rectangle for the player's 2 cards
        card_width = 50
        card_height = 80
        card_x0 = pos_x - card_width // 2
        card_y0 = pos_y - card_height // 2
        card_x1 = card_x0 + card_width * 2  # Space for two cards side by side
        card_y1 = card_y0 + card_height

        canvas.create_rectangle(card_x0, card_y0, card_x1, card_y1, outline="black", width=2)

        # Add labels for player numbers
        canvas.create_text(pos_x, pos_y - card_height//2 - 10, text=f"Player {i+1}", fill="white", font=("Helvetica", 12))

    root.mainloop()

if __name__ == "__main__":
    create_poker_table()
