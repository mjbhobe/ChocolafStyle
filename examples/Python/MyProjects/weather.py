# -*- coding: utf-8 -*-
"""
* weather.py - get weather information
* TKinter app converted to PyQt5
* TKinter app @https://www.askpython.com/python/examples/gui-weather-app-in-python
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys
import os
import pathlib
import requests
import urllib
from bs4 import BeautifulSoup
from datetime import datetime
from argparse import ArgumentParser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp

APP_PATH = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} Weather application"
HOME_DIR = str(pathlib.Path.home())

API_KEY = '609e577f6c5eeac1a9a6c42875bbc0ec'
CITY = 'Mumbai'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time

def getWeather(city='Mumbai'):
    request_url = WEATHER_URL.format(city, API_KEY)
    response = requests.get(request_url)
    weather_info = response.json()
    print(weather_info)
    weather_data = {}  # response dict

    weather_data['cod'] = weather_info['cod']

    if weather_info['cod'] == 200:
        kelvin = 273.0
        # @see: https://openweathermap.org/current for documentation
        weather_data['city'] = weather_info['name'] + ', ' + weather_info['sys']['country']
        weather_data['weather_main'] = str(weather_info['weather'][0]['description']).title() #['main']
        weather_data['weather_icon'] = weather_info['weather'][0]['icon']
        weather_data['temp'] = int(float(weather_info['main']['temp']) - kelvin)
        weather_data['feels_like_temp'] = int(float(weather_info['main']['feels_like']) - kelvin)
        weather_data['temp_min'] = int(float(weather_info['main']['temp_min']) - kelvin)
        weather_data['temp_max'] = int(float(weather_info['main']['temp_max']) - kelvin)
        weather_data['pressure'] = weather_info['main']['pressure']
        weather_data['humidity'] = weather_info['main']['humidity']
        weather_data['visibility'] = weather_info['visibility']
        weather_data['wind_speed'] = weather_info['wind']['speed'] # * 3.6
        weather_data['wind_direction'] = weather_info['wind']['deg']
        weather_data['timezone'] = weather_info['timezone']
        weather_data['cloudy'] = weather_info['clouds']['all']
        weather_data['description'] = weather_info['weather'][0]['description']
        weather_data['date'] = weather_info['dt']
        weather_data['sunrise_time'] = weather_info['sys']['sunrise']
        weather_data['sunset_time'] = weather_info['sys']['sunset']
    else:
        print(f"Weather info for city {city} not found!")
    return weather_data

def getCities():
    # @see: https://medium.com/geekculture/web-scraping-tables-in-python-using-beautiful-soup-8bbc31c5803e
    # for example of using beautifulsoup4 to load HTML table into pandas dataframe
    cities_url = "https://worldpopulationreview.com/world-cities"
    data = requests.get(cities_url).text
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table', class_='table')
    cities = []
    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')
        # cols are: Rank, Name, Country, 2022 Population, 2021 Population, Change
        cities.append(columns[1].text.strip())
    return sorted(cities)


class WeatherWidget(QWidget):
    def __init__(self, weather_data_dict, parent:QWidget=None):
        super(WeatherWidget, self).__init__(parent)
        self.setupUi()
        self.displayWeatherData(weather_data_dict)

    def loadWeatherIcon(self, weather_icon):
        pixmap_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
        data = urllib.request.urlopen(pixmap_url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        return pixmap

    def setupUi(self):
        self.iconLabel = QLabel("Weather Icon")
        self.iconLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.city = QLabel("<html><h2>City Name</h2></html>")
        self.city.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.weatherMain = QLabel("weather date & label")
        self.weatherMain.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        upperWidget = QWidget()
        gl1 = QGridLayout()
        gl1.addWidget(self.iconLabel, 0, 0, 2, 1)
        gl1.addWidget(self.city, 0, 1)
        gl1.addWidget(self.weatherMain, 1, 1)
        upperWidget.setLayout(gl1)

        self.tempLabel = QLabel("<html><b>Temperature:</b></html>")
        self.tempValueLabel = QLabel("temperature")
        self.feelsLikeTempLabel = QLabel("<html><b>Feels like:</b></html>")
        self.feelsLikeTempValueLabel = QLabel("feels like")
        self.minTempLabel = QLabel("<html><b>Min temp:</b></html>")
        self.minTempValueLabel = QLabel("min temp")
        self.maxTempLabel = QLabel("<html><b>Max temp:</b></html>")
        self.maxTempValueLabel = QLabel("max temp")
        self.pressureLabel = QLabel("<html><b>Pressure:</b></html>")
        self.pressureValueLabel = QLabel("pressure")
        self.humidityLabel = QLabel("<html><b>Humidity:</b></html>")
        self.humidityValueLabel = QLabel("humidity")
        self.sunriseTimeLabel = QLabel("<html><b>Sunrise:</b></html>")
        self.sunriseTimeValueLabel = QLabel("sunrise time")
        self.sunsetTimeLabel = QLabel("<html><b>Sunset:</b></html>")
        self.sunsetTimeValueLabel = QLabel("sunset time")

        lowerWidget = QWidget()
        gl2 = QGridLayout()
        gl2.addWidget(self.tempLabel, 0, 0)
        gl2.addWidget(self.tempValueLabel, 0, 1)
        gl2.addWidget(self.feelsLikeTempLabel, 0, 2)
        gl2.addWidget(self.feelsLikeTempValueLabel, 0, 3)
        gl2.addWidget(self.minTempLabel, 1, 0)
        gl2.addWidget(self.minTempValueLabel, 1, 1)
        gl2.addWidget(self.maxTempLabel, 1, 2)
        gl2.addWidget(self.maxTempValueLabel, 1, 3)
        gl2.addWidget(self.pressureLabel, 2, 0)
        gl2.addWidget(self.pressureValueLabel, 2, 1)
        gl2.addWidget(self.humidityLabel, 2, 2)
        gl2.addWidget(self.humidityValueLabel, 2, 3)
        gl2.addWidget(self.sunriseTimeLabel, 3, 0)
        gl2.addWidget(self.sunriseTimeValueLabel, 3, 1)
        gl2.addWidget(self.sunsetTimeLabel, 3, 2)
        gl2.addWidget(self.sunsetTimeValueLabel, 3, 3)
        lowerWidget.setLayout(gl2)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(upperWidget)
        mainLayout.addWidget(lowerWidget)
        self.setLayout(mainLayout)

    def displayWeatherData(self, weather_data):
        pixmap = self.loadWeatherIcon(weather_data['weather_icon'])
        self.iconLabel.setPixmap(pixmap.scaled(80, 80))
        self.city.setText(f"<html><h1>{weather_data['city']}</h1></html>")

        timezone = weather_data['timezone']
        weather_info_date = time_format_for_location(weather_data['date'] + timezone)
        labelText = f"<html>On {weather_info_date.strftime('%a, %d %b, %Y - %I:%M %p')}<br/><b>{weather_data['weather_main']}</b></html>"
        self.weatherMain.setText(labelText)

        self.tempValueLabel.setText(f"<html>{weather_data['temp']} &deg;C</html>")
        self.feelsLikeTempValueLabel.setText(f"<html>{weather_data['feels_like_temp']} &deg;C</html>")
        self.minTempValueLabel.setText(f"<html>{weather_data['temp_min']} &deg;C</html>")
        self.maxTempValueLabel.setText(f"<html>{weather_data['temp_max']} &deg;C</html>")
        self.pressureValueLabel.setText(f"<html>{weather_data['pressure']}</html>")
        self.humidityValueLabel.setText(f"<html>{weather_data['humidity']} %</html>")

        sunrise_time = time_format_for_location(weather_data['sunrise_time'] + timezone)
        sunrise_time_str = sunrise_time.strftime('%I:%M %p')
        sunset_time = time_format_for_location(weather_data['sunset_time'] + timezone)
        sunset_time_str = sunset_time.strftime('%I:%M %p')

        self.sunriseTimeValueLabel.setText(f"<html>{sunrise_time_str}</html>")
        self.sunsetTimeValueLabel.setText(f"<html>{sunset_time_str}</html>")

class WeatherWindow(QWidget):
    def __init__(self, weather_data_dict, city):
        super().__init__()
        self.weather_widget = WeatherWidget(weather_data_dict)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} - Weather App")
        self.citiesLabel = QLabel("<html><b>Pick another city</html>")
        self.citiesCombo = QComboBox()
        self.citiesCombo.setEditable(False)
        self.setupUi(city)
        self.setWindowIcon(QIcon(os.path.join(APP_PATH, "images", "weather.png")))

    def setupUi(self, city):
        cities = getCities()
        print(cities)

        citySelIndex = -1
        for i, ct in enumerate(cities):
            self.citiesCombo.addItem(ct)
            if ct.lower() == city.lower():
                citySelIndex = i
        self.citiesCombo.setCurrentIndex(citySelIndex)
        self.citiesCombo.currentIndexChanged.connect(self.comboSelChanged)

        hl = QHBoxLayout()
        hl.addWidget(self.citiesLabel)
        hl.addWidget(self.citiesCombo)

        l = QVBoxLayout()
        l.addWidget(self.weather_widget)
        l.addLayout(hl)
        self.setLayout(l)
        self.setGeometry(50, 50, 300, 270)

    def comboSelChanged(self, newIndex):
        city = self.citiesCombo.currentText()
        print(f"New selected city {city}")
        weather_data = getWeather(city)
        if weather_data['cod'] != 200:
            QMessageBox.critical(self, "Error!", f"Weather data for {city} is not available!\r\nPlease choose another city",
                                 QMessageBox.Ok)
        else:
            print(weather_data)
            self.weather_widget.displayWeatherData(weather_data)

    def displayValues(self, weather_data_dict):
        self.weather_widget.displayWeatherData(weather_data_dict)


if __name__ == "__main__":
    # parse command line arguments
    ap = ArgumentParser()
    ap.add_argument("-c", "--city", required=False, default="Mumbai",
                    help="Enter name of city to display weather")
    args = vars(ap.parse_args())

    app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    # app = QApplication(sys.argv)

    # get weather location of Mumbai as dict
    weather_data = getWeather(args["city"])
    print(weather_data)
    # cities = getCities()
    # print(cities)

    widget = WeatherWindow(weather_data, args["city"])
    widget.show()

    sys.exit(app.exec())