import logging
import os

from PIL import Image, ImageDraw, ImageFont
from core.utils import file_utils


class FakeEpaper:

    def display_file(self, image_file):
        logging.info('Displaying: {}'.format(image_file))
        os.system('xdg-open {}'.format(image_file))

    def display_image(self, image):
        file = file_utils.create_tmp_file(suffix='.png')
        image.save(file, "PNG")

        logging.info('Displaying: {}'.format(file))
        os.system('xdg-open {}'.format(file))

    def get_drawable_image(self):
        image = Image.new('1', (640, 384), 255)  # 255: clear the frame
        return ImageDraw.Draw(image)

    def get_fonts(self):
        font_file = file_utils.get_package_file(__package__, 'libs/Font.ttc')
        return {
            '24': ImageFont.truetype(font_file, 24),
            '18': ImageFont.truetype(font_file, 18),
            '11': ImageFont.truetype(font_file, 11),
        }

    @property
    def width(self):
        return 640

    @property
    def height(self):
        return 384
