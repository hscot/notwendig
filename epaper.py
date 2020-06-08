#!/usr/bin/python
import sys
import signal
import epd2in13_V2
import epdconfig
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from newsapi import NewsApiClient
import json
import requests
from datetime import date

api = NewsApiClient(api_key='0233006c7dc448ffaffea5cdfd337976')

top_headlines = api.get_top_headlines(sources='die-zeit', language='de')

#Checks if python 3+ is being used, otherwise an exception is thrown
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3.0 or greater!")

#Main function

def main():
    epd = epd2in13_V2.EPD()
    while True:
        try:
            print("Clear...")
            epd.init(epd.FULL_UPDATE) #Initiates the E-Paper Display; Also wakes up from deep sleep
            epd.Clear(0xFF) #Sets the screen to white
            HBlackimage = Image.new('1', (epd2in13_V2.EPD_HEIGHT, epd2in13_V2.EPD_WIDTH), 255)

            print("Drawing...")
            drawblack = ImageDraw.Draw(HBlackimage)
            font20 = ImageFont.truetype('fonts/arial.ttf', 20)
            font12 = ImageFont.truetype('fonts/arial.ttf', 12)
            
            ######Test for updating time, but static headlines
            time_image = Image.new('1', (epd.height, epd.width), 255)
            time_draw = ImageDraw.Draw(time_image)

            epd.init(epd.FULL_UPDATE)
            epd.displayPartBaseImage(epd.getbuffer(time_image))
            epd.init(epd.PART_UPDATE)

            time_draw.text((0, 10), "Source: " + api.get_sources, font = fon12, fill = 0)
            while(True):
                time_draw.rectangle((180, 0, 250, 30), fill=255)
                time_draw.text((180, 0), time.strftime('%H:%M'), font = font20, fill = 0)
                epd.displayPartial(epd.getbuffer(time_image))

        except IOError as e:
            print('traceback.format_exec():\n%s', traceback.format_exc())
            epdconfig.module_init()
            epdconfig.module_exit()
            exit()
        time.sleep(60)

def ctrl_c_handler(signal, frame):
    print('Control-C Pressed - Exiting!')
    epdconfig.module_init()
    epdconfig.module_exit()
    exit(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

if __name__ == '__main__':
    main()

