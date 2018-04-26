
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import wikipedia
from pytesseract import image_to_string
from PIL import Image
stop_words = set(stopwords.words('english'))

def get_question_and_answers_from_image(img_path):
    im = Image.open(img_path)
    crop_rectangle = (32, 269, 711, 446)
    cropped_im = im.crop(crop_rectangle)
    question = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    crop_rectangle = (81, 514,660, 606)
    cropped_im = im.crop(crop_rectangle)
    a1 = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    crop_rectangle = (83, 643, 660, 727)
    cropped_im = im.crop(crop_rectangle)
    a2 = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    crop_rectangle = (83, 771, 660, 854)
    cropped_im = im.crop(crop_rectangle)
    a3 = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    return question, (a1, a2, a3)

def remove_stop_words(string):
    out = []
    for word in string.split():
        if word.lower() not in stop_words:
            out.append(word)
    return " ".join(out)


def count_nouns(string):
    text = word_tokenize(string)
    t = pos_tag(text)
    nouns = sum(1 for i in t if i[1] == "NN" or i[1] == "NNS")
    proper_nouns = sum(1 for i in t if i[1] == "NNP" or i[1] == "NNPS")
    return 1 + nouns + (2 * proper_nouns)


def consecutive_groups(iterable):
    s = tuple(iterable)
    for size in range(1, len(s)+1):
        for index in range(len(s)+1-size):
            yield " ".join(iterable[index:index+size])


def search_wikipedia_first_result(phrase):
    try:
        return(wikipedia.page(wikipedia.search(phrase)[0]))
    except wikipedia.exceptions.DisambiguationError as e:
        print("ambiguous")
        return(wikipedia.page(e.options[0]))


def get_score(answer, q_substrings, results):
    page = search_wikipedia_first_result(answer)
    count = 0
    content = page.content.lower()
    # with open("results/{}.txt".format(answer), "w") as f:
    #     f.write("{}:\n".format(answer))
    for substr in q_substrings:
        score = content.count(substr.lower())
        count += score * len(substr.split()) * count_nouns(substr)
            # f.write("\t{}: {}\n".format(substr, score))
    count *= 1000
    count /= len(content)
    results[answer] = count
