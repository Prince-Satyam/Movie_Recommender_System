# @ Author - Prince Satyam
# Imports
import os.path
import streamlit as st
import pickle
from pathlib import Path
from main import movieRecommender

PAGE_TITLE = "CineMatch"
st.set_page_config(page_title=PAGE_TITLE, layout="wide")

# Set the background image of webpage
backgroundImage = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://c1.wallpaperflare.com/preview/375/915/707/frog-cinema-popcorn-funny.jpg");
background-size: contain;
}
</style>
"""
st.markdown(backgroundImage, unsafe_allow_html=True)

# Creating the instance of class
movieRecommenderObj = movieRecommender()

# Load the data to display on the webpage
currDir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
dataFilePath = currDir / "MoviesList.pkl"
similarDataFilePath = currDir / "Similarity.pkl"
isPickleFilePresent = False
if os.path.exists(dataFilePath) and os.path.exists(similarDataFilePath):
    movies = pickle.load(open(dataFilePath, 'rb'))
    similarDatas = pickle.load(open(similarDataFilePath, 'rb'))
    isPickleFilePresent = True
else:
    movies = movieRecommenderObj.getData()

moviesList = movies['title'].values

# Generate the layout of the page
st.markdown("<h1 style='color: red;'>CineMatch: Intelligent Movie Recommendation Platform</h1>", unsafe_allow_html=True)
# inputData = st.selectbox("Hey there, fellow cinephile! Drop your favorite flick, and we'll roll out the red carpet with a binge-worthy match", moviesList)
inputData = st.selectbox("Hey there, fellow cinephile! Drop your favorite flick, and we'll roll out the red carpet with a binge-worthy match", moviesList)

def suggestMovies(movieName):
    """
        Get the list of suggested movies through index and arrange them in decending order of their distance
    """
    index = movies[movies['title'] == movieName].index[0]

    angularDist = sorted(list(enumerate(similarDatas[index])), reverse=True, key=lambda vectorData:vectorData[1])
    # Print the first five suggestions
    recommendedMoviesList, posterList = [], []
    for dist in angularDist[1:6]:
        movieId = movies.iloc[dist[0]].id
        posterList.append(movieRecommenderObj.getPoster(movieId))
        recommendedMoviesList.append(movies.iloc[dist[0]].title)
    return recommendedMoviesList, posterList

if st.button("Show Recommendations"):
    if isPickleFilePresent:
        movieNames, posterList = suggestMovies(inputData)
    else:
        movieNames, posterList = movieRecommenderObj.getRecommendations(movies, inputData)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"<p style='color: red; font-size: 20px; font-weight: bold;'>{movieNames[0]}</p>", unsafe_allow_html=True)
        st.image(posterList[0])
    with col2:
        st.markdown(f"<p style='color: red; font-size: 20px; font-weight: bold;'>{movieNames[1]}</p>", unsafe_allow_html=True)
        st.image(posterList[1])
    with col3:
        st.markdown(f"<p style='color: red; font-size: 20px; font-weight: bold;'>{movieNames[2]}</p>", unsafe_allow_html=True)
        st.image(posterList[2])
    with col4:
        st.markdown(f"<p style='color: red; font-size: 20px; font-weight: bold;'>{movieNames[3]}</p>", unsafe_allow_html=True)
        st.image(posterList[3])
    with col5:
        st.markdown(f"<p style='color: red; font-size: 20px; font-weight: bold;'>{movieNames[4]}</p>", unsafe_allow_html=True)
        st.image(posterList[4])

