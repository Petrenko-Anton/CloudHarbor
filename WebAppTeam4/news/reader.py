from bs4 import BeautifulSoup
import requests
import os

from datetime import date, datetime
from cities import cities
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")


settings.configure()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}


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
        self.articles = self.soup.findAll('item')
        self.articles_dicts = [
            {'title': a.find('title').text, 'link': a.find('link').text,
             'description': a.find('description').text, 'pubdate': a.find('pubDate').text} for a in self.articles]
        self.first_10_articles =[]
        count = 0
        for article in self.articles_dicts:
            self.first_10_articles.append(article)
            count += 1
            if count >= 10:
                break

class ReadCurrency:
    def __init__(self, cur_url, headers):

        self.url = cur_url
        self.headers = headers
        try:
            self.r = requests.get(cur_url, headers=self.headers)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', cur_url)
            print(e)
        try:
            self.soup = BeautifulSoup(self.r.text, "html.parser")
        except Exception as e:
            print('Could not parse the html: ', self.url)
            print(e)

        self.tables = self.soup.find_all('table', class_='table-course')
        count = 0
        self.currencies_dicts = []
        for table in self.tables:
            self.rows = table.find_all('tr')
            for row in self.rows:
                cols = row.find_all('td')
                if len(cols) >= 2 and count < 6:
                    cur = {"code": cols[0].text.strip(), "currency": cols[1].text.strip(),
                           "exchange_rate": cols[3].text.split("\n")[1].strip()}
                    self.currencies_dicts.append(cur)
                    count += 1


class ReadWeather():
    def __init__(self, api_key, city_list):
        self.weather_list = []
        for city, coords in city_list.items():
            lat = coords["lat"]
            lon = coords["lon"]
            try:
                self.r = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&lang=uk&units=metric&exclude=minutely,hourly,alerts&appid={api_key}')
                self.status_code = self.r.status_code
            except Exception as e:
                print('Error fetching weather!')
                print(e)
            self.weather_list.append({city: self.r.text})


if __name__ == '__main__':
    feed_biz = ReadRss('https://kurs.com.ua/novosti/rss/feed-1.xml', headers)
    print(feed_biz.first_10_articles)
    print(len(feed_biz.first_10_articles))
    date_format = "%a, %d %b %Y %H:%M:%S +0300"

    feed_weather = ReadWeather('3478743f8ff6ad5d9cae9ea84b3cb414', cities)
    print(feed_weather.weather_list)
    #
    # feed_polit = ReadRss('https://kurs.com.ua/novosti/rss/feed-7.xml', headers)
    # print(feed_polit.urls)
    # print(len(feed_polit.urls))
    # date_format = "%a, %d %b %Y %H:%M:%S +0300"
    #
    # feed_world = ReadRss('https://kurs.com.ua/novosti/rss/feed-12.xml', headers)
    # print(feed_world.urls)
    # print(len(feed_world.urls))
    # date_format = "%a, %d %b %Y %H:%M:%S +0300"
    #
    # feed_sport = ReadRss('https://kurs.com.ua/novosti/rss/feed-17.xml', headers)
    # print(feed_sport.urls)
    # print(len(feed_sport.urls))
    # date_format = "%a, %d %b %Y %H:%M:%S +0300"
    #
    # feed_tech = ReadRss('https://kurs.com.ua/novosti/rss/feed-8.xml', headers)
    # print(feed_tech.urls)
    # print(len(feed_tech.urls))
    # date_format = "%a, %d %b %Y %H:%M:%S +0300"
    #
    # feed_lifestyle = ReadRss('https://kurs.com.ua/novosti/rss/feed-5.xml', headers)
    # print(feed_lifestyle.urls)
    # print(len(feed_lifestyle.urls))
    # date_format = "%a, %d %b %Y %H:%M:%S +0300"

    feed_cur = ReadCurrency('https://kurs.com.ua/nbu', headers)
    print(feed_cur.currencies_dicts)
