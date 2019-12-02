import sys
import logging

from core.utils import file_utils
from viewer.epaper.fake_epaper import FakeEpaper
from core.tasks.task_manager import TaskManager
from viewer.image_generator.renderer import Renderer
from viewer.image_generator.widgets.tasks import tasks_renderer

logging.basicConfig(level=logging.DEBUG)


def read_config():
    config_file = file_utils.get_package_file(__package__, '../Secrets/config.json')
    return file_utils.read_json(config_file)


def get_widgets(config):
    task_manager = TaskManager(
        jira_config=config['jira'],
        github_config=config['github'],
    )
    task_manager.fetch()
    tasks_widget = tasks_renderer.render(task_manager)
    return [tasks_widget]


if __name__ == '__main__':
    config = read_config()
    widgets = get_widgets(config)

    if len(sys.argv) > 1 and sys.argv[1] == '--fake':
        ep = FakeEpaper()
    else:
        # Lazy import because this depends on RPi only dependencies
        from viewer.epaper.epaper import ePaper
        ep = ePaper()
    renderer = Renderer(ep)
    renderer.render(widgets)

