
import tkinter as tk
import pandas as pd

import random
random.seed(42)

csv_file_path = '/Users/jebbonanno/Documents/workspace/tarot_card_reader/tarot_cards.csv'
tarot_base_df = pd.read_csv(csv_file_path)

def on_button_click():

    single_card = tarot_base_df.sample(1)['Name'].values[0]
    label.config(text=single_card)

# Create the main window
root = tk.Tk()
root.title("Simple GUI")

# Create a label
label = tk.Label(root, text="Press the button", font=("Arial", 14))
label.pack(pady=10)

# Create a button
button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=20)

# Run the GUI event loop
root.mainloop()