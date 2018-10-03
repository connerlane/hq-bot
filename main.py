from helpers import get_question_and_answers_from_image, get_question_and_answers_from_image_c
from pic_import import save_pic
from os import listdir, system
from model import WikiModel, WikiGoogle


w = WikiGoogle()
while True:

    input("ready?")
    save_pic()
    pic = "sc/" + sorted(listdir("sc")).pop()
    
    question, answers = get_question_and_answers_from_image(pic)
    # answers = ["star trek", "the jetsons", "doctor who"]
    
    predicted_answer = w.predict(question, answers)
    print(predicted_answer)
    system('say {}'.format(predicted_answer[0].replace("\'", "")))

    
