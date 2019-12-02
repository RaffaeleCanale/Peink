from core.utils.http_client import HttpClient
from core.integrations.jira.jira_api import JiraApi
from core.tasks.task import Task
from core.integrations.github.github_api import GitHubApi


class TaskManager:

    def __init__(self, jira_config, github_config):
        jira_client = HttpClient(
            base_url=jira_config['hostname'],
            headers={
                'cookie': jira_config['cookie'],
            }
        )
        self.jira = JiraApi(jira_client, jira_config['username'])
        self.github = GitHubApi(
            token=github_config['token'],
            username=github_config['username'],
        )
        self.tasks = []

    def fetch(self):
        prs = self.github.get_prs_related_to_me()
        issues = self.jira.get_issues_related_to_me()

        tasks_map = {}
        for issue in issues:
            task = Task(jira_issue=issue)
            tasks_map[task.id] = task

        for pr in prs:
            task = tasks_map.get(pr.branch)
            if task:
                task.github_prs.append(pr)
            else:
                task = Task()
                task.github_prs.append(pr)
                tasks_map[task.id] = task
                # TODO Fetch from Jira?
        self.tasks = tasks_map.values()
