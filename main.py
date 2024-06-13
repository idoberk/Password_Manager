import random
import pyperclip
import json
from tkinter import *
from tkinter import messagebox

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)

def generate_password():
	"""Generates a random password."""
	letters_list = [random.choice(letters) for _ in range(nr_letters)]
	numbers_list = [random.choice(numbers) for _ in range(nr_numbers)]
	symbols_list = [random.choice(symbols) for _ in range(nr_symbols)]

	password_list = letters_list + numbers_list + symbols_list

	random.shuffle(password_list)
	password = "".join(password_list)
	pyperclip.copy(password)
	password_entry.delete(0, END)
	password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
	"""Save website data into the txt file."""
	website = website_entry.get()
	user_name = user_name_entry.get()
	password = password_entry.get()
	new_data = {website: {
		"email": user_name,
		"password": password
	}}
	if website == "" or password == "" or user_name == "":
		messagebox.showwarning(title = "Oops", message = "Fields can't be empty!")
	else:
		try:
			with open("data.json", "r") as data_file:
				data = json.load(data_file)
		except FileNotFoundError:
			with open("data.json", "w") as data_file:
				json.dump(new_data, data_file, indent = 4)
		else:
			data.update(new_data)
			with open("data.json", "w") as data_file:
				json.dump(new_data, data_file, indent = 4)
		finally:
			website_entry.delete(0, END)
			password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
	website = website_entry.get()
	try:
		with open("data.json", "r") as data_file:
			data = json.load(data_file)
	except FileNotFoundError:
		messagebox.showwarning(title = "Error", message = "No Data File Found.")
	else:
		if website in data:
			email = data[website]["email"]
			password = data[website]["password"]
			messagebox.showinfo(title = website, message = f"Email: {email}\nPassword: {password}")
		else:
			messagebox.showinfo(title = "Error", message = f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx = 50, pady = 50)

# ------ BACKGROUND SETUP --------- #
canvas = Canvas(width = 200, height = 200)
background_img = PhotoImage(file = "logo.png")
canvas.create_image(100, 100, image = background_img)
canvas.grid(column = 1, row = 0)

# ------ LABEL SETUP --------- #
website_label = Label(text = "Website:")
website_label.grid(column = 0, row = 1)

user_name_label = Label(text = "Email/Username:")
user_name_label.grid(column = 0, row = 2)

password_label = Label(text = "Password:")
password_label.grid(column = 0, row = 3)

# ------ ENTRY SETUP --------- #
website_entry = Entry(width = 35)
website_entry.focus()
website_entry.grid(column = 1, row = 1, columnspan = 2, sticky = "EW")

user_name_entry = Entry(width = 35)
user_name_entry.grid(column = 1, row = 2, columnspan = 2, sticky = "EW")

password_entry = Entry(width = 21)
password_entry.grid(column = 1, row = 3, sticky = "EW")

# ------ BUTTON SETUP --------- #
password_generator_button = Button(text = "Generate Password", command = generate_password)
password_generator_button.grid(column = 2, row = 3, sticky = "EW")

search_button = Button(text = "Search", command = find_password)
search_button.grid(column = 2, row = 1, sticky = "EW")

add_password_button = Button(text = "Add", width = 35, command = save)
add_password_button.grid(column = 1, row = 4, columnspan = 2, sticky = "EW")

window.mainloop()