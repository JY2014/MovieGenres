#####     Download posters from TMDB     #####
# read urls from the movie metadata
# save the posters for deep learning


import numpy as np
import pandas as pd
import requests
import urllib
import time
import matplotlib
import matplotlib.pyplot as plt


# read the movie data for the poster path
data = pd.read_csv("data/top1000_movies_2011_2016_tmdb_imdb.csv")

# poster path base url (poster width = 92)
base_url = "http://image.tmdb.org/t/p/w92/"

# download posters for each movie 
for i in range(data.shape[0]):
    
    if i % 500 == 0:
        print i

    # add the poster path to url
    try:
        url = base_url + data["poster_path"][i]
    except:
        url = base_url
     
    # name the poster by movie id
    # need to manually create the poster folder 
    filename = "data/posters/" + str(int(data["id"][i])) + ".jpg"
    
    # download the image
    image = urllib.URLopener()

    try:
        image.retrieve(url, filename)
    except:
        print ("No poster")
        
    time.sleep(0.5)
    