from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import numpy as np
from utils import get_double_input
from gui import DataFramePopup


def threshold_get_groups(df_freq, th):
    # Sample data
    data = df_freq.index

    # Create a pandas Series
    series = pd.Series(data)

    # Convert series to a matrix of TF-IDF features
    tfidf_vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(series)

    # Calculate cosine similarity based on TF-IDF features
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    groups = {}
    for i, title in enumerate(series):
        group_idx = None
        for idx, group in groups.items():
            if any(cosine_similarities[i, j] > th for j in group):
                group_idx = idx
                break
        if group_idx is None:
            group_idx = i
        groups.setdefault(group_idx, []).append(i)

    # Print the groups
    for group_idx, group in groups.items():
        group_titles = [series[i] for i in group]
        print(f"Group {group_idx}: {group_titles[0]}")

    groups_df = {}

    # Print the groups
    for group_idx, group in groups.items():
        group_titles = [series[i] for i in group]
        groups_df[group_idx] = group_titles
        

    data = groups_df
    # Convert dictionary to DataFrame with padding
    max_length = max(len(v) for v in data.values())
    data_padded = {key: value + [np.nan] * (max_length - len(value)) for key, value in data.items()}

    df = pd.DataFrame(data_padded)

    popup = DataFramePopup(df)
    popup.exec_()

    # Perform cleanup or other actions after the popup is closed
    print("Do you want to change the threshold value? \n ")
    change_threshold = yes_or_no().lower()
    if change_threshold == 'y':
        new_threshold = get_double_input()
        print(f"New threshold value: {new_threshold}")
        return threshold_get_groups(df_freq, new_threshold)
    else:
        new_threshold = th
        print(f"Threshold value remains: {new_threshold}")
        return groups, series

def yes_or_no():
    yon = input("(y/n): ")
    if (yon == 'y' or yon == 'n'):
        return yon
    else :
        return yes_or_no()
