import customtkinter as ctk

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# App
app = ctk.CTk()
app.title("Basic Calculator")
app.geometry("350x500")

expression = ""

# Display
display = ctk.CTkEntry(app, font=("Poppins", 24), justify="right")
display.pack(padx=20, pady=20, fill="x")
display.focus()   # 👈 important for keyboard typing

# ---------------- FUNCTIONS ----------------
def press(num):
    global expression
    expression += str(num)
    display.delete(0, "end")
    display.insert("end", expression)

def clear():
    global expression
    expression = ""
    display.delete(0, "end")

def calculate():
    global expression
    try:
        result = str(eval(expression))
        display.delete(0, "end")
        display.insert("end", result)
        expression = result
    except:
        display.delete(0, "end")
        display.insert("end", "Error")
        expression = ""

# ---------------- KEYBOARD SUPPORT ----------------
def key_event(event):
    key = event.char

    if key in "0123456789+-*/.":
        press(key)

    elif key == "\r":  # Enter key
        calculate()

    elif key == "\x08":  # Backspace
        global expression
        expression = expression[:-1]
        display.delete(0, "end")
        display.insert("end", expression)

    elif key.lower() == "c":
        clear()

# Bind keyboard
app.bind("<Key>", key_event)

# ---------------- BUTTONS ----------------
frame = ctk.CTkFrame(app)
frame.pack(expand=True, fill="both", padx=10, pady=10)

buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

for i, row in enumerate(buttons):
    for j, char in enumerate(row):
        if char == "=":
            btn = ctk.CTkButton(
                frame, text=char, height=60,
                fg_color="#27ae60",
                command=calculate
            )
        else:
            btn = ctk.CTkButton(
                frame, text=char, height=60,
                command=lambda ch=char: press(ch)
            )

        btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

# Clear button
clear_btn = ctk.CTkButton(app, text="Clear", fg_color="#e74c3c", command=clear)
clear_btn.pack(pady=10, padx=20, fill="x")

# Grid config
for i in range(4):
    frame.grid_rowconfigure(i, weight=1)
    frame.grid_columnconfigure(i, weight=1)

app.mainloop()