import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши название города и я пришлю сводку погоды!")



@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }


    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()


        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_discription = data["weather"][0]["main"]
        if weather_discription in code_to_smile:
            wd = code_to_smile[weather_discription]
        else:
            wd = "Выгляни в окно и сам посмотри!"

        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(
            f"Дата: {datetime.datetime.now().strftime('%Y-%m-%d %H-%M')}\n"
            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
            f"Влажность: {humidity} %\nВетер: {wind} м/с\n"
            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца вручную: {sunset_timestamp}\n"
            f"Продолжительность дня: {length_of_day}\n"
            f"Хорошего дня!"
        )


    except:
        await message.reply("Проверьте название города")



if '__name__ == __main__':
    executor.start_polling(dp)
