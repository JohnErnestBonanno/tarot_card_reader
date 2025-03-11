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


# Create a frame for the main content (image & label) to keep button at bottom
content_frame = tk.Frame(root)
content_frame.pack(expand=True, fill="both")

# Create a label for images (placed at the top inside content_frame)
image_label = tk.Label(content_frame)
image_label.pack(pady=10)

# Create a label for text (placed below the image inside content_frame)
label = tk.Label(content_frame, text="", font=("Arial", 14))
label.pack(pady=10)

# Create a button and place it at the bottom
button = tk.Button(root, text="Draw a Card", command=on_button_click)
button.pack(side="bottom", pady=20)  # Ensure button stays at the bottom





# Run the GUI event loop
root.mainloop()