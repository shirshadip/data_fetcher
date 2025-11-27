import tkinter as tk 
import database

root = tk.Tk()
root.geometry("900x800")
options = ["create a new database","work with existing database"]

# StringVar to store selected value
selected = tk.StringVar()
selected.set(options[0])   # default value

# Create dropdown
dropdown = tk.OptionMenu(root, selected, *options)
dropdown.config(height=5,width=40,bg="red",fg="grey")
dropdown.pack(pady=20,padx=10)

db_label = tk.Label(root, text="Enter the database name you want to connect")
db_label.pack()

db_name = tk.Entry(root)
db_name.pack()

pas_label = tk.Label(root, text="Enter your password of database")
pas_label.pack()

pas = tk.Entry(root, show="*")  # optional: hide password
pas.pack()

def create():
    # Get text from entries
    db = db_name.get()
    password = pas.get()

    # Pass actual values
    database.database(password, db)

db_btn = tk.Button(root, text="connect database", command=create)
db_btn.pack()

root.mainloop()
