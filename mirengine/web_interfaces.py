import datetime
import json
from datetime import datetime
from urllib.request import urlopen

import requests


class WebGet():
    def get_data_list(self):
        return ["What! how?", "This aint suppose to happen"]

    def __str__(self):
        data_list = self.get_data_list()
        data_string = ""
        for x in data_list:
            data_string += str(x) + "\n"
        return data_string


class WebNews(WebGet):

    def get_data_list(self):
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


class WebQuote(WebGet):
    def get_data_list(self):
        url = 'http://quotes.rest/qod.json?category=management'

        response = urlopen(url)
        data = json.load(response)

        # print(data)

        quote_text = data["contents"]["quotes"][0]['quote']

        # print(quote_text+"\n------------------------------------------------------------\n")

        return [quote_text,]


class WebWeather(WebGet):
    def __init__(self, latitude=19.0328, longitude=72.8964):
        self.latitude = latitude
        self.longitude = longitude

    def get_data_list(self):
        """

            :param latitude: default 19.0328 (chembur)
            :param longitude: default 72.8964 (chembur)
            :return: weather detail dic : city, main, temp, temp_symbol,today,humidity
            """
        latitude_string = str(self.latitude)
        longitude_string = str(self.longitude)
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

        print("Whether Details \n {} \n {} \n temp: {}{}C \n Date:{} \n Humidity: {}0".format(city, main, temp,
                                                                                              temp_symbol,
                                                                                              today,
                                                                                              humidity))
        weather = ['temp:' + str(temp),
                   'temp_symbol:' + temp_symbol,
                   'city:' + str(city),
                   'main:' + str(main),
                   'today:' + str(today),
                   'humidity:' + str(humidity)]
        return weather

if __name__ == '__main__':
    # print(WebWeather())
    print(WebQuote())
    # print(WebNews())