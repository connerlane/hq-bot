from helpers import remove_stop_words, consecutive_groups, search_wikipedia_first_result, count_nouns, get_score, get_question_and_answers_from_image
from threading import Thread
from time import time
from pic_import import save_pic
from os import listdir, system
import operator
while True:

    input("ready?")
    save_pic()
    pic = "sc/" + sorted(listdir("sc")).pop()
    
    question, answers = get_question_and_answers_from_image(pic)
    question = question.replace("?", "")
    # answers = ["star trek", "the jetsons", "doctor who"]
    
    if "“" in question:
        q = question
    else:
        q = remove_stop_words(question)

    with open("results.txt", "w") as f:
        f.write("results:\n")
    q_substrings = list(consecutive_groups(q.split()))
    print(question + "?\n")
    start = time()
    threads = []
    results = dict()
    for answer in answers:
        t = Thread(target=get_score, args=(answer, q_substrings, results))
        threads.append(t)
        t.start()
    for i in range(len(threads)):
        threads[i].join()

    for key, val in results.items():
        print("\t{0}: {1:.2f}".format(key, val))
    print("\nresults found in {} seconds.".format(time() - start))
    system('say {}'.format(max(results.items(), key=operator.itemgetter(1))[0]).replace("\'", ""))
