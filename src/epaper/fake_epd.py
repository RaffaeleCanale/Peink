import logging


class FakeEpd:

    def init(self):
        logging.info('INIT')

    def Clear(self):
        logging.info('CLEAR')

    def sleep(self):
        logging.info('SLEEP')

    def display(self, img):
        logging.info('DISPLAY')

    def getbuffer(self, img):
        return None