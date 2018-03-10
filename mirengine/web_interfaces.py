import datetime
import json
from datetime import datetime
from urllib.request import urlopen

import requests


def get_news():
    """

    :return: news list
    """
    sources = "the-times-of-india"
    url1 = 'https://newsapi.org/v2/top-headlines?sources=' + sources + '&apiKey=6093aae6a87b4111a426e78547ca0dbb'
    response = requests.get(url1).json()
    status = response['status']
    total_results = response['totalResults']

    news_list = []
    if status == "ok":
        for index in range(0, total_results):
            news_line = response['articles'][index]['description']
            news_list.append(news_line)
    return news_list


def get_quote():
    url = 'http://quotes.rest/qod.json?category=management'

    response = urlopen(url)
    data = json.load(response)

    print(data)

    quote_text = data["contents"]["quotes"][0]['quote']
    return quote_text


def get_weather(latitude=19.0328, longitude=72.8964):
    """

    :param latitude: default 19.0328 (chembur)
    :param longitude: default 72.8964 (chembur)
    :return: weather detail dic : city, main, temp, temp_symbol,today,humidity
    """
    latitude_string = str(latitude)
    longitude_string = str(longitude)
    url = 'http://api.openweathermap.org/data/2.5/weather?appid=920b82e6f20b59d0f1b7390abfdf5a1e&lat=' \
          + latitude_string + '&lon=' + longitude_string + '&units=metric'
    data = requests.get(url).json()
    main = data['weather'][0]['main']
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    city = data['name']
    symbol = u'\u00b0'
    temp_symbol = str(symbol)
    today = str(datetime.now().strftime('%Y-%m-%d'))

    print("Whether Details \n {} \n {} \n temp: {}{}C \n Date:{} \n Humidity: {}0".format(city, main, temp, temp_symbol,
                                                                                          today,
                                                                                          humidity))
    weather = {'temp': temp,
               'temp_symbol': temp_symbol,
               'city': city,
               'main': main,
               'today': today,
               'humidity': humidity}
    return weather
