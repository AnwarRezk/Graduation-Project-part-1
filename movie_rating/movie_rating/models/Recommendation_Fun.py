from django.conf import settings
import pandas as pd

def recommend_fun(id):
    try:
        z = settings.DF_INNER_MOVIES_LINKS.loc[settings.DF_INNER_MOVIES_LINKS['id'] == id]['movieId']  #ex 769.0
        z = str(z)
        z = z.split()
        col_idx = settings.MOVIE_USER_MAT.T.columns.get_loc(int(z[1]))
        corr_specific = settings.CORR_MAT[col_idx]
        df_recommendation = pd.DataFrame(
            {'corr_specific': corr_specific, 'Movies': settings.MOVIE_USER_MAT.T.columns}).sort_values('corr_specific',
                                                                                              ascending=False).head(10)
        # print('Recommendations:')
        # print(df_recommendation)

        recommendation_with_titles = pd.merge(df_recommendation, settings.DF_INNER_MOVIES_LINKS, left_on='Movies',
                                              right_on='movieId', how='inner')
        recommendation_with_titles.drop('movieId', inplace=True, axis=1)
        recommendation_with_titles.drop('Movies', inplace=True, axis=1)
        # print('Final Recommendations:')
        # print(recommendation_with_titles)
        return recommendation_with_titles.to_dict(orient="list")
    except:
        # print("No movie Recommendations")
        return {"id": []}