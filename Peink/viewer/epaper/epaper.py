import logging

from viewer.epaper.libs.epd7in5 import EPD
from PIL import Image

from core.utils.file_utils import checksum


class ePaper:

    def __init__(self):
        self.last_file_checksum = None

    def display(self, image_file):
        current_checksum = checksum(image_file)
        if current_checksum == self.last_file_checksum:
            logging.info('Display aborted because file is identical')
            return

        epd = EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        image = Image.open(image_file)
        epd.display(epd.getbuffer(image))

        logging.info("Goto Sleep...")
        epd.sleep()

        self.last_file_checksum = current_checksum
