# TDS-Project-1



# GitHub User and Repository Data
This repository contains data on GitHub users from Berlin with over 200 followers and their most recent repositories.
Data fetched using the GitHub API.

users.csv includes 603 rows and 11 columns,Average Followers: 763,Average Public Repos: 101 ,covering GitHub user details such as login, name, company, location, email, hireable, bio, public_repos, followers, following, and created_at. repositories.csv contains 60,552 rows and 9 columns,Average Stars per Repository: 35,Most Common Language: JavaScript, detailing users' repositories, including login, full_name, created_at, stargazers_count, watchers_count, language, has_projects, has_wiki, and license_name.

# Key Observations from the Data Analysis
The repositories dataset shows an average of 35 stargazers and watchers, with JavaScript as the most common language. The majority of users have modest followings, with an average of 763 followers and 123 followings. User engagement and repository popularity are highly skewed, with a few high-profile repositories.

Top Companies: 
  -Popular companies include Microsoft (8 users), GitHub (6 users), and Zalando (5 users), showing an active developer presence in these firms.
  
Top Languages:
  -The most common languages are JavaScript (6,815 repositories), Python (3,592), and Ruby (1,948), reflecting popular choices for open-source contributions.
  
Repository Stats:
  -Repositories have an average of 46 stars and watchers, indicating steady interest and engagement across repositories.
  
Licensing:
  -The MIT license is most common (11,123 repos), followed by Apache-2.0 (4,380 repos), with a preference for permissive licensing.

# Data Scraping Explanation:
I used the GitHub API to extract user data for individuals in a specified city with over a set number of followers. For each user, I retrieved up to 500 recent repositories, collecting details like stars, language, and license, before organizing the data into CSV files.

# Interesting Finding: 
JavaScript and Python dominate repository languages, highlighting their popularity in diverse projects. Surprisingly, Ruby remains a strong choice, indicating its continued relevance.

# Actionable Recommendation: 
Developers aiming for visibility should consider contributing to JavaScript projects, given its popularity. Additionally, focusing on creating high-quality repositories with frequent updates and clear documentation could improve engagement and attract more followers and stars.
