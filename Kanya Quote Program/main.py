from tkinter import *
import requests as reqs

kanye_url = "https://api.kanye.rest"


# ---- Button code -----------#
def next_quote():
    response = reqs.get(url=kanye_url)
    response.raise_for_status()

    quote_dict = response.json()
    quote = quote_dict["quote"]
    canvas.itemconfig(quote_text, text=quote)


# ---------- UI Setup -------- #
window = Tk()
window.title("Kanye Quotes")
window.config(padx=30, pady=30)

# Background image
canvas = Canvas(width=300, height=414)
bg_img = PhotoImage(file="background.png")
canvas.create_image(150, 207, image=bg_img)
quote_text = canvas.create_text(150, 207, text="Kanye Quote Goes Here!", font=("Arial", 15, "bold"), width=250)
canvas.grid(row=0, column=0)

# Button placement
button_img = PhotoImage(file="kanye.png")
button = Button(image=button_img, highlightthickness=0, borderwidth=0, command=next_quote)
button.grid(row=1, column=0)

window.mainloop()
