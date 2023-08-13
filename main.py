# @author - Prince Satyam

# Imports
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import requests


class movieRecommender():
    def __init__(self):
        """
            Initialize the constructor
        """
        self.currDir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
        self.csvFile = r"C:\Python\DataScience\Project\Docs\MoviesData\top10K-TMDB-movies.csv" #self.currDir / "Docs" / "MoviesData" / "top10K-TMDB-movies.csv"

    def getData(self):
        """
            Read the data from dataset
        """
        moviesData = pd.read_csv(self.csvFile)
        # print(moviesData.head())
        # print(moviesData.describe())

        # Remove the unneccessary items from data
        moviesData = moviesData[['id', 'title', 'overview', 'genre']]
        # Creata a new column with comb of 2 and drop the other two
        moviesData['tags'] = moviesData['overview'] + moviesData['genre']
        newData = moviesData.drop(columns=['overview', 'genre'])
        return newData

    def getPoster(self, movieId):
        """
            Get the poster for requested movie Id
        """
        url = "https://api.themoviedb.org/3/movie/{}?api_key=d9997e530aeffabda0adfdffa8e75eaa&language=en-US".format(
            movieId)
        posterData = requests.get(url)
        posterData = posterData.json()
        posterPath = posterData['poster_path']
        fullPosterPath = "https://image.tmdb.org/t/p/w500/" + posterPath
        return fullPosterPath

    def getRecommendations(self, newData, movieName):
        """
            Transform the data into vector array and get the movie and poster list
        """
        recommemdations, posterList = [], []
        # Convert the textual data from dataset into vector format
        dataToBeTransformed = CountVectorizer(max_features=10000, stop_words='english')
        vectorData = dataToBeTransformed.fit_transform(newData['tags'].values.astype('U')).toarray()
        # print(vectorData.shape)

        # Use cosine similarity approach to get the closest movie tagline
        similarDatas = cosine_similarity(vectorData)

        def suggestMovies(movieName):
            """
                Sort the similar movies through cosine similarity and
                return the list of top 5 similar movies with their posters
                through TMDB api
            """
            # Get the list of suggested movies through index and arrange them in decending order of their distance
            index = newData[newData['title'] == movieName].index[0]
            angularDist = sorted(list(enumerate(similarDatas[index])), reverse=True, key=lambda vectorData:vectorData[1])
            # Print the first five suggestions
            recommendedList, posterList = [], []
            for dist in angularDist[1:6]:
                movieId = newData.iloc[dist[0]].id
                posterList.append(self.getPoster(movieId))
                recommendedList.append(newData.iloc[dist[0]].title)
                # print(newData.iloc[dist[0]].title)
            return recommendedList, posterList

        # Return the recommended list
        recommemdations, posterList = suggestMovies(movieName)
        return recommemdations, posterList, similarDatas

    def main(self):
        """
            Main function
        """
        movieName = "Avatar" # Recommend movies similar to movieName
        print("Getting the movies informations from dataset")
        datas = self.getData()
        if not datas.empty:
            recommemdations, posterList, similarDatas = self.getRecommendations(datas, movieName)
            print("You can watch...")
            for movie in recommemdations: print(movie)
        else:
            print("Unable to fetch the movies list from database")
        print("Storing the datas in pickle files...")
        # Save the data in Pickle file
        pickle.dump(datas, open('MoviesList.pkl', 'wb'))
        pickle.dump(similarDatas, open('Similarity.pkl', 'wb'))
        print("Data stored")

recommendObj = movieRecommender()
recommendObj.main()
