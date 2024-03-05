import marimo

__generated_with = "0.2.10"
app = marimo.App()


@app.cell
def __(mo):
    mo.md(
        """
        # You Vs. MMLU

        Test your knowledge against the [MMLU Benchmark (Hendrycks et al. 2020)](https://arxiv.org/abs/2009.03300). This benchmark covers a variety of topic areas and tests the reasoning and understanding abilities of an undergraduate student (alledgedly...but I don't actually see that statement in the paper).

        This demo of the benchmark only includes the questions from the `miscellaneous_test.csv` questions from the MMLU [dataset on GitHub](https://github.com/hendrycks/test).
        """
    )
    return


@app.cell
def __(
    correct_answers,
    current_question,
    get_result,
    mo,
    score,
    show_buttons,
    total_questions,
):
    mo.md(f"""
    You have answered {total_questions} questions and gotten {correct_answers} correct.

    Your score is: {score}%

    **Question**

    {current_question["Question"]}



    **What is your answer?**

    {show_buttons()}

    Your answer is: { get_result() if get_result() else "*Click the button for your answer.*"}


    """)
    return


@app.cell
def __(mo):
    mo.md(
        """
        ---
        This is a very quick and dirty proof of concept. I want to add:

        - [x] computing the score
        - Adding a "leaderboard" to see how you compare to various LLMs
        - A way to track performance beyond individual sessions and possibly with groups (so a whole class could compete against an AI)
        - Add more MMLU topic and question sets
        - Clean up the code and make it less hacky
        """
    )
    return


@app.cell
def __(get_right_answers, get_wrong_answers):
    correct_answers = get_right_answers()
    incorrect_answers = get_wrong_answers()

    total_questions = correct_answers + incorrect_answers
    try:
        raw_score = correct_answers / total_questions
        score = round(raw_score * 100, 2)
    except ZeroDivisionError:
        score = "Answer some questions first!"

    return (
        correct_answers,
        incorrect_answers,
        raw_score,
        score,
        total_questions,
    )


@app.cell
def __(buttons, get_result, mo, next_question):
    def show_buttons():
        if get_result():
            return next_question
        else:
            return mo.vstack(buttons, align="start")
    return show_buttons,


@app.cell
def __(pd):
    columns = ["Question", "A", "B", "C", "D", "Answer"]
    # load csv with specified headers
    questions = pd.read_csv("https://raw.githubusercontent.com/mcburton/you-vs-mmlu/main/data.csv", header=None, names=columns)
    #questions
    return columns, questions


@app.cell
def __(mo):
    next_question = mo.ui.button(label="Next Question")
    return next_question,


@app.cell
def __(next_question, questions):
    next_question

    current_question = questions.sample(1).squeeze()
    #set_result(None)
    #current_question
    return current_question,


@app.cell
def __(mo):
    get_right_answers, set_right_answers = mo.state(0)
    get_wrong_answers, set_wrong_answers = mo.state(0)
    return (
        get_right_answers,
        get_wrong_answers,
        set_right_answers,
        set_wrong_answers,
    )


@app.cell
def __(
    current_question,
    get_right_answers,
    get_wrong_answers,
    mo,
    set_right_answers,
    set_wrong_answers,
):
    get_result, set_result = mo.state("")


    def check_answer(button_value):
        correct_answer = current_question[current_question["Answer"]]
        if button_value == current_question["Answer"]:
            set_result(f"CORRECT! The correct answer was {correct_answer}")
            set_right_answers(get_right_answers() + 1)
        else:
            set_result(f"WRONG! The correct answer was {correct_answer}")
            set_wrong_answers(get_wrong_answers() + 1)

    # hardcoding the buttons because I am trying to get this working quickly
    button_A = mo.ui.button(
        value = "A",
        label = f"A - {current_question['A']}",
        on_click = lambda value: check_answer(value),

    )
    button_B = mo.ui.button(
        value = "B",
        label = f"B - {current_question['B']}",
        on_click = lambda value: check_answer(value),
    )
    button_C = mo.ui.button(
        value = "C",
        label = f"C - {current_question['C']}",
        on_click = lambda value: check_answer(value),
    )
    button_D = mo.ui.button(
        value = "D",
        label = f"D - {current_question['D']}",
        on_click = lambda value: check_answer(value),
    )
    # this should be a list comprehension
    buttons = mo.ui.array([button_A, button_B, button_C, button_D])
    #buttons
    return (
        button_A,
        button_B,
        button_C,
        button_D,
        buttons,
        check_answer,
        get_result,
        set_result,
    )


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    return mo, pd


if __name__ == "__main__":
    app.run()
