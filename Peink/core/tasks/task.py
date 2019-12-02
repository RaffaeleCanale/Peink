from core.integrations.jira.jira_issue import JiraStatus
from core.tasks.task_status import TaskStatus

class Task:

    def __init__(self, jira_issue=None):
        self.jira_issue = jira_issue
        self.github_prs = []

    @property
    def id(self):
        if self.jira_issue:
            return self.jira_issue.id
        return self.github_prs[0].branch

    @property
    def name(self):
        if self.jira_issue:
            return self.jira_issue.name
        return self.github_prs[0].name

    @property
    def statuses(self):
        if len(self.github_prs) > 0:
            return [self._my_status_from_github_pr(pr) for pr in self.github_prs]
        else:
            return [self._my_status_from_jira]

    @property
    def _my_status_from_jira(self):
        status = self.jira_issue.status
        is_mine = self.jira_issue.is_mine

        if status == JiraStatus.CONFIRMED:
            return TaskStatus.WAITING_FOR_CHANGES
        elif status == JiraStatus.TODO:
            return TaskStatus.TODO if is_mine else TaskStatus.WAITING_FOR_CHANGES
        elif status == JiraStatus.IN_PROGRESS:
            return TaskStatus.IN_PROGRESS if is_mine else TaskStatus.WAITING_FOR_CHANGES
        elif status == JiraStatus.CODE_REVIEW:
            return TaskStatus.WAITING_FOR_REVIEW if is_mine else TaskStatus.REVIEW_REQUESTED
        elif status == JiraStatus.QA:
            # TODO Check QA assignee?
            return TaskStatus.WAITING_FOR_QA if is_mine else TaskStatus.QA_REQUESTED
        elif status == JiraStatus.DONE:
            return TaskStatus.DONE

    def _my_status_from_github_pr(self, github_pr):
        if github_pr.is_assigned_to_me:
            if github_pr.is_wip:
                return TaskStatus.WAITING_FOR_CHANGES
            elif github_pr.code_ready_for_review:
                return TaskStatus.REVIEW_REQUESTED
            elif github_pr.is_merged or github_pr.is_ready_to_merge:
                return TaskStatus.DONE
            else:
                return TaskStatus.WAITING_FOR_CHANGES
        else:
            if github_pr.is_wip:
                return TaskStatus.IN_PROGRESS
            elif github_pr.has_requested_changes:
                return TaskStatus.CHANGES_REQUESTED
            elif github_pr.has_requested_reviews:
                return TaskStatus.WAITING_FOR_REVIEW
            elif github_pr.is_approved:
                return TaskStatus.APPROVED
            elif github_pr.is_merged or github_pr.is_ready_to_merge:
                return TaskStatus.DONE
            else:
                return TaskStatus.IN_PROGRESS
