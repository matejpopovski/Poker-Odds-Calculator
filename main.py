import tkinter as tk
from PIL import Image, ImageTk
import os
import math

def create_poker_table_image():
    width, height = 800, 500
    table_color = (0, 128, 0)

    table_image = Image.new("RGB", (width, height), table_color)
    draw = ImageDraw.Draw(table_image)
    draw.rectangle([(5, 5), (width-5, height-5)], outline="white", width=5)

    # Draw community card spots
    for i in range(5):
        draw.rectangle([(300 + i * 60 - 20, 200 - 30), (300 + i * 60 + 20, 200 + 30)], outline="white")

    table_image.save("poker_table.png")

class PokerCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Odds Calculator")

        # Create poker table area
        self.table_frame = tk.Frame(root, width=800, height=500)
        self.table_frame.pack(pady=20)

        # Load poker table image
        self.table_image = ImageTk.PhotoImage(Image.open("poker_table.png"))
        self.table_background = tk.Label(self.table_frame, image=self.table_image)
        self.table_background.place(x=0, y=0)

        # Load card images
        self.card_images = self.load_card_images()

        # Display cards to drag in an elliptical layout
        self.player_card_labels = []
        num_players = 9
        radius = 180
        for i, (card_name, img) in enumerate(self.card_images.items()):
            angle = (i * 2 * math.pi) / num_players
            x = 400 + radius * math.cos(angle)  # Centered around the table
            y = 350 + radius * math.sin(angle)
            
            card_label = tk.Label(self.table_frame, image=img)
            card_label.image = img  # Keep a reference
            card_label.bind("<Button-1>", self.on_drag_start)
            card_label.bind("<B1-Motion>", self.on_drag_motion)
            card_label.bind("<ButtonRelease-1>", self.on_drop)
            card_label.place(x=x, y=y)
            self.player_card_labels.append(card_label)

        # Community card labels
        self.community_card_labels = []
        for i in range(5):
            community_card_label = tk.Label(self.table_frame)
            community_card_label.place(x=300 + i * 60, y=200)
            self.community_card_labels.append(community_card_label)

    def load_card_images(self):
        card_images = {}
        card_folder = "images/cards"
        card_names = sorted(os.listdir(card_folder))  # Sort for A to K
        for card_file in card_names:
            if card_file.endswith(".png"):
                img = Image.open(os.path.join(card_folder, card_file)).resize((60, 90), Image.LANCZOS)
                card_images[card_file[:-4]] = ImageTk.PhotoImage(img)  # Remove .png from name
        return card_images

    def on_drag_start(self, event):
        event.widget._dragged_card = event.widget
        event.widget._offset_x = event.x
        event.widget._offset_y = event.y

    def on_drag_motion(self, event):
        dragged_card = event.widget._dragged_card
        x = event.x_root - event.widget._offset_x
        y = event.y_root - event.widget._offset_y
        dragged_card.place(x=x, y=y)

    def on_drop(self, event):
        dragged_card = event.widget._dragged_card
        x = event.x_root - event.widget._offset_x
        y = event.y_root - event.widget._offset_y
        
        # Check if the card is dropped within the poker table area
        if 0 <= x <= 800 and 0 <= y <= 500:
            dragged_card.place(x=x, y=y)
        else:
            # Return the card to its original position
            self.reset_card_position(dragged_card)

    def reset_card_position(self, card_label):
        index = self.player_card_labels.index(card_label)
        angle = (index * 2 * math.pi) / len(self.player_card_labels)
        radius = 180
        x = 400 + radius * math.cos(angle)
        y = 350 + radius * math.sin(angle)
        card_label.place(x=x, y=y)

if __name__ == "__main__":
    create_poker_table_image()  # Create poker table image before starting the GUI
    root = tk.Tk()
    poker_calculator = PokerCalculator(root)
    root.mainloop()
