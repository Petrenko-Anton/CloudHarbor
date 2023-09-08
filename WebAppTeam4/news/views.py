import os
from bs4 import BeautifulSoup
import requests
from django.shortcuts import render
# from .cities import city_dict
import datetime
import json
from dotenv import load_dotenv
from pathlib import Path
from django.conf import settings

city_dict = {"Kиїв": {"lat": 50.4500336, "lon": 30.5241361}, "Харків": {"lat": 49.9923181, "lon": 36.2310146},
          "Дніпро": {"lat": 48.4680221, "lon": 35.0417711}, "Одеса": {"lat": 46.4843023, "lon": 30.7322878},
          "Донецьк": {"lat": 48.0158753, "lon": 37.8013407}, "Запоріжжя": {"lat": 47.8507859, "lon": 35.1182867},
          "Львів": {"lat": 49.841952, "lon": 24.0315921}, "Миколаїв": {"lat": 46.9758615, "lon":31.9939666},
          "Луганськ": {"lat": 48.5717084, "lon": 39.2973153}, "Вінниця": {"lat": 49.2320162, "lon": 28.467975},
          "Сімферополь": {"lat": 44.9521459, "lon": 34.1024858}, "Херсон": {"lat": 46.6412644,"lon": 32.625794},
          "Полтава": {"lat": 49.5897423, "lon": 34.5507948}, "Чернігів": {"lat": 51.494099,"lon": 31.294332},
          "Черкаси": {"lat": 49.4447888, "lon": 32.0587805}, "Суми": {"lat": 50.9119775,"lon": 34.8027723},
          "Житомир": {"lat": 50.2598298, "lon": 28.6692345}, "Хмельницький": {"lat": 49.4196404,"lon": 26.9793793},
          "Кропивницький": {"lat": 48.5105805, "lon": 32.2656283}, "Рівне": {"lat": 50.6196175,"lon": 26.2513165},
          "Чернівці": {"lat": 48.2864702,"lon": 25.9376532}, "Тернопіль": {"lat": 49.5557716,"lon": 25.591886},
          "Івано-Франківськ": {"lat": 48.9225224,"lon": 24.7103188}, "Луцьк": {"lat": 50.7450733, "lon": 25.320078},
          "Ужгрод": {"lat": 48.6223732, "lon": 22.3022569}}


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

city_list = list(city_dict.keys())

class ReadRss:

    def __init__(self, rss_url, headers):

        self.url = rss_url
        self.headers = headers
        try:
            self.r = requests.get(rss_url, headers=self.headers)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', rss_url)
            print(e)
        try:
            self.soup = BeautifulSoup(self.r.text, features="xml")
        except Exception as e:
            print('Could not parse the xml: ', self.url)
            print(e)
        self.articles = self.soup.findAll('item')[:10] # parsing only last 10 news
        self.articles_dicts = [
            {'title': a.find('title').text, 'link': a.find('link').text,
             'description': a.find('description').text, 'pubdate': a.find('pubDate').text} for a in self.articles]


class ReadWeather():
    def __init__(self, api_key, city):

        def temp_conv(temperature: str) -> str:
            deg = int(round(float(temperature), 0))
            return str(deg) + "°" if deg >= 0 else "-" + str(deg) + "°"

        def date_conv(timestamp: str) -> str:
            today = datetime.date.today()
            datetime1 = datetime.datetime.utcfromtimestamp(timestamp)
            date1 = datetime.date(year=datetime1.year, month=datetime1.month, day=datetime1.day)
            return date1.strftime('%Y-%m-%d')

        def wind_dir(degrees: int) -> str:
            cardinal_directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
            arrow_symbols = ['↑', '↗', '→', '↘', '↓', '↙', '←', '↖', '↑']
            index = int((degrees + 22.5) / 45)
            return arrow_symbols[index]

        lat = city_dict[city]["lat"]
        lon = city_dict[city]["lon"]
        try:
            self.r = requests.get(
                f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&lang=uk&units=metric&exclude=minutely,hourly,alerts&appid={api_key}')
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching weather!')
            print(e)

        data = json.loads(self.r.text)

        self.weather_info = {city: {"current": {"temperature": temp_conv(data["current"]["temp"]),
                                                "humidity": str(data["current"]["humidity"]) + "%",
                                                "pressure": str(data["current"]["pressure"]) + " мм.рт.ст.",
                                                "wind_speed": str(data["current"]["wind_speed"]) + " м/с " +
                                                              wind_dir(data["current"]["wind_deg"]),
                                                "cloudness": str(data["current"]["clouds"]) + "%",
                                                "description": str(data["current"]["weather"][0]["description"])},

                                    "daily": []
                                    }}
        for day_data in data["daily"][0:]:
            daily_info = {
                "date": date_conv(day_data["dt"]),
                "temperature_day": temp_conv(day_data["temp"]["day"]),
                "temperature_night": temp_conv(day_data["temp"]["night"]),
                "humidity": str(day_data["humidity"]) + "%",
                "pressure": str(day_data["pressure"]) + " мм.рт.ст.",
                "wind_speed": str(day_data["wind_speed"]) + " м/с " + wind_dir(day_data["wind_deg"]),
                "cloudiness": str(day_data["clouds"]) + "%",
                "description": day_data["weather"][0]["description"]
            }
            self.weather_info[city]["daily"].append(daily_info)


def index(request, category="#world", city="Kиїв"):
    cat_dict = {'#business': 1, '#politic': 7, '#world': 12, '#sport': 17, '#lifestyle': 5, "#tech": 8}
    url = f'https://kurs.com.ua/novosti/rss/feed-{cat_dict[category]}.xml'
    news = ReadRss(url, headers).articles_dicts
    weather_info = ReadWeather('3478743f8ff6ad5d9cae9ea84b3cb414', city).weather_info
    return render(request, 'news/news.html', {'news': news, 'city_list': city_list, 'city': city, 'weather_info': weather_info})

def currency(request):
    currency_courses = [{'USD': {'purchase': 37.38, 'sale': 38.10, 'nbu': 36.56}}, {'EUR': {'purchase': 40.67, 'sale': 41.61, 'nbu': 39.73}}, {'PLN': {'purchase': 8.81, 'sale': 9.35, 'nbu': 8.89}}]
    return render(request, 'news/news.html', {'currency_list': currency_courses})

def weather(request):
    city = request.args.get('city')
    weather_feed = ReadWeather('3478743f8ff6ad5d9cae9ea84b3cb414', city)
    render(request, 'news/news.html', {'weather_info': weather_feed.weather_info})