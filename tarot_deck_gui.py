import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import random
import os

# Set seed for reproducibility
random.seed(42)

# File paths
csv_file_path = '/Users/jebbonanno/Documents/workspace/tarot_card_reader/tarot_cards.csv'
image_dir = '/Users/jebbonanno/Documents/workspace/tarot_card_reader/image_folder/'

# Load the tarot card data
tarot_base_df = pd.read_csv(csv_file_path)

def on_button_click():
    # Draw 3 random cards
    selected_rows = tarot_base_df.sample(3)

    # Labels for positions
    time_labels = ["Past", "Present", "Future"]

    # Clear previous images and labels
    for widget in card_frame.winfo_children():
        widget.destroy()

    # Loop through the selected cards and display them
    for idx, row in enumerate(selected_rows.itertuples()):
        card_name = row.Name
        image_filename = row.file_path
        image_path = os.path.join(image_dir, image_filename)

        # Create and place the "Past", "Present", "Future" labels
        time_label = tk.Label(card_frame, text=time_labels[idx], font=("Arial", 14, "bold"))
        time_label.grid(row=0, column=idx, padx=10, pady=5)

        # Load and display the image
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((120, 200))  # Resize for display
            img = ImageTk.PhotoImage(img)

            # Create an image label and place it in the grid
            image_label = tk.Label(card_frame, image=img)
            image_label.image = img  # Keep reference to avoid garbage collection
            image_label.grid(row=1, column=idx, padx=10, pady=5)  # Images in row 1

            # Create a text label and place it below the image
            text_label = tk.Label(card_frame, text=card_name, font=("Arial", 12))
            text_label.grid(row=2, column=idx, padx=10, pady=5)  # Text in row 2

# Create the main window
root = tk.Tk()
root.title("Rider-Waite Tarot Deck")
root.geometry("500x370")

# Create a frame to hold the three cards
card_frame = tk.Frame(root)
card_frame.pack(pady=10)

# Create a button and place it at the bottom
button = tk.Button(root, text="Draw 3 Cards", command=on_button_click)
button.pack(side="bottom", pady=20)

# Run the application
root.mainloop()