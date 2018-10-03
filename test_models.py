from model import WikiModel, GoogleModel, WikiGoogle
from json import load
from pathlib import Path

def get_accuracy(model, questions):
    correct = 0
    for question in questions:
        pred = model.predict(question, [questions[question]["a1"], questions[question]["a2"], questions[question]["a3"]])
        print(pred)
        if pred[0] == questions[question]["correct"]:
            correct += 1
    return correct / len(questions)


def load_questions():
    table_file = Path("record.json")
    if table_file.exists():
        d = load(open('record.json'))
        return d
    return dict()


if __name__ == "__main__":
    n_co = [0.5, 1.5]
    pn_co = [3, 4]
    len_co = [2]


    questions = load_questions()

    m = WikiGoogle()
    print(get_accuracy(m, questions))
    # with open("results.txt", "w") as f:
    #     f.write("results:\n")
    # for n in n_co:
    #     for p in pn_co:
    #         for l in len_co:
    #             m = WikiModel(n, p, l)
    #             with open("results.txt", "a") as f:
    #                 r = "n:{} p:{} l:{} accuracy: {}".format(n, p, l, get_accuracy(m, questions))
    #                 f.write(r + "\n")

