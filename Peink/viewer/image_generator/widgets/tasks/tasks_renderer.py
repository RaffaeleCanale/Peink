from core.utils import file_utils
from viewer.image_generator.utils import templater
from core.tasks.task_status import TaskStatus

ACTIONABLE_STATUSES = [
    TaskStatus.APPROVED,
    TaskStatus.CHANGES_REQUESTED,
    TaskStatus.IN_PROGRESS,
    TaskStatus.REVIEW_REQUESTED,
    TaskStatus.QA_REQUESTED,
    TaskStatus.TODO,
]


def render(tasks_manager):
    html_file = file_utils.get_package_file(__package__, 'tasks.html')

    tasks = [task for task in tasks_manager.tasks if _is_actionable(task)]
    tasks = _sort_by_priority(tasks)
    return templater.template(html_file, tasks=tasks)


def _sort_by_priority(tasks):
    def task_priority(task):
        return min([ACTIONABLE_STATUSES.index(status) for status in task.statuses if status in ACTIONABLE_STATUSES])
    return sorted(tasks, key=task_priority)


def _is_actionable(task):
    statuses = task.statuses
    for status in statuses:
        if status in ACTIONABLE_STATUSES:
            return True
    return False
