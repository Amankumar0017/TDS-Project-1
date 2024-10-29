# TDS-Project-1
tds-project-1


# GitHub User and Repository Data
This repository contains data on GitHub users from Berlin with over 200 followers and their most recent repositories.
Data fetched using the GitHub API.

users.csv includes 601 rows and 11 columns, covering GitHub user details such as login, name, company, location, email, hireable, bio, public_repos, followers, following, and created_at. repositories.csv contains 41,069 rows and 9 columns, detailing users' repositories, including login, full_name, created_at, stargazers_count, watchers_count, language, has_projects, has_wiki, and license_name.

# Key Observations from the Data Analysis
User Statistics: Users in the dataset have, on average, 101 public repositories and 765 followers, with a median follower count of 377. The user with the highest followers has 26,445.

Top Companies: 
  -Popular companies include Microsoft (8 users), GitHub (6 users), and Zalando (5 users), showing an active developer presence in these firms.
Top Languages:
  -The most common languages are JavaScript (6,815 repositories), Python (3,592), and Ruby (1,948), reflecting popular choices for open-source contributions.
Repository Stats:
  -Repositories have an average of 46 stars and watchers, indicating steady interest and engagement across repositories.
Licensing:
  -The MIT license is most common (11,123 repos), followed by Apache-2.0 (4,380 repos), with a preference for permissive licensing.

# Data Scraping Explanation:
The GitHub API was used to collect user and repository data for those in a specific city with over a threshold number of followers. The data was parsed and saved in users.csv and repositories.csv, preserving API values for consistency.

# Interesting Finding: 
JavaScript and Python dominate repository languages, highlighting their popularity in diverse projects. Surprisingly, Ruby remains a strong choice, indicating its continued relevance.

# Actionable Recommendation: 
Developers should consider adopting MIT or Apache-2.0 licenses, as they are widely used and permissive, enhancing the appeal for open-source contributions.
