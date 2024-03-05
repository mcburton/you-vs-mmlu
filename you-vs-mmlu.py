import marimo

__generated_with = "0.2.10"
app = marimo.App()


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        # You Vs. MMLU

        Test your knowledge against the [MMLU Benchmark (Hendrycks et al. 2020)](https://arxiv.org/abs/2009.03300).

        Answer the questions below to see how smart you are (and if you are smarter than a Large Language Model).
        """
    )
    return


@app.cell
def __(current_question, get_result, mo, show_buttons):
    mo.md(f"""
    **Question**

    {current_question["Question"]}

    **What is your answer?**

    {show_buttons()}

    Your answer is: { get_result() if get_result() else "*Click the button for your answer.*"}


    """)
    return


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
    questions = pd.read_csv("data.csv", header=None, names=columns)
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
def __(current_question, mo):
    get_result, set_result = mo.state("")

    def check_answer(button_value):
        if button_value == current_question["Answer"]:
            set_result("CORRECT!")
        else:
            return set_result("WRONG!")

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
