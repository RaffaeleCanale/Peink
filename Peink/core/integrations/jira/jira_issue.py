from core.integrations.jira.jira_status import JiraStatus


class JiraIssue:

    def __init__(self, json, username):
        self.json = json
        self.usernae = username

    @property
    def id(self):
        return self.json.get('key')

    @property
    def name(self):
        return self._fields('summary')

    @property
    def is_mine(self):
        return self._fields('assignee', {}).get('name') == self.usernae

    @property
    def status(self):
        status = self._fields('status', {}).get('name')
        if not status:
            return None

        if status == 'Confirmed':
            return JiraStatus.CONFIRMED
        elif status == 'To do':
            return JiraStatus.TODO
        elif status == 'In Progress':
            return JiraStatus.IN_PROGRESS
        elif status == 'Code Review':
            return JiraStatus.CODE_REVIEW
        elif status == 'QA':
            return JiraStatus.QA
        elif status == 'Done':
            return JiraStatus.DONE
        else:
            return None

    def _fields(self, name, default=None):
        fields = self.json.get('fields')
        return fields[name] if fields else default
