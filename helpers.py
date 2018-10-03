
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
    crop_rectangle = (81, 514, 660, 606)
    cropped_im = im.crop(crop_rectangle)
    a1 = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    crop_rectangle = (83, 643, 660, 727)
    cropped_im = im.crop(crop_rectangle)
    a2 = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    crop_rectangle = (83, 771, 660, 854)
    cropped_im = im.crop(crop_rectangle)
    a3 = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    return question, (a1, a2, a3)

def get_question_and_answers_from_image_c(img_path):
    im = Image.open(img_path)
    crop_rectangle = (39, 197, 716, 507)
    cropped_im = im.crop(crop_rectangle)
    question = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    crop_rectangle = (85, 555, 660, 642)
    cropped_im = im.crop(crop_rectangle)
    a1 = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    crop_rectangle = (83, 700, 660, 790)
    cropped_im = im.crop(crop_rectangle)
    a2 = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    crop_rectangle = (83, 845, 660, 931)
    cropped_im = im.crop(crop_rectangle)
    a3 = image_to_string(cropped_im, lang='eng').replace("\n", " ")
    return question, (a1, a2, a3)

def remove_stop_words(string):
    out = []
    for word in string.split():
        if word.lower() not in stop_words:
            out.append(word)
    return " ".join(out)

def get_proper_nouns(string):
    text = word_tokenize(string)
    t = pos_tag(text)
    return [i[0] for i in t if i[1] == "NNP" or i[1] == "NNPS"]

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
