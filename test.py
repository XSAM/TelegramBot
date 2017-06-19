from settings import init
from weather import analyse_weather

def setup():
    init()
    print('setup')

def run():
    print(analyse_weather())

setup()
