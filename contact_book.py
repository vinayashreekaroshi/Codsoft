import customtkinter as ctk
from tkinter import messagebox, Listbox
import json
import os

# -------------------- APP SETTINGS --------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Contact Book")
app.geometry("900x650")
app.resizable(False, False)

# -------------------- FILE --------------------
FILE_NAME = "contacts.json"

# -------------------- FUNCTIONS --------------------
def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_contacts():
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)

contacts = load_contacts()

def clear_fields():
    name_entry.delete(0, "end")
    phone_entry.delete(0, "end")
    email_entry.delete(0, "end")
    address_entry.delete("1.0", "end")

def refresh_contacts():
    contact_list.delete(0, "end")

    for contact in contacts:
        contact_list.insert(
            "end",
            f"{contact['name']} - {contact['phone']}"
        )

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get("1.0", "end").strip()

    if name == "" or phone == "":
        messagebox.showerror("Error", "Name and Phone are required!")
        return

    contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }

    contacts.append(contact)
    save_contacts()
    refresh_contacts()
    clear_fields()

    messagebox.showinfo("Success", "Contact Added Successfully!")

def show_contact(event):
    selected = contact_list.curselection()

    if not selected:
        return

    index = selected[0]
    contact = contacts[index]

    clear_fields()

    name_entry.insert(0, contact["name"])
    phone_entry.insert(0, contact["phone"])
    email_entry.insert(0, contact["email"])
    address_entry.insert("1.0", contact["address"])

def update_contact():
    selected = contact_list.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a contact to update!")
        return

    index = selected[0]

    contacts[index] = {
        "name": name_entry.get(),
        "phone": phone_entry.get(),
        "email": email_entry.get(),
        "address": address_entry.get("1.0", "end").strip()
    }

    save_contacts()
    refresh_contacts()

    messagebox.showinfo("Updated", "Contact Updated Successfully!")

def delete_contact():
    selected = contact_list.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a contact to delete!")
        return

    index = selected[0]

    confirm = messagebox.askyesno(
        "Delete",
        "Are you sure you want to delete this contact?"
    )

    if confirm:
        contacts.pop(index)
        save_contacts()
        refresh_contacts()
        clear_fields()

        messagebox.showinfo("Deleted", "Contact Deleted Successfully!")

def search_contact():
    keyword = search_entry.get().lower()

    contact_list.delete(0, "end")

    for contact in contacts:
        if (
            keyword in contact["name"].lower()
            or keyword in contact["phone"]
        ):
            contact_list.insert(
                "end",
                f"{contact['name']} - {contact['phone']}"
            )

# -------------------- TITLE --------------------
title = ctk.CTkLabel(
    app,
    text="📒 Contact Book",
    font=("Arial", 30, "bold")
)
title.pack(pady=15)

# -------------------- MAIN FRAME --------------------
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# -------------------- LEFT FRAME --------------------
left_frame = ctk.CTkFrame(main_frame, width=300)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

search_label = ctk.CTkLabel(
    left_frame,
    text="🔍 Search Contact",
    font=("Arial", 18, "bold")
)
search_label.pack(pady=10)

search_entry = ctk.CTkEntry(
    left_frame,
    width=250,
    placeholder_text="Enter name or phone"
)
search_entry.pack(pady=5)

search_btn = ctk.CTkButton(
    left_frame,
    text="Search",
    command=search_contact
)
search_btn.pack(pady=10)

# -------------------- CONTACT LIST --------------------
contact_list = Listbox(
    left_frame,
    width=35,
    height=20,
    font=("Arial", 12),
    bg="#2b2b2b",
    fg="white",
    selectbackground="#1f6aa5",
    relief="flat"
)

contact_list.pack(pady=10)
contact_list.bind("<<ListboxSelect>>", show_contact)

# -------------------- RIGHT FRAME --------------------
right_frame = ctk.CTkFrame(main_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Name
name_label = ctk.CTkLabel(
    right_frame,
    text="Name",
    font=("Arial", 16)
)
name_label.pack(anchor="w", padx=20, pady=(20, 5))

name_entry = ctk.CTkEntry(
    right_frame,
    width=400,
    height=40
)
name_entry.pack(padx=20)

# Phone
phone_label = ctk.CTkLabel(
    right_frame,
    text="Phone Number",
    font=("Arial", 16)
)
phone_label.pack(anchor="w", padx=20, pady=(15, 5))

phone_entry = ctk.CTkEntry(
    right_frame,
    width=400,
    height=40
)
phone_entry.pack(padx=20)

# Email
email_label = ctk.CTkLabel(
    right_frame,
    text="Email",
    font=("Arial", 16)
)
email_label.pack(anchor="w", padx=20, pady=(15, 5))

email_entry = ctk.CTkEntry(
    right_frame,
    width=400,
    height=40
)
email_entry.pack(padx=20)

# Address
address_label = ctk.CTkLabel(
    right_frame,
    text="Address",
    font=("Arial", 16)
)
address_label.pack(anchor="w", padx=20, pady=(15, 5))

address_entry = ctk.CTkTextbox(
    right_frame,
    width=400,
    height=100
)
address_entry.pack(padx=20)

# -------------------- BUTTONS --------------------
button_frame = ctk.CTkFrame(right_frame)
button_frame.pack(pady=25)

add_btn = ctk.CTkButton(
    button_frame,
    text="➕ Add Contact",
    width=140,
    command=add_contact
)
add_btn.grid(row=0, column=0, padx=10, pady=10)

update_btn = ctk.CTkButton(
    button_frame,
    text="✏️ Update",
    width=140,
    command=update_contact
)
update_btn.grid(row=0, column=1, padx=10, pady=10)

delete_btn = ctk.CTkButton(
    button_frame,
    text="🗑 Delete",
    width=140,
    command=delete_contact
)
delete_btn.grid(row=1, column=0, padx=10, pady=10)

clear_btn = ctk.CTkButton(
    button_frame,
    text="🧹 Clear",
    width=140,
    command=clear_fields
)
clear_btn.grid(row=1, column=1, padx=10, pady=10)

# -------------------- LOAD CONTACTS --------------------
refresh_contacts()

# -------------------- RUN APP --------------------
app.mainloop()