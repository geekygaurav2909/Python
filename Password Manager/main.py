from tkinter import *
from tkinter import messagebox
from random_pw_generator import random_pw_gen
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Created a seperate random password generator code
def generate_password():
    random_pass = random_pw_gen()
    ip_pw.delete(0, END)
    ip_pw.insert(0, random_pass)
    pyperclip.copy(random_pass)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pw():
    web_name = ip_webname.get()
    user_name = ip_username.get()
    password = ip_pw.get()

    final_detail = f"{web_name} | {user_name} | {password}\n"

    if (len(web_name) == 0 or
            len(user_name) == 0 or
            len(password) == 0):

        messagebox.showinfo(title="Input missing", message="Please fill up the complete details")
    else:
        is_final = messagebox.askokcancel(title=web_name, message=f"These are the details entered: \nEmail: {user_name}"
                                                                  f"\nPassword: {password}\nIs it OK to save?")
        if is_final:
            with open("data.txt", "a") as pass_file:
                pass_file.write(final_detail)

                # Post appending the details to data file, we are deleting the website name and password
                ip_webname.delete(0, END)
                ip_pw.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(height=200, width=200)
pm_logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pm_logo)
canvas.grid(row=0, column=1)

# Creating label for website
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

# Creating label for Email/Username
username_label = Label(text="Email/Username:", pady=10)
username_label.grid(row=2, column=0)

# Creating label for Password
pw_label = Label(text="Password:")
pw_label.grid(row=3, column=0)

# Creating input area for website
ip_webname = Entry(width=50)
ip_webname.focus()
ip_webname.grid(row=1, column=1, columnspan=2, padx=(10, 0))

# Creating input area for Email
ip_username = Entry(width=50)
ip_username.insert(0, "passwordman@gmail.com")
ip_username.grid(row=2, column=1, columnspan=2, padx=(10, 0))

# Creating input area for password
ip_pw = Entry(width=25)
ip_pw.grid(row=3, column=1, sticky="w", padx=(10, 0))

# Creating button for generate password
generate_pw = Button(text="Generate Password", command=generate_password)
generate_pw.grid(row=3, column=2, sticky="e")

# Creating add button
add_pw = Button(text="Add", width=25, command=save_pw)
add_pw.grid(row=4, column=1, columnspan=2, pady=10)

window.mainloop()
