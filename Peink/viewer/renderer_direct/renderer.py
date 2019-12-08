from PIL import Image, ImageDraw

class Renderer:

    def __init__(self, epaper):
        self.epaper = epaper

    def render(self, widgets):
        fonts = self.epaper.get_fonts()

        image = Image.new('1', (self.epaper.width, self.epaper.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)

        for widget in widgets:
            widget.render(draw, fonts, self)
        self.epaper.display_image(image)
