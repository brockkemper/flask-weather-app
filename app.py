from flask import Flask
from flask import render_template
from flask import request
import requests
            

app = Flask(__name__)

cities = []


def get_user_city():
    r = requests.get('http://ip-api.com/json/').json()
    user_city = r['city']

    return user_city

def get_coordinantes(city):
    api_key = 'f98dc3431a342670822af40d0261487f'
    limit = 1

    location_response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={api_key}')
    city_info = location_response.json()

    if 'name' in city_info[0].keys():
        location = {'lat': city_info[0]['lat'], 'lon': city_info[0]['lon']}
    else:
        location = 'Invalid'

    return location

def get_weather(city):
    api_key = 'f98dc3431a342670822af40d0261487f'
    location = get_coordinantes(city)

    lat = location['lat']
    lon = location['lon']

    weather_info = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')

    temp_kelvin = weather_info.json()['main']['temp']
    temp_celcius = temp_kelvin - 273.15
    temp = round((temp_celcius * (9 / 5)) + 32)

    condition = weather_info.json()['weather'][0]['main']

    weather = {'city': city, 'temp': temp, 'condition': condition}

    return weather

user_city = get_user_city()
default_cities = [user_city, 'New York City', 'London']
default_weather = [get_weather(city) for city in default_cities]

cities.append(default_weather[0])
cities.append(default_weather[1])
cities.append(default_weather[2])

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_city = request.form['add-city']
        if get_coordinantes(new_city) == 'Invalid':
           return render_template('index.html', cities=cities)
          
        new_city_weather = get_weather(request.form['add-city'])
        cities.append(new_city_weather) 

    return render_template('index.html', cities=cities)


if __name__ == '__main__':
    app.run(debug='ON')
