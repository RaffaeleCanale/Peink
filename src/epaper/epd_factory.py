from lib import epd7in5
from fake_epd import FakeEpd

def get_epd():
    if False:
        return FakeEpd()
    else:
        return epd7in5.EPD()
