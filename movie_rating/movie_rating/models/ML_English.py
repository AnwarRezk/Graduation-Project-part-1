# Function that takes in movie title as input and outputs most similar movies
import pandas as pd
from django.conf import settings

def get_recommendations(title):


    # infile1 = open("English_indices", 'rb')
    # Idx_Weights_Updated = pickle.load(infile1)
    # infile1.close()
    idx = settings.IDX_WEIGHTS_UPDATED[title]


    # infile2 = open("English_Cosine_Weights", 'rb')
    # cosine_sim = pickle.load(infile2)
    # infile2.close()

    #infile2 = open("English_movies_df", 'rb')
    #df2 = pickle.load(infile2)
    #infile2.close()

    # movies_csv = "English_movies_df.csv"
    # movies_df = pd.read_csv(movies_csv)

    sim_scores = list(enumerate(settings.COSINE_SIM[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return settings.MOVIES_DF['id'].iloc[movie_indices]


# temp = get_recommendations('Toy Story')
# temp = temp.tolist()
# print(temp)


