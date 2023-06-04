import argparse
import os

import pendulum
import requests
import openai
from BingImageCreator import ImageGen

SENTENCE_API = "https://v1.jinrishici.com/all"
DEFAULT_SENTENCE = "赏花归去马如飞\r\n去马如飞酒力微\r\n酒力微醒时已暮\r\n醒时已暮赏花归\r\n"
PROMPT = "请帮我把这个句子 `{sentence}` 翻译成英语，请翻译的有诗意一点儿。"

def generate_image(prompt, bing_cookie):
    """
    return the link for md
    """
    i = ImageGen(bing_cookie)
    images = i.get_images(prompt)
    date_str = pendulum.now().to_date_string()
    new_path = os.path.join("images", date_str)
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    i.save_images(images, new_path)
    return random.choice(images)


def get_sentence():
    try:
        r = requests.get(SENTENCE_API)
        if r.ok:
            return r.json().get("content", DEFAULT_SENTENCE)
        return DEFAULT_SENTENCE
    except:
        print("get SENTENCE_API wrong")
        return DEFAULT_SENTENCE


def build_image_prompt(sentence):
    ms = [{"role": "user", "content": PROMPT.format(sentence=sentence)}]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=ms,
    )
    sentence_en = (
        completion["choices"][0].get("message").get("content").encode("utf8").decode()
    )
    sentence_en = sentence_en + "Chinese art style 4k"
    return sentence_en


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bing-cookie')
    args = parser.parse_args()

    sentence = get_sentence()
    image_prompt = build_image_prompt(sentence)
    generate_image(image_prompt, args.bing_cookie)


if __name__ == '__main__':
    main()

