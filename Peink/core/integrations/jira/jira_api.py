from core.integrations.jira.jira_issue import JiraIssue


class JiraApi:

    def __init__(self, http_client, username):
        self.client = http_client
        self.username = username

    def get_issues_related_to_me(self):
        # TODO QA assignee tasks
        return self.get_my_issues()

    def get_my_issues(self):
        issues = self.client.post('/rest/api/3/search', body={
            'jql': 'assignee = currentUser() AND status in ("Code Review", "In Progress", QA, "To Do")',
        })
        return [JiraIssue(issue, self.username) for issue in issues['issues']]
