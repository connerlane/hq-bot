from PIL import Image
from pytesseract import image_to_string
input("ready")
print(image_to_string(Image.open('question.png'), lang='eng'))
print(image_to_string(Image.open('a1.jpg'), lang='eng'))
print(image_to_string(Image.open('a2.jpg'), lang='eng'))
print(image_to_string(Image.open('a3.jpg'), lang='eng'))