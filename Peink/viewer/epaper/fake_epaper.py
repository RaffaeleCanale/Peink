import logging
import os

class FakeEpaper:

    def display(self, image_file):
        logging.info('Displaying: {}'.format(image_file))
        os.system('xdg-open {}'.format(image_file))

