from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(text=f"Score: 0", bg=THEME_COLOR, fg="white", font=("Arial", 12, "normal"))
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg="white", highlightthickness=0)
        self.question_series = self.canvas.create_text(150, 125, text="Questions Coming Up",
                                                       font=("Arial", 16, "italic"),
                                                       fill="black",
                                                       width=280
                                                       )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        true_img = PhotoImage(file="images/true.png")
        false_img = PhotoImage(file="images/false.png")

        self.true = Button(image=true_img, bg=THEME_COLOR,
                           highlightthickness=0, borderwidth=0, command=self.true_guess)
        self.false = Button(image=false_img, bg=THEME_COLOR,
                            highlightthickness=0, borderwidth=0, command=self.wrong_guess)
        self.true.grid(row=2, column=0)
        self.false.grid(row=2, column=1)

        self.bring_up_question()

        self.window.mainloop()

    def bring_up_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_series, text=q_text)
        else:
            self.canvas.itemconfig(self.question_series, text="You have reached to the end of the quiz.")
            self.true.config(state="disabled")
            self.false.config(state="disabled")

    def true_guess(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def wrong_guess(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_true):
        if is_true:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.bring_up_question)
