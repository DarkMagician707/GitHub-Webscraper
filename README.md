# GitHub-Webscraper
This is a project that I did for a module in 3rd year University where we use the GitHub API to create a webscraper that scrapes information of users, companies and their repos

To use this project, run the github_api.py file.
Open localhost:5000
Use /users/{username} to find a user on GitHub and to view their curated information. This can be a user or company page.
Use /users/{username}/repos to view all the repos that they have publically available. Can add query parameters to request:
  - Use sort={element} to sort the list in descending order by the element you specify. Use direction={asc/desc} to change sort order
  - Use page={pageNumber} to find repos on a certain page of the repos pages of GitHub users
