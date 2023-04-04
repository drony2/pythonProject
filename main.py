from configparser import ConfigParser
import requests
from tkinter import *
from tkinter import messagebox

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config['sos']['api']
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'


def getweather(city):
    result = requests.get(url.format(city, api_key))

    if result:
        json = result.json()
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = round(temp_kelvin - 273.15)
        weather1 = json['weather'][0]['main']
        colorTempChanging(temp_celsius)
        final = [city, country, temp_kelvin,
                 temp_celsius, weather1]
        return final
    else:
        print("Такой город не найден")


def search():
    city = city_text.get()
    weather = getweather(city)

    if weather:
        location_lbl['text'] = '{} ,{}'.format(weather[0], weather[1])
        temperature_label['text'] = str(weather[3]) + " °C"
        weather_l['text'] = weather[4]

    else:
        messagebox.showerror('Ошибка', "Невозможно найти {}".format(city))


def colorTempChanging(temp):
    if temp < 0 and temp > -25:
        app.configure(background='blue')
    elif temp >= 0 and temp < 25:
        app.configure(background='yellow')
    elif temp >= 25:
        app.configure(background='red')
    elif temp <= -25:
        app.configure(background='#0033ff')
    else:
        app.configure(background='white')


app = Tk()

app.title("Погода)")
app.geometry("300x300")

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text, font={'regular', 15})
city_entry.pack(pady=30, padx=2)

Search_btn = Button(app, text="Найти погоду",
                    width=15, command=search, padx=3, pady=3)
Search_btn.pack()

location_lbl = Label(app, text="",
                     font={'bold', 20}, pady=10)
location_lbl.pack()

temperature_label = Label(app, text="",
                          font={'regular', 20})
temperature_label.pack()

weather_l = Label(app, text="", font={'regular', 20})
weather_l.pack()

app.mainloop()