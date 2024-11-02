# -*- coding: utf-8 -*-


!pip install python-dotenv

import os
import requests
import pandas as pd
import csv
from dotenv import load_dotenv

# Load GitHub token from .env file
#load_dotenv()
#GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_TOKEN = "token"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_users_in_berlin():
    users = []
    query = "location:Berlin+followers:>200"
    page = 1
    per_page = 100
    total_users = 0

    while True:
        url = f"https://api.github.com/search/users?q={query}&per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)
        print(f"Fetching page {page}...")

        if response.status_code != 200:
            print("Error fetching data:", response.json())
            break

        data = response.json()
        users.extend(data['items'])
        total_users += len(data['items'])

        if len(data['items']) < per_page:
            break

        page += 1

    detailed_users = []
    for user in users:
        user_info = get_user_details(user['login'])
        detailed_users.append(user_info)

    return detailed_users

def get_user_details(username):
    user_url = f"https://api.github.com/users/{username}"
    user_data = requests.get(user_url, headers=HEADERS).json()

    return {
        'login': user_data['login'],
        'name': user_data['name'],
        'company': clean_company_name(user_data['company']),
        'location': user_data['location'],
        'email': user_data['email'],
        'hireable': user_data['hireable'],
        'bio': user_data['bio'],
        'public_repos': user_data['public_repos'],
        'followers': user_data['followers'],
        'following': user_data['following'],
        'created_at': user_data['created_at'],
    }

def clean_company_name(company):
    if company:
        company = company.strip().upper()
        if company.startswith('@'):
            company = company[1:]
    return company

def get_user_repos(username):
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=500"
    response = requests.get(repos_url, headers=HEADERS)
    repos_data = response.json()

    repos = []
    for repo in repos_data:
        repos.append({
            'login': username,
            'full_name': repo['full_name'],
            'created_at': repo['created_at'],
            'stargazers_count': repo['stargazers_count'],
            'watchers_count': repo['watchers_count'],
            'language': repo['language'],
            'has_projects': repo['has_projects'],
            'has_wiki': repo['has_wiki'],
            'license_name': repo['license']['key'] if repo['license'] else None,
        })

    return repos

def save_users_to_csv(users):
    with open('users.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
        writer.writeheader()
        writer.writerows(users)

def save_repos_to_csv(repos):
    with open('repositories.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'])
        writer.writeheader()
        writer.writerows(repos)

if __name__ == "__main__":
    users = get_users_in_berlin()
    save_users_to_csv(users)

    all_repos = []
    for user in users:
        repos = get_user_repos(user['login'])
        all_repos.extend(repos)

    save_repos_to_csv(all_repos)
    print("Done")

import pandas as pd

# Load data - adjust file paths as needed
users = pd.read_csv("/content/users.csv")
repos = pd.read_csv("/content/repositories.csv")

users.info()

repos.info()

# 1 Extracting top 5 users in Berlin with the highest followers

# Filter for Berlin users and sort by followers
top_5_users_sg = users[users['location'].str.contains('Berlin', case=False, na=False)]
top_5_users_sg = top_5_users_sg.sort_values(by='followers', ascending=False)

# Extract top 5 and their logins
top_5_users_logins = top_5_users_sg['login'].head(5).tolist()
top_5_users_logins_output = ','.join(top_5_users_logins)
top_5_users_logins_output

# 2 Sort Berlin users by registration date
earliest_users_sg = users[users['location'] == 'Berlin'].sort_values(by='created_at')
earliest_users_sg = earliest_users_sg['login'].head(5).tolist()
print(','.join(earliest_users_sg))

# 3 Count license occurrences, ignoring missing values
licenses = repos['license_name'].dropna().value_counts().head(3).index.tolist()
print(','.join(licenses))

# 4 Find the most common company
common_company = users['company'].dropna().mode().iloc[0]
print(common_company)

# 5 Find the most used language
popular_language = repos['language'].mode().iloc[0]
print(popular_language)

# 6 Convert 'created_at' to datetime objects
users['created_at'] = pd.to_datetime(users['created_at'])

# Filter users who joined after 2020
# Changed: Create a timezone-aware timestamp for comparison
recent_users = users[users['created_at'] > pd.Timestamp('2020-01-01', tz='UTC')]

# Merge with repos to get language information
user_repos = pd.merge(recent_users, repos, on='login', how='left')

# Count language occurrences, ignoring missing values
language_counts = user_repos['language'].value_counts().dropna()

# Get the second most popular language
second_popular_language = language_counts.index[1]

print(second_popular_language)

# 7 Group by language, calculate mean stars, find max
language_avg_stars = repos.groupby('language')['stargazers_count'].mean().idxmax()
print(language_avg_stars)

#  8 Calculate leader strength and get top 5
users['leader_strength'] = users['followers'] / (1 + users['following'])
top_5_leaders = users.sort_values(by='leader_strength', ascending=False)['login'].head(5).tolist()
print(','.join(top_5_leaders))

#  9 Calculate correlation
correlation = users[['followers', 'public_repos']].corr().iloc[0, 1]
print(f"{correlation:.3f}")

from sklearn.linear_model import LinearRegression

# 10 Linear regression of followers on repos
X = users[['public_repos']]
y = users['followers']
model = LinearRegression().fit(X, y)
slope = model.coef_[0]
print(f"{slope:.3f}")

# 11 What is the correlation between a repo having projects enabled and having wiki enabled?
# Calculate correlation
correlation_projects_wiki = repos[['has_projects', 'has_wiki']].corr().iloc[0, 1]
print(f"{correlation_projects_wiki:.3f}")

# 12 Do hireable users follow more people than those who are not hireable?

# Calculate the average following for hireable users
avg_following_hireable = users[users['hireable'] == True]['following'].mean()

# Calculate the average following for non-hireable users
avg_following_non_hireable = users[users['hireable'] == False]['following'].mean()

# Calculate the difference
difference = avg_following_hireable - avg_following_non_hireable

print(f"Difference in average following: {difference}")

# 13 What's the correlation of the length of their bio (in Unicode words, split by whitespace) with followers?
from sklearn.linear_model import LinearRegression

# Filter users with non-null bios
users_with_bio = users[users['bio'].notna()].copy()

# Calculate bio length in terms of word count
users_with_bio.loc[:, 'bio_length'] = users_with_bio['bio'].apply(lambda x: len(x.split()))

# Calculate the correlation between bio length and followers
bio_length_followers_correlation = users_with_bio['bio_length'].corr(users_with_bio['followers'])
bio_length_followers_correlation = round(bio_length_followers_correlation, 3)

bio_length_followers_correlation

# 14 Convert to day of the week and filter weekends
repos['created_at'] = pd.to_datetime(repos['created_at'])
repos['weekday'] = repos['created_at'].dt.weekday
weekend_repos = repos[repos['weekday'] >= 5]

# Assuming 'login' column contains the owner's login
# Replace 'login' with the actual column name if it's different
top_weekend_users = weekend_repos['login'].value_counts().head(5).index.tolist()
print(','.join(top_weekend_users))

# 15 Calculate fractions with email for hireable and non-hireable
hireable_email_fraction = users[users['hireable'] == True]['email'].notna().mean()
non_hireable_email_fraction = users[users['hireable'] == False]['email'].notna().mean()
difference_email = hireable_email_fraction - non_hireable_email_fraction
print(f"{difference_email:.3f}")

# 16 Extract last word as surname and find the most common
users['surname'] = users['name'].dropna().apply(lambda x: x.split()[-1])
most_common_surname = users['surname'].value_counts()
most_common = most_common_surname[most_common_surname == most_common_surname.max()].index.tolist()
print(','.join(sorted(most_common)))
