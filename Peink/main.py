import sys
import logging

from core.integrations.calendar.gcalendar_client import GCalendarClient
from core.utils import file_utils
from viewer.epaper.fake_epaper import FakeEpaper
from core.tasks.task_manager import TaskManager

from viewer.renderer_direct.renderer import Renderer
from viewer.renderer_direct.widgets.calendar import GCalendarRenderer
from viewer.renderer_direct.widgets.tasks import TasksRenderer

# from viewer.renderer_html.renderer import Renderer
# from viewer.renderer_html.widgets.tasks import tasks_renderer

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

    gcalendar = GCalendarClient(
        credentials_file=file_utils.get_package_file(__package__, '../Secrets/google_calendar_credentials.json'),
        pickle_file=file_utils.get_package_file(__package__, '../Secrets/google_calendar_token.pickle'),
        calendars=config.get('googleCalendar').get('calendars'),
        users=config.get('googleCalendar').get('users'),
    )

    return [
        TasksRenderer(task_manager),
        GCalendarRenderer(gcalendar),
    ]
    # tasks_widget = tasks_renderer.render(task_manager)
    # return [tasks_widget]


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

