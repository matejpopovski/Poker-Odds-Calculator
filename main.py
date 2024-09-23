import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

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
        self.table_frame = tk.Frame(root, width=600, height=400, bg="green")
        self.table_frame.pack(pady=20)
        tk.Label(self.table_frame, text="Poker Table", bg="green", font=("Arial", 16)).pack()

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
        # Adjust the path as necessary
        card_names = ["AS", "KH", "QS", "JD", "10C", "9H", "8D", "7S", "6C"]  # Add more as needed
        for card in card_names:
            img = Image.open(f"images/{card}.png").resize((100, 140), Image.ANTIALIAS)
            card_images[card] = ImageTk.PhotoImage(img)
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
    root = tk.Tk()
    poker_calculator = PokerCalculator(root)
    root.mainloop()
