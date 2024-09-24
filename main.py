import tkinter as tk
from PIL import Image, ImageTk
import os
import math

class PokerTable:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Table")
        
        # Create canvas and card frame
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Set background color
        self.canvas.configure(bg="green")

        # Draw the poker table (red oval)
        self.table_width = 600
        self.table_height = 400
        self.table_x0 = (self.canvas_width - self.table_width) // 2
        self.table_y0 = (self.canvas_height - self.table_height) // 2
        self.table_x1 = self.table_x0 + self.table_width
        self.table_y1 = self.table_y0 + self.table_height
        self.canvas.create_oval(self.table_x0, self.table_y0, self.table_x1, self.table_y1, outline="red", width=5)

        # Initialize lists for player spots, community spots, card images, and card labels
        self.player_spots = []
        self.community_spots = []
        self.card_images = []  # Initialize here to fix the error
        self.card_labels = []

        # Create player spots
        self.create_player_spots()

        # Create community card spots (flop, turn, river)
        self.create_community_card_spots()

        # Display card images
        self.card_frame = tk.Frame(self.root, bg="green")
        self.card_frame.pack(side=tk.BOTTOM)
        self.display_card_images()

        # For drag-and-drop functionality
        self.current_card = None

    def create_player_spots(self):
        """Creates 9 player spots for cards."""
        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2
        radius_x = self.table_width // 2 - 50
        radius_y = self.table_height // 2 - 50
        num_players = 9

        for i in range(num_players):
            angle = 2 * math.pi * i / num_players
            pos_x = center_x + radius_x * math.cos(angle)
            pos_y = center_y + radius_y * math.sin(angle)

            card_width = 30
            card_height = 50
            card_x0 = pos_x - card_width
            card_y0 = pos_y - card_height // 2
            card_x1 = card_x0 + card_width * 2
            card_y1 = card_y0 + card_height

            spot = self.canvas.create_rectangle(card_x0, card_y0, card_x1, card_y1, outline="black", width=2)
            self.player_spots.append(spot)

            # Add player labels
            self.canvas.create_text(pos_x, pos_y - card_height//2 - 10, text=f"Player {i+1}", fill="white", font=("Helvetica", 12))

    def create_community_card_spots(self):
        """Creates 5 spots for the community cards in the middle (flop, turn, river)."""
        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2
        card_width = 50
        card_height = 70

        for i in range(5):
            x0 = center_x - (card_width * 2.5) + i * card_width  # Align the 5 cards horizontally
            y0 = center_y - card_height // 2
            x1 = x0 + card_width
            y1 = y0 + card_height

            spot = self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", width=2)
            self.community_spots.append(spot)

    def display_card_images(self):
        """Displays card images in a grid below the table and makes them draggable."""
        card_folder = 'images/cards'
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

        for row, suit in enumerate(suits):
            for col, rank in enumerate(ranks):
                image_path = os.path.join(card_folder, f'{rank}_of_{suit}.png')
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    img = img.resize((50, 70))
                    card_image = ImageTk.PhotoImage(img)
                    self.card_images.append(card_image)  # Keep reference

                    # Create label and make it draggable
                    label = tk.Label(self.card_frame, image=card_image, bg="green")
                    label.grid(row=row, column=col, padx=5, pady=5)
                    self.card_labels.append(label)

                    # Bind drag events
                    label.bind("<Button-1>", self.on_card_click)
                    label.bind("<B1-Motion>", self.on_card_drag)
                    label.bind("<ButtonRelease-1>", self.on_card_drop)

    def on_card_click(self, event):
        """Triggered when a card is clicked."""
        self.current_card = event.widget
        self.current_card.lift()

    def on_card_drag(self, event):
        """Handles card dragging."""
        x, y = event.widget.winfo_pointerxy()
        event.widget.place(x=x - 25, y=y - 35)

    def on_card_drop(self, event):
        """Handles dropping the card in a valid spot."""
        x, y = event.widget.winfo_pointerxy()
        for spot in self.player_spots + self.community_spots:
            spot_coords = self.canvas.coords(spot)
            if spot_coords[0] < x < spot_coords[2] and spot_coords[1] < y < spot_coords[3]:
                # Snap the card to the spot
                event.widget.place(x=spot_coords[0] + 10, y=spot_coords[1] + 10)
                return

        # If no valid spot, return the card to its original position in the grid
        event.widget.place_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerTable(root)
    root.mainloop()
