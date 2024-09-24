import tkinter as tk
from PIL import Image, ImageTk
import os
import math

class PokerTable:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Table")

        # Create canvas for poker table
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

        # Create a frame for card images
        self.card_frame = tk.Frame(self.root, bg="green")
        self.card_frame.pack(side=tk.BOTTOM)

        # Display card images
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
        """Loads card images from the 'images/cards' directory and displays them."""
        card_folder = "images/cards"
        for card_file in os.listdir(card_folder):
            if card_file.endswith('.png'):
                card_path = os.path.join(card_folder, card_file)
                card_image = Image.open(card_path)
                card_image = card_image.resize((50, 70), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
                card_image = ImageTk.PhotoImage(card_image)
                self.card_images.append(card_image)

                card_label = tk.Label(self.card_frame, image=card_image, bg="green")
                card_label.image = card_image  # Keep a reference
                card_label.pack(side=tk.LEFT, padx=5, pady=5)

                card_label.bind("<Button-1>", self.on_card_click)
                card_label.bind("<B1-Motion>", self.on_card_drag)
                card_label.bind("<ButtonRelease-1>", self.on_card_release)

                self.card_labels.append(card_label)


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

                    # Save original position
                    label.original_grid_info = label.grid_info()

                    # Bind drag events
                    label.bind("<Button-1>", self.on_card_click)
                    label.bind("<B1-Motion>", self.on_card_drag)
                    label.bind("<ButtonRelease-1>", self.on_card_drop)

    def on_card_click(self, event):
        """Triggered when a card is clicked."""
        self.current_card = event.widget

        # Remove the card from the grid layout
        self.current_card.grid_forget()

        # Raise the card above other widgets
        self.current_card.lift()

    def on_card_drag(self, event):
        """Handles card dragging."""
        x, y = self.root.winfo_pointerxy()
        # Move the card above the cursor by 700 pixels
        self.current_card.place(x=x - 25, y=y - 35 - 700)  # Adjust based on card size

    def on_card_drop(self, event):
        """Handles dropping the card in a valid spot."""
        x, y = self.root.winfo_pointerxy()
        dropped_in_valid_spot = False

        # Check if dropped in a valid player or community spot
        for spot in self.player_spots + self.community_spots:
            spot_coords = self.canvas.coords(spot)
            if spot_coords[0] < x < spot_coords[2] and spot_coords[1] < y < spot_coords[3]:
                # Snap the card to the spot and remove it from the grid
                self.current_card.place(x=spot_coords[0] + 10, y=spot_coords[1] + 10)
                dropped_in_valid_spot = True
                self.current_card.unbind("<B1-Motion>")
                self.current_card.unbind("<ButtonRelease-1>")
                break

        # Check if dropped on the table
        if not dropped_in_valid_spot:
            if self.table_x0 < x < self.table_x1 and self.table_y0 < y < self.table_y1:
                # Snap the card to the table (centered)
                self.current_card.place(x=(self.table_x0 + self.table_x1) // 2 - 25, 
                                        y=(self.table_y0 + self.table_y1) // 2 - 35)
                dropped_in_valid_spot = True
                self.current_card.unbind("<B1-Motion>")
                self.current_card.unbind("<ButtonRelease-1>")

        if not dropped_in_valid_spot:
            # Return the card to its original grid position if not dropped in a valid spot
            self.current_card.place_forget()
            self.current_card.grid(**self.current_card.original_grid_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerTable(root)
    root.mainloop()
