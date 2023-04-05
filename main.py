from tkinter import *
import pandas as pd
import random
import os

# CONSTANTS

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Arial"
FILE = "french_words.csv"
running = None
new_file = "learnt_words.csv"
pressed_button = 0
french_word = ""
english_word = ""
saved_words = []

# create screen

screen = Tk()
screen.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
screen.title("French Vocabulary")
screen.geometry("900x700")
screen.resizable(False, False)


# add functionality


def stop():
    """Stops the function called with scree.after()"""
    screen.after_cancel(running)


def create_file(name_of_file: str):
    """Creates the file that manages the learnt_words.csv."""
    data = ""
    try:
        with open(file=name_of_file, mode="r") as file:
            data = name_of_file
    except FileNotFoundError:
        with open(file=name_of_file, mode="a") as file:
            file.write("French,English")
            data = name_of_file
    return data


def save_learned_words(learnt_word, translated):
    """When clicking the correct button it will save the words in a new file."""
    name_file = create_file(new_file)
    with open(file=name_file, mode="a") as file:
        file.write(f"\n{learnt_word},{translated}")


def word(file=FILE):
    """Picks a French word with its corresponding english translation.
    When pressing the correct button, avoid showing the word that it's saved on the learnt_words.csv"""
    data = pd.read_csv(file)
    picked_french_word = random.choice(data.French.values)
    english_translation_word = data.English[data.French == picked_french_word].values[0]
    if picked_french_word in saved_words:
        screen.after(1000, word)
    return picked_french_word, english_translation_word


def english_card():
    """Shows the english cards."""
    global english_word, back_card_image, french_word, pressed_button, saved_words
    canvas_card.itemconfig(card_image_canvas, image=back_card_image)
    canvas_card.itemconfig(title_text, text="English", fill="white")
    canvas_card.itemconfig(word_text, text=f"{english_word}", fill="white")
    wrong_button["state"] = ACTIVE
    correct_button["state"] = ACTIVE
    if pressed_button == 1:
        save_learned_words(saved_words[0], saved_words[1])
    saved_words[0] = french_word
    saved_words[1] = english_word


def french_card(button):
    """Shows the French card."""
    global french_word, running, pressed_button, english_word, saved_words
    french_word, english_word = word()
    canvas_card.itemconfig(card_image_canvas, image=front_card_image)
    canvas_card.itemconfig(title_text, text="French", fill="black")
    canvas_card.itemconfig(word_text, text=f"{french_word}", fill="black")
    running = screen.after(3000, english_card)
    wrong_button["state"] = DISABLED
    correct_button["state"] = DISABLED
    saved_words.append(french_word)
    saved_words.append(english_word)
    pressed_button = button


def restart_automatically(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


restart_automatically(new_file)

# create widgets
front_card_image = PhotoImage(file="card_front.png")
back_card_image = PhotoImage(file="card_back.png")

canvas_card = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
card_image_canvas = canvas_card.create_image(400, 263, image=front_card_image)
canvas_card.grid(row=0, column=1)
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
