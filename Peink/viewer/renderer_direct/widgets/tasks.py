from core.tasks.task_status import TaskStatus

ACTIONABLE_STATUSES = [
    TaskStatus.APPROVED,
    TaskStatus.CHANGES_REQUESTED,
    TaskStatus.IN_PROGRESS,
    TaskStatus.REVIEW_REQUESTED,
    TaskStatus.QA_REQUESTED,
    TaskStatus.TODO,
]


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


PADDING = 5
FONT_SIZE = '11'
LINE_HEIGHT = 15

FIRST_COLUMN_WIDTH = 70
FIRST_COLUMN_CHAR_TRIM = 10

SECOND_COLUMN_CHAR_TRIM = 120
MAX_LINES = 10


class TasksRenderer:

    def __init__(self, tasks_manager):
        tasks = [task for task in tasks_manager.tasks if _is_actionable(task)]
        self.tasks = _sort_by_priority(tasks)

    def render(self, draw, fonts, renderer):
        font = fonts[FONT_SIZE]

        current_line = PADDING
        for index in range(0, min(MAX_LINES, len(self.tasks))):
            task = self.tasks[index]
            # ID
            draw.text((PADDING, current_line), self._trim(task.id, FIRST_COLUMN_CHAR_TRIM), font=font, fill=0)
            # Title
            draw.text(
                (PADDING + FIRST_COLUMN_WIDTH, current_line),
                self._trim(task.name, SECOND_COLUMN_CHAR_TRIM),
                font=font,
                fill=0,
            )

            current_column = PADDING + FIRST_COLUMN_WIDTH
            for status in task.statuses:
                draw.text((current_column, current_line + LINE_HEIGHT), self._trim(status, SECOND_COLUMN_CHAR_TRIM), font=font, fill=0)
                current_column += 150  # TODO
            current_line += (2*LINE_HEIGHT)

    def _trim(self, text, length):
        if len(text) > length:
            return text[0:length-3] + '...'
        return text
