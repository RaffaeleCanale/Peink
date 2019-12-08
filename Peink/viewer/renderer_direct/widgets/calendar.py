PADDING = 5
FONT_SIZE = '11'
LINE_HEIGHT = 15


class GCalendarRenderer:

    def __init__(self, gcalendar_client):
        self.client = gcalendar_client

    def render(self, draw, fonts, renderer):
        event = self.client.get_my_next_accepted_event()

        height = renderer.epaper.height
        draw.text(
            (PADDING, height - PADDING - 2*LINE_HEIGHT),
            event.get('summary', '???'),
            font=fonts[FONT_SIZE],
            fill=0,
        )
        draw.text(
            (PADDING, height - PADDING - LINE_HEIGHT),
            event.get('location', '(No room)'),
            font=fonts[FONT_SIZE],
            fill=0,
        )
