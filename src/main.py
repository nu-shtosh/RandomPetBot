# RandomPetBot/src/main.py
import logging
import os
import random

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

secret_token = os.getenv('TG_TOKEN')
secret_token_giphy = os.getenv('GIPHY_TOKEN')
updater = Updater(token=secret_token, use_context=True)

rating = 'pg-13'
cat_tag = 'cat'
dog_tag = 'dog'
URL_cats = 'https://api.thecatapi.com/v1/images/search'
URL_dogs = 'https://api.thedogapi.com/v1/images/search'
URL_cats_gifs = (
    'https://api.giphy.com/v1/gifs/random?'
    f'api_key={secret_token_giphy}&tag={cat_tag}&rating={rating}'
)
URL_dogs_gifs = (
    'https://api.giphy.com/v1/gifs/random?'
    f'api_key={secret_token_giphy}&tag={dog_tag}&rating={rating}'
)


def get_random_cat_gif():
    response = requests.get(URL_cats_gifs)
    response = response.json()
    random_gif = response['data']['images']['downsized']['url']
    print(random_gif)
    return random_gif


def new_cat_gif(update, context):
    context.bot.send_animation(
        chat_id=update.effective_chat.id,
        animation=get_random_cat_gif()
    )


def get_random_dog_gif():
    response = requests.get(URL_dogs_gifs)
    response = response.json()
    random_gif = response['data']['images']['downsized']['url']
    print(random_gif)
    return random_gif


def new_dog_gif(update, context):
    context.bot.send_animation(
        chat_id=update.effective_chat.id,
        animation=get_random_dog_gif()
    )


def get_random_cat_image():
    try:
        response = requests.get(URL_cats)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(URL_dogs)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat_image(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_random_cat_image())


def get_random_dog_image():
    try:
        response = requests.get(URL_dogs)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(URL_cats)
    response = response.json()
    random_dog = response[0].get('url')
    return random_dog


def new_dog_image(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_random_dog_image())


def wake_up(update, context):
    chat_id = update.effective_chat.id
    name = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([
        ['/new_cat_image'],
        ['/new_dog_image'],
        ['/new_cat_gif'],
        ['/new_dog_gif']
        ],
        resize_keyboard=True
    )
    pets = ['cat_image', 'dog_image', 'cat_gif', 'dog_gif']
    if random.choice(pets) == 'cat_image':
        context.bot.send_message(
            chat_id=chat_id,
            text='Привет, {}. Cмотри, какого котика я тебе нашёл'.format(name),
            reply_markup=buttons
        )
        context.bot.send_photo(
            chat_id=chat_id,
            photo=get_random_cat_image()
        )
    elif random.choice(pets) == 'dog_image':
        context.bot.send_message(
            chat_id=chat_id,
            text='Привет, {}. Cмотри, какого песика я тебе нашёл'.format(name),
            reply_markup=buttons
        )
        context.bot.send_photo(
            chat_id=chat_id,
            photo=get_random_dog_image()
        )
    elif random.choice(pets) == 'cat_gif':
        context.bot.send_message(
            chat_id=chat_id,
            text='Привет, {}. Cмотри, какого котика я тебе нашёл'.format(name),
            reply_markup=buttons
        )
        context.bot.send_animation(
            chat_id=chat_id,
            animation=get_random_cat_gif()
        )
    elif random.choice(pets) == 'dog_gif':
        context.bot.send_message(
            chat_id=chat_id,
            text='Привет, {}. Cмотри, какого песика я тебе нашёл'.format(name),
            reply_markup=buttons
        )
        context.bot.send_animation(
            chat_id=chat_id,
            animation=get_random_dog_gif()
        )


def main():
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(
        CommandHandler('new_cat_image', new_cat_image)
    )
    updater.dispatcher.add_handler(
        CommandHandler('new_dog_image', new_dog_image)
    )
    updater.dispatcher.add_handler(CommandHandler('new_cat_gif', new_cat_gif))
    updater.dispatcher.add_handler(CommandHandler('new_dog_gif', new_dog_gif))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
