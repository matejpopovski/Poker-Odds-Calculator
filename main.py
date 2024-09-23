import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os

def create_poker_table_image():
    # Define table dimensions
    width, height = 600, 400
    table_color = (0, 128, 0)  # Green color for the table

    # Create a new image with a green background
    table_image = Image.new("RGB", (width, height), table_color)

    # Optional: Draw a border
    draw = ImageDraw.Draw(table_image)
    draw.rectangle([(5, 5), (width-5, height-5)], outline="white", width=5)

    # Save the image
    table_image.save("poker_table.png")

class PokerCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Odds Calculator")
        
        self.player_count = tk.IntVar(value=6)  # Default to 6 players

        # Step 1: Choose number of players
        tk.Label(root, text="Select Number of Players:").pack()
        tk.Radiobutton(root, text="6 Players", variable=self.player_count, value=6).pack()
        tk.Radiobutton(root, text="9 Players", variable=self.player_count, value=9).pack()

        # Step 2: Create poker table area
        self.table_frame = tk.Frame(root, width=600, height=400)
        self.table_frame.pack(pady=20)

        # Load poker table image
        self.table_image = ImageTk.PhotoImage(Image.open("poker_table.png"))
        self.table_background = tk.Label(self.table_frame, image=self.table_image)
        self.table_background.place(x=0, y=0)

        # Step 3: Load card images
        self.card_images = self.load_card_images()

        # Step 4: Display cards to drag
        self.card_frame = tk.Frame(root)
        self.card_frame.pack()

        for card_name, img in self.card_images.items():
            card_label = tk.Label(self.card_frame, image=img)
            card_label.image = img  # Keep a reference
            card_label.bind("<Button-1>", self.on_drag_start)
            card_label.bind("<B1-Motion>", self.on_drag_motion)
            card_label.bind("<ButtonRelease-1>", self.on_drop)
            card_label.pack(side='left', padx=5, pady=5)

    def load_card_images(self):
        card_images = {}
        # Load card images from "images/cards"
        card_folder = "images/cards"
        card_names = os.listdir(card_folder)  # List all files in the folder
        for card_file in card_names:
            if card_file.endswith(".png"):
                img = Image.open(os.path.join(card_folder, card_file)).resize((100, 140), Image.LANCZOS)
                card_images[card_file[:-4]] = ImageTk.PhotoImage(img)  # Remove .png from name
        return card_images

    def on_drag_start(self, event):
        # Store the card being dragged
        event.widget._dragged_card = event.widget

    def on_drag_motion(self, event):
        # Move the dragged card
        dragged_card = event.widget._dragged_card
        dragged_card.place(x=event.x_root - 50, y=event.y_root - 70, anchor="center")

    def on_drop(self, event):
        # Place the card on the poker table
        event.widget.place(x=event.x_root - 50, y=event.y_root - 70, anchor="center")

if __name__ == "__main__":
    create_poker_table_image()  # Create poker table image before starting the GUI
    root = tk.Tk()
    poker_calculator = PokerCalculator(root)
    root.mainloop()
