import requests
from bs4 import BeautifulSoup
from collections import defaultdict

username = "parsamrrelax"
url = f'https://letterboxd.com/{username}/following/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all elements with the attribute 'data-username'
followings = [tag['data-username'] for tag in soup.find_all(attrs={"data-username": True})]

# Dictionary to count occurrences of each movie
high_movie_counts = defaultdict(int)

for following in followings:
    five_star_movies_page = requests.get(f"https://letterboxd.com/{following}/films/rated/5/")
    high_soup = BeautifulSoup(five_star_movies_page.text, 'html.parser')
    five_star_movies = [tag['data-film-slug'] for tag in high_soup.find_all(attrs={"data-film-slug": True})]
    
    for movie in five_star_movies:
        high_movie_counts[movie] += 1

low_movie_counts = defaultdict(int)

for following in followings:
    half_star_movies_page = requests.get(f"https://letterboxd.com/{following}/films/rated/.5/")
    low_soup = BeautifulSoup(half_star_movies_page.text, 'html.parser')
    half_star_movies = [tag['data-film-slug'] for tag in low_soup.find_all(attrs={"data-film-slug": True})]

    for movie in half_star_movies:
        low_movie_counts[movie] += 1

# Sort the movies by count in descending order
sorted_movies = sorted(high_movie_counts.items(), key=lambda x: x[1], reverse=True)
low_sorted_movies= sorted(low_movie_counts.items(), key=lambda x: x[1], reverse=True)


# Save the sorted movie counts to a file
with open('movie_counts.txt', 'w') as file:
    for movie, count in sorted_movies[:10]:
        file.write(f'{movie} : {count}\n')
    for movie, count in low_sorted_movies[:10]:
        file.write(f'{movie} : {count}\n')
        print(f'{movie} : {count}')
