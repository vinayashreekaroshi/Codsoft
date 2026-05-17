import customtkinter as ctk
import random

# -------------------- APP SETTINGS --------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Rock Paper Scissors Game")
app.geometry("500x550")
app.resizable(False, False)

# -------------------- VARIABLES --------------------
choices = ["Rock", "Paper", "Scissors"]

user_score = 0
computer_score = 0

# -------------------- FUNCTIONS --------------------
def play(user_choice):
    global user_score, computer_score

    computer_choice = random.choice(choices)

    user_choice_label.configure(text=f"👤 You Chose: {user_choice}")
    computer_choice_label.configure(text=f"💻 Computer Chose: {computer_choice}")

    # Game Logic
    if user_choice == computer_choice:
        result = "🤝 It's a Tie!"
    elif (
        (user_choice == "Rock" and computer_choice == "Scissors")
        or (user_choice == "Paper" and computer_choice == "Rock")
        or (user_choice == "Scissors" and computer_choice == "Paper")
    ):
        result = "🎉 You Win!"
        user_score += 1
    else:
        result = "😢 Computer Wins!"
        computer_score += 1

    result_label.configure(text=result)

    score_label.configure(
        text=f"Your Score: {user_score}    |    Computer Score: {computer_score}"
    )

def reset_game():
    global user_score, computer_score

    user_score = 0
    computer_score = 0

    user_choice_label.configure(text="👤 You Chose: ")
    computer_choice_label.configure(text="💻 Computer Chose: ")
    result_label.configure(text="Choose Rock, Paper, or Scissors")
    score_label.configure(text="Your Score: 0    |    Computer Score: 0")

# -------------------- UI --------------------
title = ctk.CTkLabel(
    app,
    text="✊ Rock Paper Scissors ✂️",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)

instruction = ctk.CTkLabel(
    app,
    text="Select your choice below",
    font=("Arial", 16)
)
instruction.pack(pady=5)

# Buttons Frame
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)

rock_btn = ctk.CTkButton(
    button_frame,
    text="🪨 Rock",
    width=120,
    height=50,
    command=lambda: play("Rock")
)
rock_btn.grid(row=0, column=0, padx=10, pady=10)

paper_btn = ctk.CTkButton(
    button_frame,
    text="📄 Paper",
    width=120,
    height=50,
    command=lambda: play("Paper")
)
paper_btn.grid(row=0, column=1, padx=10, pady=10)

scissors_btn = ctk.CTkButton(
    button_frame,
    text="✂️ Scissors",
    width=120,
    height=50,
    command=lambda: play("Scissors")
)
scissors_btn.grid(row=0, column=2, padx=10, pady=10)

# Result Section
user_choice_label = ctk.CTkLabel(
    app,
    text="👤 You Chose: ",
    font=("Arial", 18)
)
user_choice_label.pack(pady=10)

computer_choice_label = ctk.CTkLabel(
    app,
    text="💻 Computer Chose: ",
    font=("Arial", 18)
)
computer_choice_label.pack(pady=10)

result_label = ctk.CTkLabel(
    app,
    text="Choose Rock, Paper, or Scissors",
    font=("Arial", 22, "bold"),
    text_color="cyan"
)
result_label.pack(pady=20)

score_label = ctk.CTkLabel(
    app,
    text="Your Score: 0    |    Computer Score: 0",
    font=("Arial", 18)
)
score_label.pack(pady=10)

# Reset Button
reset_btn = ctk.CTkButton(
    app,
    text="🔄 Reset Game",
    width=180,
    height=45,
    command=reset_game
)
reset_btn.pack(pady=25)

# -------------------- RUN APP --------------------
app.mainloop()