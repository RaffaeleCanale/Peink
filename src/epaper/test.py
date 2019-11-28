#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

import logging
from lib import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5 Demo")

    epd = epd7in5.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    logging.info("FOOBAR")
    Himage = Image.open('./its-alive.bmp')
    epd.display(epd.getbuffer(Himage))

    # logging.info("Clear...")
    # epd.init()
    # epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()