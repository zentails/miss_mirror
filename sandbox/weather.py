import datetime
from datetime import datetime

import requests

def get_details():
    # r = requests.get('https://api.ipdata.co').json()
    laty=str(19.0328)#str(r['latitude'])
    longy=str(72.8964)#str(r['longitude'])
    # print(laty)
    # print(longy)
    url='http://api.openweathermap.org/data/2.5/weather?appid=920b82e6f20b59d0f1b7390abfdf5a1e&lat='+laty+'&lon='+longy+'&units=metric'
    data=requests.get(url).json()
    main=data['weather'][0]['main']
    temp=data['main']['temp']
    humidity=data['main']['humidity']
    city=data['name']
    symbol=u'\u00b0'
    t=str(symbol)
    today = str(datetime.now().strftime('%Y-%m-%d'))

    tex="Whether Details \n {} \n {} \n temp: {}{}C \n Date:{} \n Humidity: {}0".format(city,main ,temp,t,today,humidity)
    return tex

# print(get_details())