import pandas as pd
import math
import openpyxl
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

######################
#what job you want to search for
matchers = ['Application Developer Specialist IT','Application Operation Specialist','Data Analyst']

#insert path   ,   file_name.xlsx
xlsx_file = Path('C:/Users/NiklasWernich/OneDrive - Diadrom Holding AB/Dokument', 'AL_AB_Volvo_Postings.xlsx')
df = pd.read_excel(xlsx_file, index_col=0)
#print(df)
df.columns = df.iloc[0]
#remove first row from DataFrame
df = df[1:]

#view updated DataFrame
df['Job Posting Submit Date'] = pd.to_datetime(df['Job Posting Submit Date'])
df = df.set_index(df['Job Posting Submit Date'])
df = df.sort_index()
#print(df)
df = df.dropna()
# Printing dataframe
#print(df)
#distinct titles only
df_dist = df.drop_duplicates(subset = ['Title'])
#print(df_dist)
#new column with year
df['year'] = df['Job Posting Submit Date'].dt.year
#print(df)

df_freq = df.pivot_table(index = ['Title'], columns=['year'], aggfunc ='size')
df_freq = df_freq.fillna(0)
df_freq

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import fuzz

# Sample data
data = df_freq.index

# Create a pandas Series
series = pd.Series(data)

# Calculate Levenshtein distance similarity
def levenshtein_similarity(a, b):
    return 1 - (fuzz.distance(a, b) / max(len(a), len(b)))

# Convert series to a matrix of TF-IDF features
tfidf_vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
tfidf_matrix = tfidf_vectorizer.fit_transform(series)

# Calculate cosine similarity based on TF-IDF features
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

# Group similar strings
threshold = 0.55  # Adjust this threshold as needed
groups = {}
for i, title in enumerate(series):
    group_idx = None
    for idx, group in groups.items():
        if any(cosine_similarities[i, j] > threshold for j in group):
            group_idx = idx
            break
    if group_idx is None:
        group_idx = i
    groups.setdefault(group_idx, []).append(i)

# Print the groups
for group_idx, group in groups.items():
    group_titles = [series[i] for i in group]
    print(f"Group {group_idx}: {group_titles[0]}")

x = list(map(int, input("Enter multiple values of groups: ").split()))
print("List of groups: ", x)
for wanted in x:
    group_titles = [series[i] for i in groups[wanted]]
    indices = groups[wanted]
    test = df_freq.iloc[indices].sum()
    fig, axes = plt.subplots(nrows=1, ncols=2)
    fig.suptitle(group_titles[0])
    test.plot(ax=axes[0], kind = 'bar')
    df_freq.iloc[indices].plot(ax=axes[1], kind='bar')
    #plt.title(k)
plt.show()
