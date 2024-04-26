import json
from tkinter import *
from tkinter import messagebox as mb, ttk
import time
import random

class Quiz:
    def __init__(self, username, gui, quiz_data, quiz_type, difficulty):
        self.username = username
        self.q_no = 0
        self.gui = gui
        self.display_title()
        self.data = quiz_data
        self.quiz_type = quiz_type
        self.difficulty = difficulty
        self.filter_questions_by_difficulty()
        self.shuffle_questions()
        self.display_question()
        self.opt_selected = IntVar()
        self.opts = self.radio_buttons()
        self.display_options()
        self.buttons()
        self.correct = 0
        self.start_time = None
        self.timer_label = None
        self.start_timer()
        self.first_click = True

    def start_timer(self):
        self.start_time = time.time()
        self.timer_label = Label(self.gui, text="Time Left: 15", font=("Arial", 12))
        self.timer_label.place(x=70, y=450)
        self.update_timer()

    def update_timer(self):
        if self.start_time is not None:
            elapsed_time = int(time.time() - self.start_time)
            time_left = max(15 - elapsed_time, 0)
            self.timer_label.config(text=f"Time Left: {time_left}")
            if time_left > 0:
                self.timer_label.after(1000, self.update_timer)
            else:
                self.next_btn()

    def filter_questions_by_difficulty(self):
        filtered_data = {
            'question': [],
            'options': [],
            'answer': []
        }
        for i in range(len(self.data['question'])):
            if self.data['difficulty'][i] == self.difficulty:
                filtered_data['question'].append(self.data['question'][i])
                filtered_data['options'].append(self.data['options'][i])
                filtered_data['answer'].append(self.data['answer'][i])
        self.data = filtered_data

    def shuffle_questions(self):
        combined = list(zip(self.data['question'], self.data['options'], self.data['answer']))
        random.shuffle(combined)
        self.data['question'], self.data['options'], self.data['answer'] = zip(*combined)

    def display_result(self):
        result_window = Toplevel(self.gui)
        result_window.title("Result")
        result_window.geometry("500x400")

        wrong_count = len(self.data['question']) - self.correct
        score = int(self.correct / len(self.data['question']) * 100)

        # Calculate grade based on score
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"

        result = f"Score: {score}%\nGrade: {grade}\nCorrect: {self.correct}\nWrong: {wrong_count}"
        result_label = Label(result_window, text=result, font=("Arial", 16))
        result_label.pack(pady=20)

        def close_result_window():
            result_window.destroy()
            self.destroy_gui()

        okay_button = ttk.Button(result_window, text="Okay", command=close_result_window)
        okay_button.pack(pady=10)

        leaderboard_button = ttk.Button(result_window, text="Leaderboard", command=open_leaderboard)
        leaderboard_button.pack(pady=10)

        def open_suggestion_window():
            suggestion_window = Toplevel(result_window)
            suggestion_window.title("Suggestions")
            suggestion_window.geometry("400x200")

            suggestion_label = Label(suggestion_window, text="Enter your suggestions:", font=("Arial", 14),)
            suggestion_label.pack(pady=10)

            suggestion_entry = Entry(suggestion_window, width=50)
            suggestion_entry.pack(pady=10)

            def save_suggestion():
                suggestion_text = suggestion_entry.get()
                with open("suggestions.json", "a") as f:
                    suggestion_data = {"username": self.username, "suggestion": suggestion_text}
                    json.dump(suggestion_data, f)
                    f.write("\n")
                mb.showinfo("Success", "Thank you for your suggestion!")
                suggestion_window.destroy()
                close_result_window()

            submit_button = ttk.Button(suggestion_window, text="Submit", command=save_suggestion)
            submit_button.pack(pady=10)

            suggestion_window.mainloop()

        suggestion_button = ttk.Button(result_window, text="Suggestion", command=open_suggestion_window)
        suggestion_button.pack(pady=10)

        result_window.mainloop()

    def destroy_gui(self):
        if self.gui:
            self.gui.destroy()
            self.gui = None

    def display_correct_and_selected(self):
        correct_option = self.data['answer'][self.q_no]
        selected_option = self.opt_selected.get()
        for index, option in enumerate(self.opts):
            if index + 1 == correct_option:
                option.config(fg='green')
            if index + 1 == selected_option:
                if selected_option == correct_option:
                    option.config(fg='green')
                else:
                    option.config(fg='red')

    def clear_option_color(self):
        for option in self.opts:
            option.config(fg='black')

    def buttons(self):
        next_button = Button(self.gui, text="Next", command=self.next_btn,
                             width=10, bg="blue", fg="white", font=("Arial", 16, "bold"))
        next_button.place(x=650, y=800)
        quit_button = Button(self.gui, text="Quit", command=self.quit_btn,
                             width=5, bg="black", fg="white", font=("Arial", 16, "bold"))
        quit_button.place(x=1300, y=900)

    def display_options(self):
        val = 0
        self.opt_selected.set(0)
        for option in self.data['options'][self.q_no]:
            self.opts[val]['text'] = option
            self.opts[val]['fg'] = 'black'
            val += 1

    def display_question(self):
        q_no = Label(self.gui, text=self.data['question'][self.q_no], width=90,
                     font=('Arial', 16, 'bold'), anchor='w')
        q_no.place(x=90, y=100)
        self.update_question_label()

    def display_title(self):
        title = Label(self.gui, text="Mind Crafter's QUIZ",
                      width=90, bg="red", fg="white", font=("Arial", 20, "bold"))
        title.place(x=0, y=2)

    def radio_buttons(self):
        q_list = []
        y_pos = 200
        while len(q_list) < 4:
            radio_btn = Radiobutton(self.gui, text=" ", variable=self.opt_selected,
                                    value=len(q_list) + 1, font=("Arial", 14))
            q_list.append(radio_btn)
            radio_btn.place(x=100, y=y_pos)
            y_pos += 40
        return q_list

    def save_score(self, score):
        try:
            with open('user_scores.json', 'r') as f:
                user_scores = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            user_scores = {}

        if self.username not in user_scores:
            user_scores[self.username] = {'scores': {}}

        user_scores[self.username]['scores'][self.quiz_type] = {'score': score,
                                                                'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                                                                'quiz_type': self.quiz_type,
                                                                'difficulty': self.difficulty}

        with open('user_scores.json', 'w') as f:
            json.dump(user_scores, f)

    def update_question_label(self):
        question_label = Label(self.gui, text=f"Question {self.q_no + 1}/{len(self.data['question'])}",
                               font=("Arial", 12))
        question_label.place(x=70, y=420)

    def next_btn(self):
        if self.first_click:
            if self.q_no < len(self.data['question']):
                if self.check_ans(self.q_no):
                    self.correct += 1
                self.display_correct_and_selected()
                self.first_click = False
        else:
            self.gui.after(3000, self.clear_option_color)
            self.q_no += 1
            self.first_click = True
            if self.q_no < len(self.data['question']):
                self.display_question()
                self.display_options()
                self.update_question_label()
                self.start_timer()
            else:
                self.display_result()
                self.save_score(self.correct * 100 // len(self.data['question']))
                if self.gui:
                    self.gui.withdraw()
                    self.gui.after(100, self.destroy_gui)

    def check_ans(self, q_no):
        if self.opt_selected.get() == self.data['answer'][q_no]:
            return True

    def quit_btn(self):
        if self.gui:
            self.gui.destroy()
            self.gui = None

def start_quiz(username, quiz_choice, difficulty):
    global gui_login
    gui_login.destroy()
    gui = Tk()
    gui.attributes("-fullscreen", True)
    gui.title("Mind Crafter's Quiz")

    with open(quiz_choice) as f:
        quiz_data = json.load(f)

    quiz_type = quiz_choice.split('.')[0]
    quiz = Quiz(username, gui, quiz_data, quiz_type, difficulty)

def login():
    global entry_username, quiz_choice, difficulty_var
    username = entry_username.get().strip()
    if username:
        difficulty = difficulty_var.get()
        if quiz_choice.get() == 1:
            start_quiz(username, 'Sports.json', difficulty)
        elif quiz_choice.get() == 2:
            start_quiz(username, 'GK.json', difficulty)
        elif quiz_choice.get() == 3:
            start_quiz(username, 'Technology.json', difficulty)
        else:
            mb.showerror("Error", "Please select a quiz type!")
    else:
        mb.showerror("Error", "Username cannot be empty!")

def start_login():
    global gui_rule, gui_login, difficulty_var
    gui_rule.destroy()
    gui_login = Tk()
    gui_login.title("Login")
    gui_login.geometry("500x300")
    gui_login.configure(background="lightblue")  # Set background color here


    label_username = ttk.Label(gui_login, text="Username:")
    label_username.grid(row=0, column=0, pady=10, padx=10, sticky="w")


    global entry_username
    entry_username = ttk.Entry(gui_login, width=30)
    entry_username.grid(row=0, column=1, pady=5, padx=10, sticky="w")

    global quiz_choice
    quiz_choice = IntVar()
    label_quiz = Label(gui_login, text="Choose a Quiz Type:")
    label_quiz.grid(row=1, column=0, pady=10, padx=10, sticky="w")

    ttk.Radiobutton(gui_login, text="Sports", variable=quiz_choice, value=1).grid(row=2, column=0, pady=5, padx=10, sticky="w")
    ttk.Radiobutton(gui_login, text="GK", variable=quiz_choice, value=2).grid(row=3, column=0, pady=5, padx=10, sticky="w")
    ttk.Radiobutton(gui_login, text="Technology", variable=quiz_choice, value=3).grid(row=4, column=0, pady=5, padx=10, sticky="w")

    label_difficulty = Label(gui_login, text="Choose Difficulty:")
    label_difficulty.grid(row=5, column=0, pady=10, padx=10, sticky="w")

    difficulty_var = StringVar()
    difficulty_var.set("Easy")
    difficulty_choices = ["Easy", "Medium", "Hard"]
    difficulty_menu = OptionMenu(gui_login, difficulty_var, *difficulty_choices)
    difficulty_menu.grid(row=5, column=1, pady=5, padx=10, sticky="w")

    button_login = ttk.Button(gui_login, text="Start Quiz", width=15, command=login)
    button_login.grid(row=6, column=0, pady=10, padx=10, sticky="w")

    leaderboard_button = ttk.Button(gui_login, text="Leaderboard", command=open_leaderboard)
    leaderboard_button.grid(row=6, column=1, pady=10, padx=10, sticky="w")

    gui_login.mainloop()

def start():
    global gui_rule
    gui_rule = Tk()
    gui_rule.title("Rules")
    gui_rule.geometry("800x400")
    gui_rule.configure(background="lightblue")  # Set background color here

    rules = '''
    Welcome to the Mind Crafter's Quiz!

    Rules:
    1. This quiz contains multiple choice questions.
    2. You will have 15 seconds to answer each question.
    3. Once you select an option, click 'Next' to move to the next question.
    4. There is no negative marking.
    5. The quiz will be automatically submitted when you finish all questions or when time runs out.
    6. Have fun and test your knowledge!

    Choose a quiz type, enter your username, and click 'Start Quiz' to begin.

    Good Luck!
    '''

    label = Label(gui_rule, text=rules, justify=LEFT, font=("Arial", 14),bg="lightblue")
    label.pack(pady=20, padx=20)

    start_button = ttk.Button(gui_rule, text="Start Quiz", width=15,  command=start_login )
    start_button.pack()

    gui_rule.mainloop()


def open_leaderboard():
    leaderboard_window = Tk()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("600x400")
    leaderboard_window.configure(background="lightblue")  # Set background color here

    leaderboard_label = Label(leaderboard_window, text="Leaderboard", font=("Arial", 16))
    leaderboard_label.grid(row=0, column=0, columnspan=3, pady=20)

    try:
        with open('user_scores.json', 'r') as f:
            user_scores = json.load(f)

        top_scores = {}

        for username, data in user_scores.items():
            for quiz_type, score_data in data['scores'].items():
                score = score_data['score']
                difficulty = score_data['difficulty']
                if difficulty == 'Hard':
                    if quiz_type not in top_scores:
                        top_scores[quiz_type] = [(username, score)]
                    else:
                        top_scores[quiz_type].append((username, score))
                        top_scores[quiz_type].sort(key=lambda x: x[1], reverse=True)
                        top_scores[quiz_type] = top_scores[quiz_type][:2]

        row_index = 1

        for quiz_type, scores in top_scores.items():
            quiz_type_label = Label(leaderboard_window, text=quiz_type, font=("Arial", 12))
            quiz_type_label.grid(row=row_index, column=0, padx=10, sticky='w')
            for rank, (username, score) in enumerate(scores, start=1):
                user_score_label = Label(leaderboard_window, text=f"{rank}. {username}: {score}", font=("Arial", 12))
                user_score_label.grid(row=row_index, column=rank, padx=10, sticky='w')
            row_index += 1

    except FileNotFoundError:
        mb.showerror("Error", "Leaderboard data file not found!")
    except json.decoder.JSONDecodeError:
        mb.showerror("Error", "Error decoding leaderboard data!")

    leaderboard_window.mainloop()

if __name__ == "__main__":
    start()
