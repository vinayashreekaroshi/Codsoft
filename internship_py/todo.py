import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, Toplevel
from tkcalendar import Calendar
from datetime import datetime
import json
import os

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

FILE = "tasks.json"

# -------- LOAD DATA --------
def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except:
            pass
    return {}

# -------- SAVE DATA --------
def save_data():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# -------- APP --------
app = ctk.CTk()
app.title("✨ Smart To-Do Manager")
app.geometry("520x650")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# -------- CLEAR --------
def clear():
    for widget in app.winfo_children():
        widget.destroy()

# -------- DASHBOARD --------
def dashboard():
    clear()

    frame = ctk.CTkFrame(app, corner_radius=20)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(frame, text="📅 Daily Planner",
                 font=("Arial", 24, "bold"))\
        .grid(row=0, column=0, pady=30)

    ctk.CTkButton(frame, text="➕ Schedule Task",
                  height=50, command=schedule_screen)\
        .grid(row=1, column=0, padx=40, pady=10, sticky="ew")

    ctk.CTkButton(frame, text="📅 View Today",
                  height=50, fg_color="#1f6aa5",
                  command=view_today)\
        .grid(row=2, column=0, padx=40, pady=10, sticky="ew")

    ctk.CTkButton(frame, text="📆 View by Date",
                  height=50, fg_color="#8e44ad",
                  command=view_by_date)\
        .grid(row=3, column=0, padx=40, pady=10, sticky="ew")

# -------- CALENDAR POPUP --------
def get_date_popup(entry):
    top = Toplevel(app)
    top.title("Select Date")
    top.geometry("320x300")
    top.configure(bg="white")

    cal = Calendar(
        top,
        date_pattern="yyyy-mm-dd",
        background="white",
        foreground="black",
        bordercolor="gray",
        headersbackground="#f0f0f0",
        headersforeground="black",
        selectbackground="#1f6aa5",
        normalbackground="white",
        normalforeground="black",
        weekendbackground="white",
        weekendforeground="black",
        othermonthbackground="#f5f5f5",
        othermonthforeground="gray"
    )
    cal.pack(pady=10)

    # Auto select on click
    def on_date_select(event):
        entry.delete(0, "end")
        entry.insert(0, cal.get_date())
        top.destroy()

    cal.bind("<<CalendarSelected>>", on_date_select)

# -------- SCHEDULE --------
def schedule_screen():
    clear()

    frame = ctk.CTkFrame(app, corner_radius=20)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(frame, text="📅 Schedule Task",
                 font=("Arial", 20, "bold"))\
        .grid(row=0, column=0, pady=15)

    date_entry = ctk.CTkEntry(frame, placeholder_text="Select Date")
    date_entry.grid(row=1, column=0, padx=40, pady=10, sticky="ew")

    ctk.CTkButton(frame, text="📅 Choose Date",
                  command=lambda: get_date_popup(date_entry))\
        .grid(row=2, column=0, pady=5)

    task_entry = ctk.CTkEntry(frame, placeholder_text="Enter task")
    task_entry.grid(row=3, column=0, padx=40, pady=10, sticky="ew")

    task_listbox = tk.Listbox(frame, height=8,
                              bg="#2b2b2b", fg="white",
                              selectbackground="#1f6aa5")
    task_listbox.grid(row=4, column=0, padx=40, pady=10, sticky="ew")

    # Add task (stay on same screen)
    def add_task():
        date = date_entry.get()
        task = task_entry.get()

        if not date or not task:
            messagebox.showwarning("Error", "Fill all fields!")
            return

        data.setdefault(date, []).append(task)
        save_data()

        task_listbox.insert(tk.END, "• " + task)
        task_entry.delete(0, "end")

    def finish():
        messagebox.showinfo("Saved", "Tasks saved ✅")
        dashboard()

    ctk.CTkButton(frame, text="➕ Add Task",
                  command=add_task)\
        .grid(row=5, column=0, pady=5)

    ctk.CTkButton(frame, text="✔ Done Adding",
                  fg_color="#27ae60",
                  command=finish)\
        .grid(row=6, column=0, pady=5)

    ctk.CTkButton(frame, text="⬅ Back",
                  fg_color="gray",
                  command=dashboard)\
        .grid(row=7, column=0, pady=10)

# -------- SHOW TASKS --------
def show_tasks_for_date(date):
    clear()

    frame = ctk.CTkFrame(app, corner_radius=20)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(frame, text=f"📅 {date}",
                 font=("Arial", 18, "bold"))\
        .grid(row=0, column=0, pady=10)

    listbox = tk.Listbox(frame, bg="#2b2b2b", fg="white",
                         selectbackground="#1f6aa5")
    listbox.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    if date not in data or not data[date]:
        ctk.CTkLabel(frame, text="No tasks 😴",
                     text_color="gray")\
            .grid(row=1, column=0, pady=10)
    else:
        for t in data[date]:
            listbox.insert(tk.END, "• " + t)

        def mark_done():
            try:
                i = listbox.curselection()[0]
                data[date].pop(i)

                if not data[date]:
                    del data[date]

                save_data()
                show_tasks_for_date(date)
            except:
                messagebox.showwarning("Error", "Select a task!")

        ctk.CTkButton(frame, text="✔ Complete",
                      fg_color="#27ae60",
                      command=mark_done)\
            .grid(row=3, column=0, pady=10)

    ctk.CTkButton(frame, text="⬅ Back",
                  fg_color="gray",
                  command=dashboard)\
        .grid(row=4, column=0, pady=10)

# -------- VIEW TODAY --------
def view_today():
    today = datetime.now().strftime("%Y-%m-%d")
    show_tasks_for_date(today)

# -------- VIEW BY DATE --------
def view_by_date():
    clear()

    frame = ctk.CTkFrame(app, corner_radius=20)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(frame, text="📆 Select Date",
                 font=("Arial", 18, "bold"))\
        .grid(row=0, column=0, pady=15)

    date_entry = ctk.CTkEntry(frame, placeholder_text="Select Date")
    date_entry.grid(row=1, column=0, padx=40, pady=10, sticky="ew")

    ctk.CTkButton(frame, text="📅 Choose Date",
                  command=lambda: get_date_popup(date_entry))\
        .grid(row=2, column=0, pady=5)

    def view():
        d = date_entry.get()
        if not d:
            messagebox.showwarning("Error", "Select date!")
        else:
            show_tasks_for_date(d)

    ctk.CTkButton(frame, text="View Tasks", command=view)\
        .grid(row=3, column=0, pady=10)

    ctk.CTkButton(frame, text="⬅ Back",
                  fg_color="gray", command=dashboard)\
        .grid(row=4, column=0, pady=10)

# -------- START --------
dashboard()
app.mainloop()