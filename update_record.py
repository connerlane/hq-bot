from json import load, dump
from pathlib import Path
from helpers import get_question_and_answers_from_image
from os import listdir


def load_questions():
    table_file = Path("record.json")
    if table_file.exists():
        d = load(open('record.json'))
        return d
    return dict()

def write_questions(questions):
    with open("record.json", "w") as f:
        dump(questions, f)

questions = load_questions()
images = sorted(listdir("sc"))
try: 
    for image in images:
        question, answers = get_question_and_answers_from_image("sc/" + image)
        if question not in questions:
            print(question)
            for i, answer in enumerate(answers):
                print("\t" + str(i + 1) + ": " + answer)
            add = input("want to add? ")
            if add.lower() == "y":
                c = int(input("which is correct? (1, 2, 3): "))
                questions[question] = dict()
                questions[question]["a1"] = answers[0]
                questions[question]["a2"] = answers[1]
                questions[question]["a3"] = answers[2]
                questions[question]["correct"] = answers[c - 1]
    write_questions(questions)
except KeyboardInterrupt:
    i = input("write? ")
    if i.lower() == "y":
        write_questions(questions)




