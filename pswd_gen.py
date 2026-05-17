import customtkinter as ctk
import random
import string

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# App
app = ctk.CTk()
app.title("Password Generator")
app.geometry("420x480")

# ---------------- FUNCTIONS ----------------
def generate_password():
    length = int(length_slider.get())

    chars = string.ascii_lowercase

    if upper_var.get():
        chars += string.ascii_uppercase
    if digit_var.get():
        chars += string.digits
    if symbol_var.get():
        chars += string.punctuation

    if not chars:
        result_entry.delete(0, "end")
        result_entry.insert(0, "Select options")
        return

    password = ''.join(random.choice(chars) for _ in range(length))

    result_entry.delete(0, "end")
    result_entry.insert(0, password)


def copy_password():
    app.clipboard_clear()
    app.clipboard_append(result_entry.get())

# ---------------- UI ----------------

main_frame = ctk.CTkFrame(app, corner_radius=20)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Title
title = ctk.CTkLabel(
    main_frame,
    text="🔐 Password Generator",
    font=("Segoe UI", 20, "bold")
)
title.pack(pady=(20, 10))

# Result box
result_entry = ctk.CTkEntry(
    main_frame,
    font=("Segoe UI", 16),
    height=45,
    justify="center",
    corner_radius=10
)
result_entry.pack(padx=20, pady=10, fill="x")

# Slider label
length_label = ctk.CTkLabel(main_frame, text="Length: 8")
length_label.pack(pady=(10, 0))

def update_length(value):
    length_label.configure(text=f"Length: {int(value)}")

# Slider
length_slider = ctk.CTkSlider(
    main_frame,
    from_=4,
    to=20,
    command=update_length
)
length_slider.set(8)
length_slider.pack(padx=20, pady=10, fill="x")

# Options frame
options_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
options_frame.pack(pady=10)

upper_var = ctk.BooleanVar()
digit_var = ctk.BooleanVar()
symbol_var = ctk.BooleanVar()

ctk.CTkCheckBox(options_frame, text="Uppercase", variable=upper_var).grid(row=0, column=0, padx=10)
ctk.CTkCheckBox(options_frame, text="Numbers", variable=digit_var).grid(row=0, column=1, padx=10)
ctk.CTkCheckBox(options_frame, text="Symbols", variable=symbol_var).grid(row=0, column=2, padx=10)

# Generate button
generate_btn = ctk.CTkButton(
    main_frame,
    text="Generate",
    height=45,
    corner_radius=12,
    command=generate_password
)
generate_btn.pack(padx=20, pady=15, fill="x")

# Copy button
copy_btn = ctk.CTkButton(
    main_frame,
    text="Copy",
    height=40,
    fg_color="#2ecc71",
    hover_color="#27ae60",
    corner_radius=12,
    command=copy_password
)
copy_btn.pack(padx=20, pady=(0, 20), fill="x")

# Run
app.mainloop()