def recommend_fun(id):
    try:
        col_idx = movie_user_mat.T.columns.get_loc(id) #5952
        corr_specific = corr_mat[col_idx]
        df_recommendation = pd.DataFrame(
            {'corr_specific': corr_specific, 'Movies': movie_user_mat.T.columns}).sort_values('corr_specific',
                                                                                              ascending=False).head(10)
        print('Recommendations:')
        print(df_recommendation)

        recommendation_with_titles = pd.merge(df_recommendation, df_inner_movies_links, left_on='Movies',
                                              right_on='movieId', how='inner')
        print('Final Recommendations:')
        print(recommendation_with_titles)
        return recommendation_with_titles
    except:
        print("No movie Recommendations")
        return "No movie Recommendations"