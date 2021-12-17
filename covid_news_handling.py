import requests
import sched

import covid_logger
import time
import json

all_news = {}
configData = json.load(open('config.json'))


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    response = requests.get(configData["news_api_url"] + covid_terms + configData["api_key"])
    return response.json()


def update_news():
    dic = news_API_request()
    covid_logger.log("news_data : "+str(len(str(dic)))+" byte")
    for article in dic["articles"]:
        if article["title"] not in all_news:
            all_news[article["title"]] = article


def schedule_news(update_interval, update_name=None):
    s = sched.scheduler(time.time, time.sleep)

    def update(sc):
        update_news()
        covid_logger.log("all_news  : "+str(len(all_news))+" titles")
        s.enter(update_interval, 1, update, (sc,))

    s.enter(0, 1, update, (s,))
    s.run()
