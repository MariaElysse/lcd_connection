from multiprocessing import Process, Pipe
import arrow
import requests
import ics
import string
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image, ImageDraw, ImageFont
import textwrap

import time

IMAGE_DIR = "icons/"
APIKEY = "9c2639dae29c05b601b637b9ea2e544e"

def weatherWriter(connexion):
    weather_dict = {}
    #Hardware setup
    DC = 23
    RST = 24
    SPI_PORT = 0
    SPI_DEVICE = 0
    display = LCD.PCD8544(DC,RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
    display.begin(contrast=60)
    display.clear()
    font = ImageFont.load('Tamsyn5x9r.pil')
    fontBig = ImageFont.load('Tamsyn6x12r.pil')
    fontSuperBig = ImageFont.truetype('vcr.ttf', 20)

    while True:
        if connexion.poll(None):
            weather_dict = connexion.recv()

        current_conditions = []
        try:
            current_conditions.append(weather_dict['currently']['summary'])
        except (KeyError):
            continue
        current_conditions.append("{0}C".format(str(weather_dict['currently']['temperature'])))
        current_conditions.append("Rain:" + str(weather_dict['currently']['precipProbability']) + " chance")

        con_icon = IMAGE_DIR + weather_dict['currently']['icon'] + ".png"
        icon = Image.open(con_icon)
        for item in current_conditions:
            display.clear()
            image = Image.new("1", (LCD.LCDWIDTH, LCD.LCDHEIGHT))
            draw = ImageDraw.Draw(image)
            draw.rectangle((0,0,LCD.LCDWIDTH, LCD.LCDHEIGHT), fill=255, outline=255)
            image.paste(icon, (0,0,LCD.LCDHEIGHT, LCD.LCDHEIGHT))
            itemWrapped = textwrap.wrap(item, 7)
            y = 0
            for line in itemWrapped:
                draw.text((48,y), line ,font=font)
                y+=7
            display.image(image)
            display.display()
            time.sleep(2)

def update():
    """this function should run forever"""
    start = arrow.now()
    weather_con_request = requests.get("https://api.forecast.io/forecast/9c2639dae29c05b601b637b9ea2e544e/34.0537,-118.2427?units=si")
    weather = weather_con_request.json()
    (receiver, sender) = Pipe()
    p = Process(target=weatherWriter, args=(receiver,))
    p.start()
    while True:
        if (arrow.now() - start).seconds % 300 <5:
            weather_con_request = requests.get("https://api.forecast.io/forecast/9c2639dae29c05b601b637b9ea2e544e/34.0537,-118.2427?units=si")
            weather = weather_con_request.json()
        sender.send(weather)

if __name__ == "__main__":
    update()
