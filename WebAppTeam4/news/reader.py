from bs4 import BeautifulSoup
import requests

import json

import datetime
from cities import city_dict


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
        self.articles = self.soup.findAll('item')[:10] # parsing only last 10 news
        self.articles_dicts = [
            {'title': a.find('title').text, 'link': a.find('link').text,
             'description': a.find('description').text, 'pubdate': a.find('pubDate').text} for a in self.articles]


class ReadCurrency:
    def __init__(self, headers):

        self.url_nbu = 'https://kurs.com.ua/nbu'
        self.url_pb = 'https://kurs.com.ua/bank/10-privatbank'
        self.headers = headers

        # fetch NBU courses
        try:
            self.r = requests.get(self.url_nbu, headers=self.headers)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', self.url_nbu)
            print(e)
        try:
            self.soup_nbu = BeautifulSoup(self.r.text, "html.parser")
        except Exception as e:
            print('Could not parse the html: ', self.url_nbu)
            print(e)

        # fetch privatbank courses
        try:
            self.r = requests.get(self.url_pb, headers=self.headers)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', self.url_pb)
            print(e)
        try:
            self.soup_pb = BeautifulSoup(self.r.text, "html.parser")
        except Exception as e:
            print('Could not parse the html: ', self.url_pb)
            print(e)


        self.table = self.soup_nbu.find('table', class_='table-course')
        print(self.table)
        count = 0
        self.currencies_dicts = []
        self.rows = self.table.find_all('tr')
        for row in self.rows:
            cols = row.find_all('td')
            if len(cols) >= 2 and count < 6:
                code = cols[0].text.strip()
                cur = {"currency": cols[1].text.strip(),
                       "nbu_rate": round(float(cols[3].text.split("\n")[1].strip()), 2)}
                if code != "RUB":
                    self.currencies_dicts.append({code: cur})
                count += 1

        # self.currencies_dicts = []
        self.table_pb = self.soup_pb.find('table', class_='table-course', recursive=True)
        print(self.table_pb)
        count = 0

        self.rows = self.table_pb.find_all('tr', recursive=True)
        print(self.rows)
        for row in self.rows:
            cols = row.find_all('td')
            if len(cols) >= 2 and count < 6:
                code = cols[0].text.strip()
                cur = {"purchase": round(float(cols[2].text.strip()), 2),
                       "sale": round(float(cols[3].text.split("\n")[1].strip()), 2)}
                self.currencies_dicts.append({code: cur})
                count += 1


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


if __name__ == '__main__':
    # feed_biz = ReadRss('https://kurs.com.ua/novosti/rss/feed-1.xml', headers)
    # print(feed_biz.articles_dicts)
    #
    feed_weather = ReadWeather('3478743f8ff6ad5d9cae9ea84b3cb414', "Kиїв")
    print(feed_weather.weather_info)
    #
    # feed_polit = ReadRss('https://kurs.com.ua/novosti/rss/feed-7.xml', headers)
    # print(feed_polit.articles_dicts)
    #
    # feed_world = ReadRss('https://kurs.com.ua/novosti/rss/feed-12.xml', headers)
    # print(feed_world.articles_dicts)
    #
    # feed_sport = ReadRss('https://kurs.com.ua/novosti/rss/feed-17.xml', headers)
    # print(feed_sport.articles_dicts)
    #
    # feed_tech = ReadRss('https://kurs.com.ua/novosti/rss/feed-8.xml', headers)
    # print(feed_tech.articles_dicts)
    #
    # feed_lifestyle = ReadRss('https://kurs.com.ua/novosti/rss/feed-5.xml', headers)
    # print(feed_lifestyle.articles_dicts)

    feed_cur_nbu = ReadCurrency(headers)
    print(feed_cur_nbu.currencies_dicts)

    # feed_cur_pb = ReadCurrency('https://kurs.com.ua/bank/10-privatbank', headers)
    # print(feed_cur_pb.currencies_dicts)
