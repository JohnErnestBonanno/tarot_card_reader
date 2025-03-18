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


### ---- probabilities ---- ###

prob_major_arcana = round(comb(22, 3) / comb(78, 3) * 100 , 2)

prob_three_kind = round((comb(4,3) * 14) / comb(78,3) * 100, 2)

prob_royals = round(comb(16, 3) / comb(78 , 3) *100, 2) 

prob_flush = round((4 * comb(14,3)) / comb(78 , 3) * 100, 2)

prob_royal_flush = 4/76076

prob_straight_flush = 52/76076


#prob_straight
single_straight = 4**3  # 4 choices per suit, 3 ranks in a straight
all_straight = 8 * single_straight #(8 possible straights)
prob_straight = round((all_straight) / comb(78 , 3) *100, 2)

### ---- Condition Checking Function ---- ###

def condition_check(selected_rows, num_cards):  # Add num_cards as a parameter
    court_list = ['Page', 'Knight', 'Queen', 'King']
    message = ""

    # Ensure 'number_digit' column exists before sorting
    if 'number_digit' in selected_rows.columns:
        selected_rows = selected_rows.sort_values(by="number_digit").reset_index()

        if num_cards > 1 and selected_rows['Suit'].nunique() == 1 and selected_rows['Suit'][0] == 'Major Arcane':
            message = f"Major Arcana Only! A {prob_major_arcana}% chance."

        elif num_cards > 1 and selected_rows['Number'].nunique() == 1:
            message = f"Three of a Kind! A {prob_three_kind}% chance."
        
        elif num_cards > 1 and selected_rows['Suit'].nunique() == 1:
            message = f"A Flush! A {prob_flush}% chance."
        
        elif num_cards > 1 and selected_rows['Number'].isin(court_list).all():
            message = f"A Court Pull! A {prob_royals}% chance."

        elif num_cards == 3 and selected_rows['number_digit'].nunique() == 3:
            sorted_digits = sorted(selected_rows['number_digit'])
            if sorted_digits[2] - sorted_digits[1] == 1 and sorted_digits[1] - sorted_digits[0] == 1:
                message = f"A Straight! A {prob_straight}% chance."

    probability_label.config(text=message)

### ---- GUI Functionality ---- ###

def draw_cards(num_cards):
    # Draw random cards based on user selection
    selected_rows = tarot_base_df.sample(num_cards)
    
    # Check for any special tarot conditions
    condition_check(selected_rows, num_cards)  # Pass num_cards here
    
    # Clear previous images and labels
    for widget in card_frame.winfo_children():
        widget.destroy()
    
    # Labels for positions (only for 3-card draw)
    time_labels = ["Past", "Present", "Future"] if num_cards == 3 else ["Single Card"]
    
    # Loop through the selected cards and display them
    for idx, row in enumerate(selected_rows.itertuples()):
        card_name = row.Name
        image_filename = row.file_path
        image_path = os.path.join(image_dir, image_filename)

        # Create and place the labels
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
            image_label.grid(row=1, column=idx, padx=10, pady=5)

            # Create a text label and place it below the image
            text_label = tk.Label(card_frame, text=card_name, font=("Arial", 12))
            text_label.grid(row=2, column=idx, padx=10, pady=5)

# Create the main window
root = tk.Tk()
root.title("Rider-Waite Tarot Deck")
root.geometry("500x500")

# Create a frame to hold the drawn cards
card_frame = tk.Frame(root)
card_frame.pack(pady=10)

# Create a label for probability messages
probability_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="red")
probability_label.pack(pady=5)

# Create buttons for drawing cards
button_3 = tk.Button(root, text="Draw 3 Cards", command=lambda: draw_cards(3))
button_3.pack(side="bottom", pady=10)

button_1 = tk.Button(root, text="Draw 1 Card", command=lambda: draw_cards(1))
button_1.pack(side="bottom", pady=10)

# Run the application
root.mainloop()
