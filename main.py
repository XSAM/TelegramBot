from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.bot import Bot
import logging
from multiprocessing import Process
import os

import weather
import settings
import polling


def start(bot, update):
    # for personality
    if update.message.chat_id != user_id:
        return
    bot.send_message(chat_id=update.message.chat_id, text="Hello, my friend!")

# just test
def caps(bot, update, args):
    # for personality
    if update.message.chat_id != user_id:
        return
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

def status(bot, update):
    # for personality
    if update.message.chat_id != user_id:
        return
    bot.send_message(chat_id=update.message.chat_id, text=weather.get_weather())

def location(bot, update):
    # for personality
    if update.message.chat_id != user_id:
        return
    bot.send_message(chat_id=update.message.chat_id,
                    text = "Current Location:\n {},{}".format(settings.data['lng'], settings.data['lat']))

def set_location(bot, update):
    # for personality
    if update.message.chat_id != user_id:
        return
    print(update.message.location)
    location = update.message.location
    settings.update_location(location.longitude, location.latitude)
    bot.send_message(chat_id=update.message.chat_id,
                    text="Location Confirmed:\n {},{}".format(location.longitude, location.latitude))
    bot.send_message(chat_id=update.message.chat_id, text=weather.get_weather())

def main():
    print("token_key: {}".format(os.getenv('TELEGRAM_BOT_TOKEN_KEY')))
    global token_key

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
                        level=logging.INFO)

    # init data
    settings.init()
    # ready for polling
    polling.init()

    start_handler = CommandHandler('start', start);
    caps_handler = CommandHandler('caps', caps, pass_args=True)
    status_handler = CommandHandler('status', status);
    location_handler = CommandHandler('location', location);
    set_location_handler = MessageHandler(Filters.location, set_location)

    #updater = Updater(bot = polling.bot)
    updater = Updater(token = token_key)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(status_handler)
    dispatcher.add_handler(location_handler)
    dispatcher.add_handler(set_location_handler)

    updater.start_polling()
    polling.start()

# polling module need this
token_key = os.getenv('TELEGRAM_BOT_TOKEN_KEY')
user_id = 389135227
if token_key is None:
    print('Need Configure Environment Variable: TELEGRAM_BOT_TOKEN_KEY')
    exit()

if __name__ == '__main__':
    main()
