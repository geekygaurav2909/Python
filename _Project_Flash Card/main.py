from tkinter import *
import pandas as pd
import random
BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
to_learn = {}

# ---------- READING FILE AND SHOWING RANDOM FRENCH WORDS--------- #
try:
    content = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = content.to_dict(orient="records")


# print(to_learn[0]["French"])
# print(to_learn)

def next_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    img_canvas.itemconfig(title_text, text="French", fill="black")
    img_canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    img_canvas.itemconfig(canvas_image, image=front_image)
    
    flip_timer = window.after(3000,change_card)


# ----------------------------- CHANGING CARD ------------------------- #

def change_card():
    img_canvas.itemconfig(title_text, text="English", fill="white")
    img_canvas.itemconfig(canvas_image, image=back_image)
    img_canvas.itemconfig(word_text, text=current_card["English"], fill="white")


# ------------------ User knows the word ---------------------------- #
def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_word()

# ----------------------------- UI SETUP ------------------------- #

window = Tk()
window.title("Flash Card App")
window.config(padx=40, pady=60, bg= BACKGROUND_COLOR)

flip_timer= window.after(3000, change_card)


# Image canvas for the background card
img_canvas = Canvas(width=800, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)

front_image = PhotoImage(file = "images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")

canvas_image = img_canvas.create_image(400,265, image= front_image)
title_text = img_canvas.create_text(400,150, text="", font= ("Arial", 40, "italic"))
word_text = img_canvas.create_text(400,263, text="", font=("Arial", 60, "bold"))
img_canvas.grid(row=0, column=0)


# wrong tick placement
wrong_tick = PhotoImage(file="images/wrong.png")
wrong_canvas = Button(image=wrong_tick, highlightthickness=0, borderwidth=0, command=next_word)
wrong_canvas.grid(row=1, column=0, sticky="w", padx=(100,0))


# right tick placement
right_tick = PhotoImage(file="images/right.png")
right_canvas=Button(image=right_tick, highlightthickness=0, borderwidth=0, command=is_known)
right_canvas.grid(row=1, column=0, sticky="e", padx=(0,100))

next_word()




window.mainloop()
