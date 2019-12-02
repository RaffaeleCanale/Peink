from core.integrations.github.github_pr_labels import GithubPrLabels


class GithubPr:

    def __init__(self, issue_json=None, pr_json=None):
        self.issue_json = issue_json
        self.pr_json = pr_json

    def meta_self(self):
        if self.issue_json:
            return self.issue_json.get('pull_request').get('url')
        if self.pr_json:
            return self.pr_json.get('url')
        return None

    @property
    def id(self):
        return self.meta_self()

    @property
    def branch(self):
        if self.pr_json:
            return self.pr_json.get('head').get('ref')
        return None

    @property
    def name(self):
        return self.pr_json.get('title')

    @property
    def is_assigned_to_me(self):
        assignees = self.pr_json.get('assignees') \
                    + self.pr_json.get('requested_reviewers')
        assignees = [user['login'] for user in assignees]
        return 'RaffaeleCanale' in assignees

    @property
    def is_wip(self):
        return GithubPrLabels.WORK_IN_PROGRESS in self.labels

    @property
    def code_ready_for_review(self):
        return GithubPrLabels.CODE_READY_FOR_REVIEW in self.labels

    @property
    def is_merged(self):
        return self.pr_json.get('state') != 'open'

    @property
    def is_ready_to_merge(self):
        return GithubPrLabels.READY_TO_MERGE in self.labels

    @property
    def has_requested_changes(self):
        labels = self.labels
        return GithubPrLabels.CODE_CHANGES_REQUIRED in labels \
               or GithubPrLabels.UI_CHANGES_REQUIRED in labels \
               or GithubPrLabels.PRODUCT_CHANGES_REQUIRED in labels

    @property
    def has_requested_reviews(self):
        labels = self.labels
        return GithubPrLabels.CODE_READY_FOR_REVIEW in labels \
               or GithubPrLabels.UI_READY_FOR_REVIEW in labels \
               or GithubPrLabels.PRODUCT_READY_FOR_REVIEW in labels

    @property
    def is_approved(self):
        return GithubPrLabels.CODE_APPROVED in self.labels

    @property
    def labels(self):
        return [label.get('name') for label in self.pr_json.get('labels', [])]
