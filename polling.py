import threading
import datetime
import time
from telegram.bot import Bot

from main import token_key
import weather


def init():
    global bot
    bot = Bot(token = token_key)

def loop_thread():
    while 'True':
        now = str(datetime.datetime.now())
        print('{}: loop_thread awake'.format(now))
        result = weather.analyse_weather()
        if result is not None:
            bot.send_message(chat_id = 389135227, text = result)
        time.sleep(14400)

def start():
    thread = threading.Thread(target = loop_thread)
    thread.start()
