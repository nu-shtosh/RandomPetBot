# RandomPetBot/src/main.py
import os
from dotenv import load_dotenv
import giphy_client
import logging
import requests
import random
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

secret_token = os.getenv('TG_TOKEN')
updater = Updater(token=secret_token, use_context=True)
URL_cats = 'https://api.thecatapi.com/v1/images/search'
URL_dogs = 'https://api.thedogapi.com/v1/images/search'
# secret_token_giphy = os.getenv('GIPHY_TOKEN')


# def get_random_cat_gif(api_key):
#     instanse = giphy_client.DefaultApi()
#     response = instanse.gifs_random_get(api_key, tag='cat')
#     print(response)
#     random_gif = response.data.url
#     return random_gif


# def new_cat_gif(update, context):
#     context.bot.send_animation(
#         chat_id=update.effective_chat.id,
#         animation=get_random_cat_gif(secret_token_giphy)
#     )


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
    # , 'gifs' , ['/new_cat_gif']
    buttons = ReplyKeyboardMarkup([['/new_cat_image'], ['/new_dog_image']], resize_keyboard=True)
    
    pets = ['cats', 'dogs']
    if random.choice(pets) == 'cats':
        context.bot.send_message(
            chat_id=chat_id,
            text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
            reply_markup=buttons
        )
        context.bot.send_photo(chat_id=chat_id, photo=get_random_cat_image())
    elif random.choice(pets) == 'dogs':
        context.bot.send_message(
            chat_id=chat_id,
            text='Привет, {}. Посмотри, какого песика я тебе нашёл'.format(name),
            reply_markup=buttons
        )
        context.bot.send_photo(chat_id=chat_id, photo=get_random_dog_image())
    # else:
    #     context.bot.send_message(
    #         chat_id=chat_id,
    #         text='Привет, {}. Посмотри, какую гифку я тебе нашёл'.format(name),
    #         reply_markup=buttons
    #     )
    #     context.bot.send_animation(chat_id=chat_id, animation=get_random_cat_gif(secret_token_giphy))


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('new_cat_image', new_cat_image))
updater.dispatcher.add_handler(CommandHandler('new_dog_image', new_dog_image))
# updater.dispatcher.add_handler(CommandHandler('new_cat_gif', new_cat_gif))
updater.start_polling()
updater.idle()
