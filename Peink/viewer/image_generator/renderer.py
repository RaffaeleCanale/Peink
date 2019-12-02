import os
import logging

from core.utils import file_utils
from viewer.image_generator.utils import templater


class Renderer:

    def __init__(self, epaper, browser):
        self.epaper = epaper
        self.browser = browser

    def render(self, widgets):
        index_file = self._generate_html(widgets)
        print(index_file)
        screenshot_file = self._capture_screenshot(index_file)
        # screenshot_file = self._convert_screenshot(screenshot_file)

        self.epaper.display(screenshot_file)

    def _generate_html(self, widgets):
        index_file = file_utils.get_package_file(__package__, 'index.html')
        html = templater.template(index_file, widgets=widgets)

        return file_utils.create_tmp_file(content=html, suffix='.html')

    def _capture_screenshot(self, html_file):
        screenshot_file = file_utils.create_tmp_file(suffix='.png')
        command = '{browser} --headless --screenshot={screenshot} --window-size=640,384 {file}'.format(
            browser=self.browser,
            file=html_file,
            screenshot=screenshot_file,
        )
        logging.debug('Executing: {}'.format(command))
        os.system(command)
        return screenshot_file

    def _convert_screenshot(self, image_file):
        converted_file = file_utils.create_tmp_file(suffix='.bmp')
        print(image_file)
        print(converted_file)
        command = 'convert "{input}" -resize 640x384\! -type bilevel "{output}"'.format(
            input=image_file,
            output=converted_file,
        )
        logging.debug('Executing: {}'.format(command))
        os.system(command)
        return converted_file