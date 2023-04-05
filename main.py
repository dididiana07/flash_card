from tkinter import *
import pandas as pd
import random

# CONSTANTS

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Arial"
FILE = "french_words.csv"
pressed_button = 0
picked_word = {}

data = pd.read_csv(FILE)
list_words = data.to_dict(orient="records")


def next_word(words_list):
    """Picks a French word with its corresponding english translation."""
    global picked_word
    picked_word = random.choice(words_list)


def remove_word(word_list, item_to_remove):
    """Remove word from list so we can avoid to show it up again."""
    word_list.remove(item_to_remove)


def english_card():
    """Shows the english cards."""
    global back_card_image, pressed_button, picked_word, list_words
    canvas_card.itemconfig(card_image_canvas, image=back_card_image)
    canvas_card.itemconfig(title_text, text="English", fill="white")
    canvas_card.itemconfig(word_text, text=f"{picked_word['English']}", fill="white")
    wrong_button["state"] = ACTIVE
    correct_button["state"] = ACTIVE
    if pressed_button == 1:
        remove_word(list_words, picked_word)
    elif len(list_words) == 0:
        picked_word["French"] = ""
        picked_word["English"] = ""
    next_word(list_words)


def french_card(button):
    """Shows the French card."""
    global pressed_button, picked_word
    wrong_button["state"] = DISABLED
    correct_button["state"] = DISABLED
    canvas_card.itemconfig(card_image_canvas, image=front_card_image)
    canvas_card.itemconfig(title_text, text="French", fill="black")
    canvas_card.itemconfig(word_text, text=f"{picked_word['French']}", fill="black")
    screen.after(3000, english_card)
    pressed_button = button


# create screen

screen = Tk()
screen.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
screen.title("French Vocabulary")
screen.geometry("900x700")
screen.resizable(False, False)

next_word(list_words)

# create widgets
front_card_image = PhotoImage(file="card_front.png")
back_card_image = PhotoImage(file="card_back.png")

canvas_card = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
card_image_canvas = canvas_card.create_image(400, 263, image=front_card_image)
canvas_card.grid(row=0, column=1, columnspan=2)
title_text = canvas_card.create_text(400, 150, text="Flash Card", font=("Arial", 40, "italic"))
word_text = canvas_card.create_text(400, 300, text="Word", font=("Arial", 70, "bold"))

wrong_img = PhotoImage(file="wrong.png")
wrong_button = Button(image=wrong_img, background=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR,
                      command=lambda: french_card(2))
wrong_button.place(x=250, y=530)

correct_img = PhotoImage(file="right.png")
correct_button = Button(image=correct_img, background=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR,
                        command=lambda: french_card(1))
correct_button.place(x=450, y=530)

french_card(pressed_button)
screen.mainloop()
