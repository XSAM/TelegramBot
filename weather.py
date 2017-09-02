import re
import requests
import datetime
import decimal
from urllib.parse import urlencode, quote_plus

import settings

# get weather data from yahoo
def get_weather_description_with_yahoo(lng, lat):
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = 'select * from weather.forecast where woeid in (select woeid from geo.places where text="({},{})")'.format(lat, lng)
    yql_url = baseurl + urlencode({'q':yql_query}) + "&format=json"
    print(yql_query)
    api_data = requests.get(url=yql_url)
    #print(api_data.text)
    result_json = api_data.json()
    print("fetch weather info successed")
    #print(result_json)

    while(result_json['query']['results'] is None):
        time.sleep(5)
        print("Refetch data")
        api_data = requests.get(url=yql_url)
        result_json = api_data.json()
        print(result_json)

    description = result_json['query']['results']['channel']['item']['forecast'][0]['text']
    return description

# get weather data from dark sky
def get_weather_description_with_darksky(lng, lat):
    baseurl = "https://api.darksky.net/forecast/0974760b3c252cd3940907222d7dd041/{},{}".format(lat, lng)
    print(baseurl)
    api_data = requests.get(url=baseurl)
    result_json = api_data.json()
    print("fetch weather info successed")
    #print(result_json)

    while(result_json['currently'] is None):
        time.sleep(5)
        print("Refetch data")
        api_data = requests.get(url=baseurl)
        result_json = api_data.json()
        print(result_json)

    description = result_json['hourly']['data'][0]['summary']
    return description

def get_weather_with_location(lng, lat):
    now = str(datetime.datetime.now())
    print(f'{}: get_weather'.format(now))

    description = get_weather_description_with_darksky(lng, lat)
    print(f'get_weather_with_location() - description: {}'.format(description))
    return description

def get_weather():
    return get_weather_with_location(settings.data['lng'], settings.data['lat'])

def analyse_weather():
    #need_send_message = false
    keywords = ('Thunder','Rain','Showers')

    # GTM+8 timezone
    time = datetime.datetime.utcnow() + datetime.timedelta(hours=+8)
    day = time.day
    description = get_weather()
    if any(keyword in description for keyword in keywords):
        if description != settings.data['description']\
                or day != settings.data['day']:
            #need_send_message = true
            settings.update_weather(day, description)
            return description
        else:
            return None
    else:
        return None
