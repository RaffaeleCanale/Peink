from core.utils.http_client import HttpClient
from core.integrations.github.github_pr import GithubPr


class GitHubApi:

    def __init__(self, token, username):
        self.client = HttpClient(
            base_url='',
            headers={
                'Authorization': 'Token {}'.format(token)
            }
        )
        self.username = username

    def _get_prs_assigned_to_me(self):
        response = self.client.get('https://api.github.com/search/issues', params={
            'q': 'is:pr state:open author:{}'.format(self.username)
        })
        return response['items']

    def _get_prs_created_by_me(self):
        response = self.client.get('https://api.github.com/search/issues', params={
            'q': 'is:pr state:open assignee:{}'.format(self.username)
        })
        return response['items']

    def _get_prs_assigned_to_me_as_reviewer(self):
        response = self.client.get('https://api.github.com/search/issues', params={
            'q': 'is:pr state:open review-requested:{}'.format(self.username)
        })
        return response['items']

    def get_prs_related_to_me(self):
        items = self._get_prs_assigned_to_me() \
                + self._get_prs_assigned_to_me_as_reviewer() \
                + self._get_prs_created_by_me()
        return self._process_prs(items)

    def _process_prs(self, items):
        result = {}
        for item in items:
            pr = GithubPr(item)
            if pr.id not in result:
                data = self.client.get(pr.meta_self())
                pr.pr_json = data
                result[pr.id] = pr
        return result.values()