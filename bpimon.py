#!/usr/bin/python

import logging
from waveshare_epd import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont
import speedtest
import time

logging.basicConfig(level=logging.DEBUG)

def main():
    
    epd = epd2in13_V2.EPD()
    logging.info("init")
    epd.init(epd.FULL_UPDATE)

    logging.info("get the speedtest results") 
    s = speedtest.Speedtest()
    s.get_best_server()
    bw_down = s.download()
    bw_up = s.upload()
    results_dict = s.results.dict()
    ping = (results_dict['ping'])
    
    image = Image.new('1', (epd2in13_V2.EPD_HEIGHT,epd2in13_V2.EPD_WIDTH), 255)  
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('fonts/Roboto-Thin.ttf', 14)
    font2 = ImageFont.truetype('fonts/DroidSans.ttf', 24)
    font3 = ImageFont.truetype('fonts/Roboto-Light.ttf', 10)
    font4 = ImageFont.truetype('fonts/Roboto-Thin.ttf', 10)
    font5 = ImageFont.truetype('fonts/Verdana_Bold.ttf', 20)

    draw.rectangle((0, 0, 250, 40), fill = 0)
    draw.text((5, 10), 'Bandwidth PiMonitor', font = font5, fill = 255)

    start_y = 50
    offset_y_1 = 20
    offset_y_2 = 45 

    draw.text((0, start_y), "Ping:", font=font)
    draw.text((0, start_y + offset_y_1), ('{:5.1f}'.format(ping)), font=font2)
    draw.text((0, start_y + offset_y_2), "ms", font=font3)	

    draw.text((80, start_y), "Download:", font=font)
    draw.text((80, start_y + offset_y_1), ('{:5.2f}'.format(bw_down/1E6,2)), font=font2)
    draw.text((80, start_y + offset_y_2), 'Mbps', font=font3)

    draw.text((170, start_y), "Upload:", font=font)
    draw.text((170, start_y + offset_y_1), ('{:4.2f}'.format(bw_up/1E6,2)), font=font2)
    draw.text((170, start_y + offset_y_2), 'Mbps', font=font3)

    current_time = time.strftime("%H:%M:%S, %d.%m.%Y")
    draw.text((6, 110), 'tested @' + current_time, font=font3)

    logging.info("clear and display the results")
    epd.Clear(0xFF)
    epd.display(epd.getbuffer(image.rotate(180,expand=True)))
    epd.sleep()
    
if __name__ == '__main__':
    main()

