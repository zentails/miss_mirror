from urllib.request import urlopen
import json

'''
extra sites to get quotes
url='http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1'
url1='http://quotes.rest/qod.json?category=management'
data=requests.get(url ).json()
print(data[0]['content'])
print(data['contents']['quotes'][0]['quote'])

    response = requests.post("https://andruxnet-random-famous-quotes.p.mashape.com/?cat=famous&count=10",
      headers={
        "X-Mashape-Key": "njkiSXE1gYmshR0nlfUMUX3JLkVPp19AFSHjsnOp4fgO5qbv7o",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
      }
    ).json()
    quote=response['quote']
'''


def get_quote():
    url = 'http://quotes.rest/qod.json?category=management'

    response = urlopen(url)
    data = json.load(response)

    print(data)

    quote_text = data["contents"]["quotes"][0]['quote']
    return quote_text
