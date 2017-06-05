# -*- coding: utf-8 -*-

#####       Extract data from TMDB API        #####
# The code downloads the top 1000 movies of year 2011-2016 
# TMDB metadata is stored in a csv file

### import libraries
import numpy as np
import scipy as sp
import pandas as pd
import requests
import time
import json
import csv


### Download top 1000 movies of each year from 2011-2016 in US

# my TMDB API key
API_KEY = ''

# base url to download popular, non-adult movies produced in US
url_1 = 'https://api.themoviedb.org/3/discover/movie?api_key='
url_2 = '&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page='
url_3 = '&primary_release_year='
url_4 = '&with_original_language=en'


# download movies from 2011-2016
release_year_range = range(2011,2017)

# download top 1000 movies from each year
# need 50 pages (20 movies per page)
n_pages_per_year = 50


# Create empty list to store the movie information
movies_list = [None] * n_pages_per_year * len(release_year_range)

# Index to the list
ind = 0

# download the movies
for release_year in release_year_range:
    print (release_year)
    
    for page_n in range(1, n_pages_per_year + 1):
        # download the page
        url = url_1 + API_KEY + url_2 + str(page_n)+ url_3 + str(release_year) + url_4
        response_page = requests.get(url)
        # add to the list
        movies_list[ind] = response_page.json()
        ind = ind + 1
        # pause for 0.3 sec
        time.sleep(0.3)
        

        
### save the results to a csv file

file_name = 'data/top1000_movies_2011_2016_tmdb.csv'

with open(file_name, "w") as file:
    csv_file = csv.writer(file)  
    # Add column names
    csv_file.writerow(['poster_path', 'title', 'release_date', 'overview', 
                       'popularity', 'original_title', 'backdrop_path',
                       'vote_count', 'video', 'adult', 'vote_average', 
                       'original_language', 'id', 'genre_ids'])
    
    # save the information
    for i in range(len(movies_list)):
        for item in movies_list[i]['results']:
            csv_file.writerow([item['poster_path'], item['title'].encode('utf8', 'ignore'), 
                               item['release_date'], item['overview'].encode("utf8", "ignore"), 
                               item['popularity'], item['original_title'].encode("utf8", 'ignore'), item['backdrop_path'], 
                               item['vote_count'], item['video'], item['adult'], 
                               item['vote_average'], item['original_language'], 
                               item['id'], item['genre_ids']])
    

    
### Download the genre list from TMDB

url = "https://api.themoviedb.org/3/genre/movie/list?api_key=" + API_KEY + "&language=en-US"

payload = "{}"
response = requests.request("GET", url, data=payload)

# reformat the result
movie_genres = response.json()
movie_genres = movie_genres["genres"]

# now the genres are in a dictionary
for i in range(len(movie_genres)):
    print "id: ", movie_genres[i]["id"], "; Genre name: ", movie_genres[i]["name"]
    
# Export genre list 
with open("data/genre_list.csv", "wb") as file:
    csv_file = csv.writer(file) 
    
    # Add column names
    csv_file.writerow(["id", "GenreName"])
    
    for item in movie_genres:
            csv_file.writerow([item['id'], item['name']])