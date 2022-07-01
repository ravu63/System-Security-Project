from captcha.image import ImageCaptcha
import string
import random


def generate_captcha_image(captcha_text):
    image = ImageCaptcha(width=280, height=90)
    data = image.generate(captcha_text)
    captcha_image = image.write(captcha_text,'static/cap.jpeg')





