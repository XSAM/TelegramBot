import json

def init():
    global data
    with open('data.json', 'r') as file:
        data = json.load(file)

def update_weather(day, description):
    global data
    data['day'] = day
    data['description'] = description
    write_settings_file()

def update_location(lng, lat):
    global data
    data['lng'] = lng
    data['lat'] = lat
    write_settings_file()

def write_settings_file():
    global data
    with open('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii = False)
