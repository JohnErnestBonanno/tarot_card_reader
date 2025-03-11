import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import random
import os

import random
random.seed(42)

csv_file_path = '/Users/jebbonanno/Documents/workspace/tarot_card_reader/tarot_cards.csv'

image_dir = '/Users/jebbonanno/Documents/workspace/tarot_card_reader/image_folder/'


tarot_base_df = pd.read_csv(csv_file_path)

def on_button_click():

    single_row = tarot_base_df.sample(1)
    
    card_name = single_row['Name'].values[0]
    label.config(text=card_name)

    image_filename = single_row['file_path'].values[0] 
    image_path = os.path.join(image_dir, image_filename)

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((150, 250))  # Resize for display
        img = ImageTk.PhotoImage(img)

        image_label.config(image=img)
        image_label.image = img

# Create the main window
root = tk.Tk()
root.title("Tarot Deck")
root.geometry("300x500")

# Create a button
button = tk.Button(root, text="Draw a Card", command=on_button_click)
button.pack(pady=20)

# Create a label for text
label = tk.Label(root, text="", font=("Arial", 14))
label.pack(pady=10)

# Create a label for images
image_label = tk.Label(root)
image_label.pack(pady=10)


# Run the GUI event loop
root.mainloop()