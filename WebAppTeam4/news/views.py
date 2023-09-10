import datetime
import json
import redis
from redis_lru import RedisLRU
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from .cities import city_dict

headers = {
    'User-Agent': settings.USER_AGENT
}

city_list = list(city_dict.keys())

client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
cache = RedisLRU(client)
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)

news_id =1
class ReadRss:
    def __init__(self, rss_url, category, headers):

        def find_pic(url):
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")
            main_image = soup.find("meta", property="og:image")
            image_url = main_image["content"]
            return image_url if main_image else None

        self.url = rss_url
        self.headers = headers
        self.category = category
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
        self.articles = self.soup.findAll('item')[:10]  # parsing only last 10 news
        self.articles_dicts = [
            {'category': self.category, 'title': a.find('title').text, 'link': a.find('link').text,
             'description': a.find('description').text.replace(r'\"', '"').strip('"'),
             'pubdate': a.find('pubDate').text, 'img': find_pic(a.find('link').text)} for a in self.articles]


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


@cache(ttl=60 * 60 * 24)
def currency():
    today = datetime.datetime.now().date().strftime('%d.%m.%Y')
    r = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={today}')
    json_ = r.text
    data = json.loads(json_)
    desired_currencies = ['USD', 'EUR', 'GBP', 'CHF', 'PLN']
    currency_courses = []
    for exchange_rate in data["exchangeRate"]:
        currency_code = exchange_rate["currency"]

        if currency_code in desired_currencies:
            purchase_rate = exchange_rate.get("purchaseRate")
            sale_rate = exchange_rate.get("saleRate")
            nbu_rate = round(((exchange_rate.get("purchaseRateNB") + exchange_rate.get("saleRateNB")) / 2), 2)

            currency_courses.append({
                currency_code: {
                    "purchase": purchase_rate,
                    "sale": sale_rate,
                    "nbu": nbu_rate
                }
            })
    return (sorted(currency_courses, key=lambda x: desired_currencies.index(list(x.keys())[0])))


@cache(ttl=60 * 60 * 2)
def weather(city):
    weather_feed = ReadWeather(settings.WEATHER_API_KEY, city)
    return weather_feed.weather_info



def news():
    news_feed = []
    cat_dict = {'business': 1, 'politic': 7, 'world': 12, 'sport': 17, 'lifestyle': 5, "tech": 8}
    for cat in cat_dict.keys():
        print(cat)
        url = f'https://kurs.com.ua/novosti/rss/feed-{cat_dict[cat]}.xml'
        news_feed.extend(ReadRss(url, cat, headers).articles_dicts)
        print(news_feed)
    return news_feed


def get_news():
    news_ = r.get(str(news_id))
    if news_ is None:
        news_ = news()
        r.set(news_id, json.dumps(news_))
        r.expire(str(news_id), 60 * 60 * 2)
        return news_
    return json.loads(news_)


def index(request, city="Kиїв"):
    news_f = get_news()
    weather_info = weather(city)
    return render(request, 'news/news.html',{'news': news_f, 'city_list': city_list, 'city': city,
                                             'weather_info': weather_info, 'currency_list': currency()})
