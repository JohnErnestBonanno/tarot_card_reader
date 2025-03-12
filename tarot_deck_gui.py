import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import random
import os
from math import comb

# Set seed for reproducibility
random.seed(42)

# File paths
csv_file_path = '/Users/jebbonanno/Documents/workspace/tarot_card_reader/tarot_cards.csv'
image_dir = '/Users/jebbonanno/Documents/workspace/tarot_card_reader/image_folder/'

# Load the tarot card data
tarot_base_df = pd.read_csv(csv_file_path)


### ---- Probability Calculations ---- ###
prob_major_arcana = comb(22, 3) / comb(78, 3)
prob_minor_arcana = 4 * comb(14, 3) / comb(78, 3)
prob_three_kind = (comb(4, 3) * 14) / comb(78, 3)
prob_royals = comb(16, 3) / comb(78, 3)
prob_flush = (4 * comb(14, 3)) / comb(78, 3)

# Probability of a straight
single_straight = 4**3  # 4 choices per suit, 3 ranks in a straight
all_straight = 8 * single_straight  # 8 possible straights
prob_straight = all_straight / comb(78, 3)

### ---- Condition Checking Function ---- ###
def condition_check(three_card_pull):
    court_list = ['Page', 'Knight', 'Queen', 'King']

    # Initialize the message variable
    message = ""

    # Ensure 'number_digit' is sorted for straight condition
    three_card_pull = three_card_pull.sort_values(by="number_digit").reset_index()

    if three_card_pull['Number'].nunique() == 1:
        message = f"Three of a Kind! Probability: {round((prob_three_kind*100),2)}%"

    elif three_card_pull['Suit'].nunique() == 1 and three_card_pull.iloc[0]['Suit'] == 'Major Arcana':
        message = f"All Major Arcana! Probability: {round((prob_major_arcana*100),2)}%"

    elif three_card_pull['Suit'].nunique() == 1:
        message = f"A Three Card Flush! Probability: {round((prob_flush*100),2)}%"

    elif (three_card_pull['number_digit'][2] - three_card_pull['number_digit'][1] == 1 and 
          three_card_pull['number_digit'][1] - three_card_pull['number_digit'][0] == 1):
        message = f"A Straight! Probability: {round((prob_straight*100),2)}%"

    elif three_card_pull['Number'].isin(court_list).all():
        message = f"A Court Pull! Probability: {round((prob_royals*100),2)}%"

    # Update probability label text
    probability_label.config(text=message)

### ---- GUI Functionality ---- ###



def on_button_click():
    # Draw 3 random cards
    selected_rows = tarot_base_df.sample(3)

    # Check for any special tarot conditions
    condition_check(selected_rows)

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
root.geometry("500x500")

# Create a frame to hold the three cards
card_frame = tk.Frame(root)
card_frame.pack(pady=10)

# Create a label to display probability messages
probability_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="red")
probability_label.pack(pady=5)  # Place it above the button

# Create a button and place it at the bottom
button = tk.Button(root, text="Draw 3 Cards", command=on_button_click)
button.pack(side="bottom", pady=20)

# Run the application
root.mainloop()