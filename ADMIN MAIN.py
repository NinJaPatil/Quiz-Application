import json
from tkinter import *
from tkinter import messagebox as mb, ttk
from tkinter import Scrollbar, Canvas

def admin_login():
    admin_window = Tk()
    admin_window.title("Admin Login")
    admin_window.geometry("300x200")
    admin_window.configure(background="lightblue")

    label_username = ttk.Label(admin_window, text="Username:")  # Add this line
    label_username.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))

    entry_username = ttk.Entry(admin_window)
    entry_username.grid(row=0, column=1, padx=(20, 0), pady=(20, 0))

    label_password = ttk.Label(admin_window, text="Password:")
    label_password.grid(row=1, column=0, padx=(20, 0), pady=(20, 0))

    entry_password = ttk.Entry(admin_window, show="*")
    entry_password.grid(row=1, column=1, padx=(20, 0), pady=(20, 0))

    def authenticate():
        username = entry_username.get()
        password = entry_password.get()

        # Check if the entered username and password match the expected values
        if username == "admin" and password == "admin123":
            admin_window.destroy()
            open_admin_panel()
        else:
            mb.showerror("Error", "Invalid username or password")

    button_login = ttk.Button(admin_window, text="Login", command=authenticate)
    button_login.grid(row=2, column=0, columnspan=2, pady=10)  # Use grid instead of pack

    admin_window.mainloop()


def open_admin_panel():
    admin_panel = Tk()
    admin_panel.title("Admin Panel")
    admin_panel.geometry("300x200")
    admin_panel.configure(background="lightblue")

    label_title = Label(admin_panel, text="Welcome Admin!", font=("Arial", 14, "bold"))
    label_title.pack(pady=10)



    button_view_scores = ttk.Button(admin_panel, text="View Scores", command=view_scores)
    button_view_scores.pack(pady=5)


    button_edit_questions = ttk.Button(admin_panel, text="Add Questions", command=edit_questions)
    button_edit_questions.pack(pady=5)

    # Add a button for suggestions
    button_suggestions = ttk.Button(admin_panel, text="Suggestions", command=open_suggestions_file)
    button_suggestions.pack(pady=5)

    admin_panel.mainloop()


def open_suggestions_file():
    try:
        with open("suggestions.json", "r") as f:
            suggestions_data = [json.loads(line) for line in f.readlines()]

        suggestions_window = Tk()
        suggestions_window.title("Suggestions")
        suggestions_window.geometry("400x300")
        suggestions_window.configure(background="lightblue")

        title_label = Label(suggestions_window, text="User Suggestions", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        canvas = Canvas(suggestions_window)
        canvas.pack(side="left", fill="both", expand=True)

        scroll_y = Scrollbar(suggestions_window, orient="vertical", command=canvas.yview)
        scroll_y.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scroll_y.set)

        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Display suggestions
        for data in suggestions_data:
            suggestion_text = f"{data['username']}: {data['suggestion']}"
            suggestion_label = Label(frame, text=suggestion_text, font=("Arial", 12))
            suggestion_label.pack(pady=5, anchor='w')

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        suggestions_window.mainloop()

    except FileNotFoundError:
        mb.showerror("Error", "No suggestions found.")


def view_scores():
    try:
        with open('user_scores.json', 'r') as f:
            user_scores = json.load(f)
    except FileNotFoundError:
        mb.showerror("Error", "No scores found. Run the quiz to generate scores.")
        return
    except json.decoder.JSONDecodeError:
        mb.showerror("Error", "Invalid JSON format in user_scores.json.")
        return

    # Create the score window
    score_window = Tk()
    score_window.title("Scores")
    score_window.geometry("600x400")
    score_window.configure(background="lightblue")

    title_label = Label(score_window, text="User Scores", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Display scores
    display_scores(score_window, user_scores)

    score_window.mainloop()

def display_scores(score_window, user_scores):
    canvas = Canvas(score_window)
    canvas.pack(side="left", fill="both", expand=True)

    scroll_y = Scrollbar(score_window, orient="vertical", command=canvas.yview)
    scroll_y.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scroll_y.set)

    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Function to display scores in the desired format
    for username, data in user_scores.items():
        user_label = Label(frame, text=f"Username: {username}", font=("Arial", 14, "bold"))
        user_label.pack(pady=5, anchor='w')

        # Check if 'scores' is a string (invalid format), handle it gracefully
        if isinstance(data, str):
            mb.showerror("Error", f"Invalid data format for user '{username}'")
            continue

        if isinstance(data.get('scores'), str):
            mb.showerror("Error", f"Invalid 'scores' format for user '{username}'")
            continue

        for quiz, score_data in data.get('scores', {}).items():
            quiz_label = Label(frame, text=f"Quiz: {quiz}", font=("Arial", 12, "bold"))
            quiz_label.pack(pady=2, anchor='w')

            score_label = Label(frame, text=f"Score: {score_data['score']}%", font=("Arial", 12))
            score_label.pack(pady=2, anchor='w')

            difficulty_label = Label(frame, text=f"Difficulty: {score_data['difficulty']}", font=("Arial", 12))
            difficulty_label.pack(pady=2, anchor='w')

            time_label = Label(frame, text=f"Completion Time: {score_data['time']}", font=("Arial", 12))
            time_label.pack(pady=2, anchor='w')

            divider_label = Label(frame, text="--------------------------------------------")
            divider_label.pack(pady=5, anchor='w')

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def edit_questions():
    def save_question():
        global entry_question, entry_options, entry_answer, entry_difficulty, quiz_var
        question_text = entry_question.get().strip()
        options_text = entry_options.get().strip()
        correct_answer = entry_answer.get().strip().upper()
        difficulty = entry_difficulty.get().strip()

        if not question_text or not options_text or not correct_answer or not difficulty:
            mb.showerror("Error", "All fields must be filled!")
            return

        options = [option.strip() for option in options_text.split(',')]

        if correct_answer not in ['A', 'B', 'C', 'D']:
            mb.showerror("Error", "Correct answer must be A, B, C, or D.")

        answer_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4}

        selected_quiz = quiz_var.get()
        if not selected_quiz:
            mb.showerror("Error", "Please select a quiz!")
            return

        try:
            with open(selected_quiz, 'r') as f:
                questions_data = json.load(f)
        except FileNotFoundError:
            questions_data = {'question': [], 'options': [], 'answer': [], 'difficulty': []}

        formatted_options = [f"{chr(65 + i)}. {opt}" for i, opt in enumerate(options, start=0)]

        questions_data['question'].append(question_text)
        questions_data['options'].append(formatted_options)
        questions_data['answer'].append(answer_map[correct_answer])
        questions_data['difficulty'].append(difficulty)

        with open(selected_quiz, 'w') as f:
            json.dump(questions_data, f, indent=4)

        mb.showinfo("Success", "Question has been added/updated successfully!")

        entry_question.delete(0, END)
        entry_options.delete(0, END)
        entry_answer.delete(0, END)
        entry_difficulty.delete(0, END)

        return questions_data

    global entry_question, entry_options, entry_answer, entry_difficulty, quiz_var
    edit_window = Tk()
    edit_window.title("Edit Questions")
    edit_window.geometry("600x400")
    edit_window.configure(background="lightblue")

    quiz_files = ['Sports.json', 'GK.json', 'Technology.json']
    quiz_var = StringVar()
    quiz_var.set(quiz_files[0])
    quiz_dropdown = OptionMenu(edit_window, quiz_var, *quiz_files)
    quiz_dropdown.pack(pady=10)

    def update_selected_quiz_label(*args):
        selected_quiz_label.config(text="Selected Quiz: " + quiz_var.get())

    quiz_var.trace('w', update_selected_quiz_label)

    selected_quiz_label = ttk.Label(edit_window, text="Selected Quiz: " + quiz_var.get())
    selected_quiz_label.pack()

    label_question = ttk.Label(edit_window, text="Enter Question:")
    label_question.pack(pady=10)

    entry_question = ttk.Entry(edit_window, width=50)
    entry_question.pack(pady=5)

    label_options = ttk.Label(edit_window, text="Enter Options (comma-separated):")
    label_options.pack(pady=10)

    entry_options = ttk.Entry(edit_window, width=50)
    entry_options.pack(pady=5)

    label_answer = ttk.Label(edit_window, text="Enter Correct Answer (A, B, C, D):")
    label_answer.pack(pady=10)

    entry_answer = ttk.Entry(edit_window, width=50)
    entry_answer.pack(pady=5)

    label_difficulty = ttk.Label(edit_window, text="Enter Difficulty (Easy, Medium, Hard):")
    label_difficulty.pack(pady=10)

    entry_difficulty = ttk.Entry(edit_window, width=50)
    entry_difficulty.pack(pady=5)

    button_save = ttk.Button(edit_window, text="Save Question", command=save_question)
    button_save.pack(pady=10)


    edit_window.mainloop()

# Call the function to open the admin login window
admin_login()