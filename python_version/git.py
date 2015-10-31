__author__ = 'alexkahan'

from requests import get
from config import CONFIG
import json


class Github:

    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.github.com'
        self.owner = CONFIG['organization']

    def _build_request(self, path):

        request_url = "%s%s" % (self.base_url, path)
        return request_url

    def _make_request(self, url, **params):
        try:
            resp = get(url, params=params)
            return json.loads(resp.text)
        except Exception:
            pass

    def get_pull_requests_by_repo(self, repo):
        path = '/repos/%s/%s/pulls' % (self.owner, repo)
        url = self._build_request(path)
        pull_reauests = \
            self._make_request(url, state='open', access_token=self.token)
        return [pr['number'] for pr in pull_reauests]

    def get_comments_on_pull_request(self, pull_request_id, repo):
        path = '/repos/%s/%s/issues/%s/comments' % \
               (self.owner, repo, pull_request_id)
        url = self._build_request(path)
        return self._make_request(url, access_token=self.token)

    def build_pull_request_url(self, pull_request, repo):
        return 'https://github.com/%s/%s/pull/%s' \
               % (CONFIG['organization'], repo, pull_request)

    def check_for_pull_requests(self, repo):
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


