import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 as sql

# Add task function
def add_task():
    task_string = task_field.get()
    if not task_string:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('INSERT INTO tasks (title, user_id) VALUES (?, ?)', (task_string, current_user_id))
        update_list()
        task_field.delete(0, 'end')
        connection.commit()

# Update the listbox with tasks
def update_list():
    task_listbox.delete(0, 'end')
    for task in tasks:
        task_listbox.insert('end', task)

# Delete selected task function
def delete_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        if selected_task in tasks:
            tasks.remove(selected_task)
            the_cursor.execute('DELETE FROM tasks WHERE title = ? AND user_id = ?', (selected_task, current_user_id))
            update_list()
            connection.commit()
    except tk.TclError:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

# Delete all tasks function
def delete_all_tasks():
    if messagebox.askyesno('Delete All', 'Are you sure?'):
        tasks.clear()
        the_cursor.execute('DELETE FROM tasks WHERE user_id = ?', (current_user_id,))
        update_list()
        connection.commit()

# Close application function
def close_app():
    guiWindow.destroy()

# Retrieve data from database
def retrieve_database():
    tasks.clear()
    for row in the_cursor.execute('SELECT title FROM tasks WHERE user_id = ?', (current_user_id,)):
        tasks.append(row[0])

# Login function
def login():
    global current_user_id
    username = username_entry.get()
    password = password_entry.get()
    user = the_cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    if user:
        current_user_id = user[0]
        login_frame.pack_forget()
        main_frame.pack(fill="both", expand=True)
        retrieve_database()
        update_list()
    else:
        messagebox.showinfo('Error', 'Invalid username or password.')

# Register function
def register():
    username = username_entry.get()
    password = password_entry.get()
    if the_cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone():
        messagebox.showinfo('Error', 'Username already exists.')
    else:
        the_cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        connection.commit()
        messagebox.showinfo('Success', 'User registered successfully.')
        login()

# Apply focus and hover effects to the entry field
def on_enter(event):
    event.widget.config(highlightbackground='#ADD8E6', highlightcolor='#ADD8E6', highlightthickness=2)  # LightBlue

def on_leave(event):
    event.widget.config(highlightthickness=0)

# Main function
if __name__ == "__main__":
    # Initialize GUI window
    guiWindow = tk.Tk()
    guiWindow.title("To-Do List Manager")
    guiWindow.geometry("500x450+750+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#F0F8FF")  # AliceBlue

    # Database connection
    connection = sql.connect('listOfTasks.db')
    the_cursor = connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, user_id INTEGER)')
    the_cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')

    tasks = []
    current_user_id = None

    # Login/Register frame
    login_frame = tk.Frame(guiWindow, bg="#F0F8FF")  # AliceBlue
    login_frame.pack(fill="both", expand=True)

    ttk.Label(login_frame, text="Login/Register", font=("Arial", 30), background="#F0F8FF", foreground="#5F9EA0").pack(padx=20, pady=20)  # CadetBlue
    
    ttk.Label(login_frame, text="Username:", font=("Arial", 11, "bold"), background="#F0F8FF").pack(padx=20, pady=5)
    username_entry = ttk.Entry(login_frame, font=("Arial", 12), width=18)
    username_entry.pack(padx=20, pady=5)
    username_entry.bind("<Enter>", on_enter)
    username_entry.bind("<Leave>", on_leave)
    
    ttk.Label(login_frame, text="Password:", font=("Arial", 11, "bold"), background="#F0F8FF").pack(padx=20, pady=5)
    password_entry = ttk.Entry(login_frame, font=("Arial", 12), width=18, show="*")
    password_entry.pack(padx=20, pady=5)
    password_entry.bind("<Enter>", on_enter)
    password_entry.bind("<Leave>", on_leave)
    
    ttk.Button(login_frame, text="Login", width=24, command=login).pack(padx=20, pady=5)
    ttk.Button(login_frame, text="Register", width=24, command=register).pack(padx=20, pady=5)

    # Main frame
    main_frame = tk.Frame(guiWindow, bg="#F0F8FF")  # AliceBlue

    header_frame = tk.Frame(main_frame, bg="#F0F8FF")  # AliceBlue
    functions_frame = tk.Frame(main_frame, bg="#F0F8FF")  # AliceBlue
    listbox_frame = tk.Frame(main_frame, bg="#F0F8FF")  # AliceBlue

    header_frame.pack(fill="both")
    functions_frame.pack(side="left", expand=True, fill="both")
    listbox_frame.pack(side="right", expand=True, fill="both")

    ttk.Label(header_frame, text="The To-Do List", font=("Arial", 30), background="#F0F8FF", foreground="#5F9EA0").pack(padx=20, pady=20)  # CadetBlue

    ttk.Label(functions_frame, text="Enter the Task:", font=("Arial", 11, "bold"), background="#F0F8FF").place(x=30, y=40)
    task_field = ttk.Entry(functions_frame, font=("Arial", 12), width=18)
    task_field.place(x=30, y=80)
    task_field.bind("<Enter>", on_enter)
    task_field.bind("<Leave>", on_leave)

    ttk.Button(functions_frame, text="Add Task", width=24, command=add_task).place(x=30, y=120)
    ttk.Button(functions_frame, text="Delete Task", width=24, command=delete_task).place(x=30, y=160)
    ttk.Button(functions_frame, text="Delete All Tasks", width=24, command=delete_all_tasks).place(x=30, y=200)
    ttk.Button(functions_frame, text="Exit", width=24, command=close_app).place(x=30, y=240)

    task_listbox = tk.Listbox(listbox_frame, width=26, height=13, selectmode='SINGLE', background="#FFFFFF", selectbackground="#5F9EA0")  # CadetBlue
    task_listbox.place(x=10, y=20)

    guiWindow.mainloop()
    connection.commit()
    the_cursor.close()
