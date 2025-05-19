from main import *
from tkinter import filedialog


# GUI Setup
root = tk.Tk()
root.title("Particles Tracker")

open_button = tk.Button(root, text="Open Video File", command=getvideo)
open_button.pack(pady=10)

open_button = tk.Button(root, text="Color", command=getcolor)
open_button.pack(pady=30)


open_button = tk.Button(root, text="Analyze", command=Analyze)
open_button.pack(pady=40)


word_label = tk.Label(root, text="", font=("Helvetica", 70), pady=20)
word_label.pack()

root.mainloop()
