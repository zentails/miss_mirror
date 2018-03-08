import requests


def get_news():
    sources = "the-times-of-india"
    url1 = 'https://newsapi.org/v2/top-headlines?sources=' + sources + '&apiKey=6093aae6a87b4111a426e78547ca0dbb'
    response = requests.get(url1).json()
    status = response['status']
    total_results = response['totalResults']

    newss = ""
    if status == "ok":
        for index in range(0, total_results):
            news = response['articles'][index]['description']
            newss += "\n\n>>{}".format(news)
    return newss
