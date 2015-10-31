from flask import Flask, render_template
from git import Github
from config import CONFIG
app = Flask(__name__)


@app.route('/')
def pull():
    g = Github(CONFIG['github_token'])
    accepted = []
    needs_peer_review = []
    for repo in CONFIG['repositories']:
        pull_requests = g.check_for_pull_requests(repo)
        for url, count in pull_requests.iteritems():
            if count >= CONFIG['acceptance_threshold']:
                accepted.append(url)
            else:
                needs_peer_review.append(url)

    response = {
        'accepted': accepted,
        'needs_peer_review': needs_peer_review
    }
    return render_template('template.html', data=response)


if __name__ == '__main__':
    app.run(debug=True)
