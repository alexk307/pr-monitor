# pr-monitor

Simple web app to monitor your organizations repositories for Pull Requests that need reviews.

Edit the `config.py` file to setup.
  - `acceptence_tokens`: These are the words/phrases/symbols your organization uses to express that the pull request is accepted
  - `acceptence_threshold`: This is the number of `acceptence_tokens` needed to be considered accepted
  - `github_token`: Your Github API token
  - `organization`: The name of your organization on Github
  - `repositories`: The names of repositories in your organization that you are interested in monitoring
