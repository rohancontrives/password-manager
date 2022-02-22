from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import json
import pyperclip

LIGHT_YELLOW = "#FAEDC6"
LIGHT_GREEN = "#BAFFB4"


# ---------------------------- PASSWORD FINDER ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=f"Search result for {website}", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Info Box",
                                message=f"No details for the {website} exits")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def password_generator():
    password_entry.delete(0, END)  # deletes previously populated entry.
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '@', '#', '$', '%', '&', '*', '.']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(END, string=password)

    """
    # Copying functionality by pyperclip module
    # A cross-platform clipboard module for Python, with copy & paste functions for plain text.
    """
    pyperclip.copy(password)

    # Copied pop-up
    """
    A toast provides simple feedback about an operation in a small popup. 
    # It only fills the amount of space required for the message 
    # and the current activity remains visible and interactive. 
    # Toasts automatically disappear after a timeout.
    """
    toast = Label(window, text="Copied to clipboard")
    toast.grid(row=4, column=2, sticky="ew")
    window.after(2000, lambda: toast.destroy())
    window.mainloop()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """
    entry = Entry()
    entry.delete(first=0, last=None)
    # Above couple lines of codes is used to delete the character at index, or within the given range.
    # Use delete(0, End) to delete all text in the widget.
    # first: Start of range.
    # last: Optional end of range. If omitted, only a single character is removed.
    """
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        },
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        # is_ok = messagebox.askokcancel(title="Verify the Credential",
        #                                message=f"These are the details entered: \nEmail: {email} "
        #                                        f"\nPassword: {password} \nIs it ok to save?")
        # if is_ok:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Creating data.json for the first time and populating it with the new_data entered.
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# setting Icon
photo = PhotoImage(file="logo.png")
window.iconphoto(False, photo)
"""
Alternatively, we can set the icon as follows:
from PIL import Image, ImageTk

ico = Image.open("logo.png")
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

# if .ico file is present:
window.iconbitmap("myIcon.ico")
"""

# Canvas
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Label
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entry Box
"""
widget.grid(sticky="EW")
# Sticky: By default, when a cell is larger than the widget it contains, the grid geometry manager 
places the widget at the center of the cell horizontally and vertically. 
# To change this default behavior, you can use the sticky option. 
# The sticky option specifies which edge of the cell the widget should stick to.
# sticky="E"/"W"/"N"/"S"/"NW"/"NE"/"SE"/"SW"/
"NS": NS stretches the widget vertically. However, it leaves the widget centered horizontally.
"EW": EW stretches the widget horizontally. However, it leaves the widget centered vertically.
"""
website_entry = Entry(width=30)
website_entry.grid(row=1, column=1, columnspan=2, sticky="w")
website_entry.focus()

email_entry = Entry()
email_entry.insert(END, string="rohansingh0369@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")

password_entry = Entry(width=30)
password_entry.grid(row=3, column=1, sticky="w")

# Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="ew")

generate_password_button = Button(text="Generate Password", bg=LIGHT_GREEN, command=password_generator)
generate_password_button.grid(row=3, column=2, sticky="ew")

add_button = Button(text="Add", command=save, bg=LIGHT_YELLOW)
add_button.grid(row=4, column=1, columnspan=2, sticky="ew")

window.mainloop()
