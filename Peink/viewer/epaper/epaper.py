import logging

from viewer.epaper.libs.epd7in5 import EPD_HEIGHT
from viewer.epaper.libs.epd7in5 import EPD_WIDTH
from viewer.epaper.libs.epd7in5 import EPD
from PIL import Image, ImageDraw, ImageFont

from core.utils import file_utils


class ePaper:

    def __init__(self):
        self.last_file_checksum = None

    def display_file(self, image_file):
        current_checksum = file_utils.checksum(image_file)
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

    def display_image(self, image):
        epd = EPD()
        epd.init()
        epd.Clear()

        epd.display(epd.getbuffer(image))

        epd.sleep()

    def get_drawable_image(self):
        image = Image.new('1', (self.width, self.height), 255)  # 255: clear the frame
        return ImageDraw.Draw(image)

    def get_fonts(self):
        font_file = file_utils.get_package_file(__package__, 'libs/Font.ttc')
        return {
            '24': ImageFont.truetype(font_file, 24),
            '18': ImageFont.truetype(font_file, 18),
        }

    @property
    def width(self):
        return EPD_WIDTH

    @property
    def height(self):
        return EPD_HEIGHT
