from requests import get
from config import CONFIG
import json


class Github:
    """
    Class encapsulating GitHub API
    """

    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.github.com'
        self.owner = CONFIG['organization']

    def _build_request(self, path):
        """
        Builds the HTTP request
        :param path: The path to make the request to
        :return: The full request URL
        """
        request_url = "%s%s" % (self.base_url, path)
        return request_url

    def _make_request(self, url, **params):
        """
        Makes the HTTP request
        :param url: The URL to make the request to
        :param params: Optional parameters to include in the request
        :return: The response text
        """
        resp = get(url, params=params)
        if str(resp.status_code).startswith('2'):
            return json.loads(resp.text)
        else:
            return {}

    def get_pull_requests_by_repo(self, repo):
        """
        Gets all the open pull requests from a given repository
        :param repo: The repository to fetch the pull requests from
        :return: A list of pull request IDs
        """
        path = '/repos/%s/%s/pulls' % (self.owner, repo)
        url = self._build_request(path)
        pull_reauests = \
            self._make_request(url, state='open', access_token=self.token)
        return [pr['number'] for pr in pull_reauests]

    def get_comments_on_pull_request(self, pull_request_id, repo):
        """
        Gets all comments on a pull request
        :param pull_request_id: The ID of the pull request
        :param repo: The name of the repository
        :return: Information about each comment
        """
        path = '/repos/%s/%s/issues/%s/comments' % \
               (self.owner, repo, pull_request_id)
        url = self._build_request(path)
        return self._make_request(url, access_token=self.token)

    def build_pull_request_url(self, pull_request, repo):
        """
        Builds the URL to the pull request on GitHub
        :param pull_request: The ID of the pull request
        :param repo: The name of the repository
        :return: The URL to the pull request on GitHub
        """
        return 'https://github.com/%s/%s/pull/%s' \
               % (CONFIG['organization'], repo, pull_request)

    def check_for_pull_requests(self, repo):
        """
        Checks a repository for pull requests that need reviewing
        :param repo: The name of the repository
        :return: Dictionary containing URLs to the pull requests and the
            number of acceptence comments
        """
        response = {}
        for pull_request in self.get_pull_requests_by_repo(repo):
            approvals = 0
            for comment in self.get_comments_on_pull_request(pull_request, repo):
                for token in CONFIG['acceptance_tokens']:
                    if token in comment.get('body'):
                        approvals += 1
            url = self.build_pull_request_url(pull_request, repo)
            response[url] = approvals
        return response


