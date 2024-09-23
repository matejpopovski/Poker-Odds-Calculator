import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os

def create_poker_table_image():
    width, height = 600, 400
    table_color = (0, 128, 0)  # Green color for the table

    # Create a new image with a green background
    table_image = Image.new("RGB", (width, height), table_color)
    draw = ImageDraw.Draw(table_image)
    draw.rectangle([(5, 5), (width-5, height-5)], outline="white", width=5)

    # Draw designated spots for 9 players
    spots = [(50, 50), (150, 50), (250, 50), (350, 50), (450, 50), 
             (50, 200), (150, 200), (250, 200), (350, 200)]
    for spot in spots:
        draw.rectangle([spot[0]-15, spot[1]-20, spot[0]+15, spot[1]+20], outline="white")

    table_image.save("poker_table.png")

class PokerCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Odds Calculator")
        
        # Create poker table area
        self.table_frame = tk.Frame(root, width=600, height=400)
        self.table_frame.pack(pady=20)

        # Load poker table image
        self.table_image = ImageTk.PhotoImage(Image.open("poker_table.png"))
        self.table_background = tk.Label(self.table_frame, image=self.table_image)
        self.table_background.place(x=0, y=0)

        # Load card images
        self.card_images = self.load_card_images()

        # Display cards to drag in a grid layout
        self.card_frame = tk.Frame(root)
        self.card_frame.pack()

        rows = 3  # Change this for more rows if needed
        columns = 13  # 13 cards (Ace to King)
        for i, (card_name, img) in enumerate(self.card_images.items()):
            card_label = tk.Label(self.card_frame, image=img)
            card_label.image = img  # Keep a reference
            card_label.bind("<Button-1>", self.on_drag_start)
            card_label.bind("<B1-Motion>", self.on_drag_motion)
            card_label.bind("<ButtonRelease-1>", self.on_drop)
            card_label.grid(row=i // columns, column=i % columns, padx=5, pady=5)

    def load_card_images(self):
        card_images = {}
        card_folder = "images/cards"
        card_names = sorted(os.listdir(card_folder))  # Sort for A to K
        for card_file in card_names:
            if card_file.endswith(".png"):
                img = Image.open(os.path.join(card_folder, card_file)).resize((80, 120), Image.LANCZOS)  # Smaller size
                card_images[card_file[:-4]] = ImageTk.PhotoImage(img)  # Remove .png from name
        return card_images

    def on_drag_start(self, event):
        event.widget._dragged_card = event.widget

    def on_drag_motion(self, event):
        dragged_card = event.widget._dragged_card
        dragged_card.place(x=event.x_root - 40, y=event.y_root - 60, anchor="center")

    def on_drop(self, event):
        # Place the card on the poker table
        event.widget.place(x=event.x_root - 40, y=event.y_root - 60, anchor="center")

if __name__ == "__main__":
    create_poker_table_image()  # Create poker table image before starting the GUI
    root = tk.Tk()
    poker_calculator = PokerCalculator(root)
    root.mainloop()
