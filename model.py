from time import time
import operator
from threading import Thread
from os import system
import wikipedia
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from requests import get
from bs4 import BeautifulSoup
import helpers


class Model():
    def __init__(self):
        pass


class WikiModel(Model):

    def __init__(self, noun_coef=1.5, pnoun_coef=3, len_coef=2):
        self.NOUN_COEF = noun_coef  # noun importance
        self.PNOUN_COEF = pnoun_coef  # proper noun importance
        self.LEN_COEF = len_coef

    def predict(self, question, answers, mute, thread):
        q = helpers.remove_stop_words(question.replace("\"", "").replace("?", ""))
        q_substrings = list(helpers.consecutive_groups(q.split()))
        if not mute:
            print(question + "?\n")
        start = time()
        threads = []
        results = dict()
        for answer in answers:
            t = Thread(target=self.get_scores, args=(
                answer, q_substrings, results))
            threads.append(t)
            t.start()
        for i in range(len(threads)):
            threads[i].join()
        if not mute:
            for key, val in results.items():
                print("\t{0}: {1:.2f}".format(key, val))
            print("\nresults found in {} seconds.".format(time() - start))
        predicted_answer = max(results.items(), key=operator.itemgetter(1))[0]
        if not mute:
            system('say {}'.format(predicted_answer.replace("\'", "")))
        if results[predicted_answer] == 0:
            confidence = 0
        else: 
            confidence = results[predicted_answer] / sum([s for r, s in results.items()])
        thread["wiki"] =(predicted_answer, confidence) 
        return predicted_answer, confidence

    def get_scores(self, answer, q_substrings, results):
        page = helpers.search_wikipedia_first_result(answer)
        count = 0
        content = page.content.lower()
        for substr in q_substrings:
            score = content.count(substr.lower())
            count += (score + (self.count_nouns(substr) * score)) * \
                (self.LEN_COEF * len(substr.split()))
        count *= 1000
        count /= len(content)
        results[answer] = count

    def count_nouns(self, string):
        text = word_tokenize(string)
        t = pos_tag(text)
        nouns = sum(1 for i in t if i[1] == "NN" or i[1] == "NNS")
        proper_nouns = sum(1 for i in t if i[1] == "NNP" or i[1] == "NNPS")
        return (nouns * self.NOUN_COEF) + (self.PNOUN_COEF * proper_nouns)


class GoogleModel(Model):
    def __init__(self):
        pass

    def predict(self, question, answers, thread):
        results = dict()
        search_url = "https://www.google.com/search?q={}".format("+".join(question.split()))
        page = get(search_url)
        soup = BeautifulSoup(page.content)
        spans = soup.find_all('span', {'class' : 'st'})
        content = " ".join([span.get_text() for span in spans])
        for a in answers:
            c = content.lower().count(a.lower())
            results[a] = c
        predicted_answer = max(results.items(), key=operator.itemgetter(1))[0]
        # for r, s in results.items():
        #     print(r, s)
        # system('say {}'.format(predicted_answer.replace("\'", "")))
        if results[predicted_answer] == 0:
            confidence = 0
        else: 
            confidence = results[predicted_answer] / sum([s for r, s in results.items()])
        thread["google"] = (predicted_answer, confidence) 
        return predicted_answer, confidence

class WikiGoogle(Model):
    def __init__(self):
        self.w = WikiModel()
        self.g = GoogleModel()

    def predict(self, question, answers):
        threads = []
        results = dict()
        t1 = Thread(target=self.w.predict, args=(
                question, answers, True, results))
        threads.append(t1)
        t1.start()
        t2 = Thread(target=self.g.predict, args=(
                question, answers, results))
        threads.append(t2)
        t2.start()
        for i in range(len(threads)):
            threads[i].join()

        google_answer = results["google"]
        wiki_answer = results["wiki"]
        if wiki_answer[1] < 0.7 and google_answer[1] > 0:
            return google_answer
        else:
            return wiki_answer
        