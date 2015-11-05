# pr-monitor

Simple web app to monitor your organizations repositories for Pull Requests that need reviews.

Edit the `config.py` file to setup.
  - `acceptance_tokens`: These are the words/phrases/symbols your organization uses to express that the pull request is accepted
  - `acceptance_threshold`: This is the number of `acceptance_tokens` needed to be considered accepted
  - `github_token`: Your Github API token
  - `organization`: The name of your organization on Github
  - `repositories`: The names of repositories in your organization that you are interested in monitoring
