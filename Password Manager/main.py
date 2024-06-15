from tkinter import *
from tkinter import messagebox
from random_pw_generator import random_pw_gen
import pyperclip
import json


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

    new_data = {
        web_name:{
            "email": user_name,
            "password": password
        }
    }

    final_detail = f"{web_name} | {user_name} | {password}\n"

    if (len(web_name) == 0 or
            len(user_name) == 0 or
            len(password) == 0):

        messagebox.showinfo(title="Input missing", message="Please fill up the complete details")
    else:
        is_final = messagebox.askokcancel(title=web_name, message=f"These are the details entered: \nEmail: {user_name}"
                                                                  f"\nPassword: {password}\nIs it OK to save?")
        if is_final:
            try:
                with open("data.json", "r") as pass_file:
                    data = json.load(pass_file)
            except FileNotFoundError:
                data = {}

            # Checking if already data exists for the website before adding.
            if web_name in data:
                is_update = messagebox.askyesno(title=web_name, message=f"{web_name} is already available in the record."
                                                                        f"\nEmail: {user_name}\nPassword: {password}. Would you like to update?")
                if is_update:
                    data[web_name]["email"] = user_name
                    data[web_name]["password"] = password
                    messagebox.showinfo(title="Update Successful", message=f"Details for {web_name} is successfully updated.")
            else:
                data.update(new_data)
                messagebox.showinfo(title="Success", message=f"Details for {web_name} added successfully.")


            with open("data.json", "w") as pass_file:
                json.dump(data, pass_file, indent=4)

                # Post appending the details to data file, we are deleting the website name and password
                ip_webname.delete(0, END)
                ip_pw.delete(0, END)


# ---------------------------- SEARCH SETUP ------------------------------- #

def search_record():
    website = ip_webname.get()

    try:
        with open("data.json", "r") as detailed_repo:
            data = json.load(detailed_repo)
            if website in data:
                user_name = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Email ID/User name: {user_name}"
                                                   f"\nPassword: {password}")
            else:
                add_website(website)
    except FileNotFoundError:
        add_website(website)


# ---------------------------- Add Website ------------------------------- #

def add_website(website):
    add_data = messagebox.askyesno(title=website, message=f"The details aren't available for {website}. Would you like to add?")
    if add_data:
        generate_password() 
        save_pw()

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
ip_webname = Entry(width=30)
ip_webname.focus()
ip_webname.grid(row=1, column=1, padx=(5, 0))

# Creating input area for Email
ip_username = Entry(width=50)
ip_username.insert(0, "passwordman@gmail.com")
ip_username.grid(row=2, column=1, columnspan=2, padx=(10, 0))

# Creating input area for password
ip_pw = Entry(width=30)
ip_pw.grid(row=3, column=1, sticky="w", padx=(10, 0))

# Creating button for generate password
generate_pw = Button(text="Generate Password", command=generate_password)
generate_pw.grid(row=3, column=2, sticky="e")

# Creating add button
add_pw = Button(text="Add", width=25, command=save_pw)
add_pw.grid(row=4, column=1, columnspan=2, pady=10)

# Creating Search button
search = Button(text="Search", width=10, command=search_record)
search.grid(row=1, column=2, sticky="e")

window.mainloop()
