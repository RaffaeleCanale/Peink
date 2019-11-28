#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

import logging
import time
from epd_factory import get_epd
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5 Demo")

    epd = get_epd()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    logging.info("FOOBAR")
    # Himage = Image.open('./its-alive.bmp')
    Himage = Image.open('./screenshot.png')
    # Himage = Image.open('./7in5.bmp')
    # print(Himage.tobytes())
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