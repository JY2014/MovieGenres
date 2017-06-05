# -*- coding: utf-8 -*-

######     Download IMDB data for a list of movies    #####

import numpy as np
import pandas as pd
import imdb  # need to pip install IMDBPY
from imdb import IMDb
from datetime import datetime
import re



### Function to find a movie id on IMDb using movie title and year
# input: movie title and movie year in strings
# output: matched movie id if found, otherwise return 0
def find_movie_id(movie_name, movie_year):
    # search for the movie    
    ia = IMDb()
    search_result = ia.search_movie(title)
    
    # go through the result and match to the given year
    # use the first movie matched to the year
    for movie in search_result:
        # some movies do not have year information
        # set year to 0 so guaranteed no match
        try:
            year = movie['year']
        except:
            year = 0
        
        # find the movie if the year matched 
        if year == movie_year:
            matched_movie = movie
            break
    
    # find the movie ID
    try: 
        # extract both movieID and title for double checking
        matched_id = ia.get_imdbID(matched_movie)
        matched_title = matched_movie['title']
    except:
        # id = 0 if movie not exist
        matched_id = 0
        matched_title = "NA"
        
    return(matched_id, matched_title)



### Function to find movie information using movie ID
# input: movie id from IMDb
# output: runtime, director and aspect ratio
def extract_movie_info(movie_id):
    # find the movie information
    ia = IMDb()
    movie = ia.get_movie(movie_id)
    
    # extract relevant information 
    # NA if not exist
    try:
        runtime = ",".join(movie.data['runtimes'])
    except:
        runtime = "NA"
        
    try:
        director = movie.data['director'][0]['name']
    except: 
        director = "NA"
        
    try:
        aspect_ratio = movie.data['aspect ratio']
    except:
        aspect_ratio = "NA"
    
    
    return(runtime, director, aspect_ratio)




#### read the TMDB data
movie_data = pd.read_csv("data/top1000_movies_2011_2016_tmdb.csv")



######   find movie ID for the movies   ######

release_years = list() #data do not already have release year
movie_ids = list()
matched_title = list()

for i in range(movie_data.shape[0]):
    if i % 500 == 0:
        print (i)
        
    # extract movie title
    title = movie_data.iloc[i]["title"]
    
    # extract release year
    t = movie_data.iloc[i]["release_date"]
    year = datetime.strptime(t, '%Y-%M-%d').year
    release_years.append(year)
    
    
    # find movie_id
    movie_id, movie_title = find_movie_id(title, year)
    movie_ids.append(movie_id)
    matched_title.append(movie_title)



# add movie year, id and matched title to the dataframe
movie_data['year'] = pd.Series(release_years, index=movie_data.index)
movie_data['imdb_id'] = pd.Series(movie_ids, index=movie_data.index)
movie_data['imdb_title'] = pd.Series(matched_title, index=movie_data.index)




######   find movie information from IMDb   #######

# read the movie id due to deleted rows
movie_ids = movie_data["imdb_id"]

movie_runtimes = list()
movie_directors = list()
movie_ratio = list()

i = 0  # to track the progress

for movie_id in movie_ids:
    if i % 100 == 0:
        print (i)
    i=i+1
        
    # if not empty
    if movie_id != 0:
        runtime, director, aspect_ratio = extract_movie_info(movie_id)
    else: # NA if empty
        runtime = director = aspect_ratio = "NA"
    
    # add to the lists
    movie_runtimes.append(runtime)
    movie_directors.append(director)
    movie_ratio.append(aspect_ratio)
  
  
# add runtime, director and aspect ratio to the dataframe
movie_data['runtime'] = pd.Series(movie_runtimes, index=movie_data.index)
movie_data['director'] = pd.Series(movie_directors, index=movie_data.index)
movie_data['aspect_ratio'] = pd.Series(movie_ratio, index=movie_data.index)
  


### Fix the format of runtime
# some movies have multiple runtimes; save the first runtime

# non-missing runtime
runtime_nomissing_index = (movie_data['runtime'] != 'NA')
runtime_nomissing = movie_data['runtime'][runtime_nomissing_index]

# split by delimiters
# Source: http://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters
runtime_splits = [re.findall(r"[\w']+", runtime_nomissing.iloc[i]) for i in range(len(runtime_nomissing))]

# save the first runtime for each movie
runtime_value = np.zeros((len(runtime_nomissing)))

for j in range(len(runtime_splits)):
    list_num = [int(s) for s in runtime_splits[j] if s.isdigit()]
    runtime_value[j] =list_num[0]

# reassign runtime_value to the correct column
movie_data['runtime'][runtime_nomissing_index] = runtime_value


          
### save the dataframe into csv 
         
# check the columns with non-ascii code
error_columns = []
for i in range(len(movie_data.columns)):
    try:
        movie_data[movie_data.columns[i]].to_csv('test' + str(i) +'.csv')
    except Exception,e: 
        print str(e) + ' error at ' + str(i)
        error_columns.append(i)
 
#'ascii' codec can't encode character u'\xb0' in position 3:
    # ordinal not in range(128) error at 16
#'ascii' codec can't encode character u'\xe4' in position 9: 
    #ordinal not in range(128) error at 18

# encode all text in utf-8
for bad_col in error_columns:
    movie_data[movie_data.columns[bad_col]] = movie_data[movie_data.columns[bad_col]].str.encode('utf-8')


# save to csv
movie_data.to_csv("data/top1000_movies_2011_2016_tmdb_imdb.csv", 
                  index=False)

# pickle the data
movie_data.to_pickle('data/top1000_movies_2011_2016_tmdb_imdb.p')
