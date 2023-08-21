import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import fuzz
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTableView, QVBoxLayout, QDialogButtonBox, QHeaderView
from PyQt5.QtCore import Qt, QAbstractTableModel



# ... (same code to create the DataFrame) ...

def VCC_or_AB():
    VCC = input("Is it postings for VCC -> y \nIs it postings for Volvo AB -> n: ")
    if (VCC == 'y' or VCC == 'n'):
        if VCC == 'y':
            return 'Job Posting Title'
        else :
            return 'Title'
    else :
        return VCC_or_AB()

def is_double(value):
    return isinstance(value, float)

def get_double_input():
    while True:
        user_input = input("Enter a threshold (between 0 and 1) for likeness of job titles: ")
        try:
            user_input = float(user_input)
            if is_double(user_input) and 0 <= user_input <= 1:
                return user_input
            else:
                print("Input must be a double between 0 and 1.")
        except ValueError:
            print("Invalid input. Please enter a valid double.")

class DataFrameTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.data.columns)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self.data.iat[index.row(), index.column()])
        return None

class DataFramePopup(QDialog):
    def __init__(self, df):
        super().__init__()

        self.setWindowTitle("DataFrame Viewer")

        layout = QVBoxLayout()

        table_view = QTableView()
        model = DataFrameTableModel(df)
        table_view.setModel(model)

        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setDefaultSectionSize(150)  # Adjust the width as needed

        layout.addWidget(table_view)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)

        layout.addWidget(button_box)

        self.setLayout(layout)

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
    change_threshold = input("Do you want to change the threshold value (y/n)? ").lower()
    if change_threshold == 'y':
        new_threshold = get_double_input()
        print(f"New threshold value: {new_threshold}")
        return threshold_get_groups(df_freq, new_threshold)
    else:
        new_threshold = th
        print(f"Threshold value remains: {new_threshold}")
        return groups, series

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ... (same code to create the DataFrame) ...
    title = VCC_or_AB()

    path1 = input('insert path like \nC:/Users/NiklasWernich/OneDrive - Diadrom Holding AB/Dokument/ALL_AB_Volvo_Postings.xlsx \n')

    #insert path   ,   file_name.xlsx
    xlsx_file = Path(path1)
    # 'All_VCC_Postings.xlsx'
    # 'ALL_AB_Volvo_Postings.xlsx'
    df = pd.read_excel(xlsx_file, index_col=0)

    #ALL_AB_Volvo_Postings.xlsx

    #All_VCC_Postings.xlsx
    #######################################

    #print(df)
    df.columns = df.iloc[0]
    #remove first row from DataFrame
    df = df[1:]

    #view updated DataFrame
    df['Job Posting Submit Date'] = pd.to_datetime(df['Job Posting Submit Date'])
    df = df.set_index(df['Job Posting Submit Date'])
    df = df.sort_index()
    #print(df)
    df = df.dropna(how='all')

    #distinct titles only
    df_dist = df.drop_duplicates(subset = [title])
    #print(df_dist)
    #new column with year
    df['year'] = df['Job Posting Submit Date'].dt.year
    #print(df)

    df_freq = df.pivot_table(index = [title], columns=['year'], aggfunc ='size')
    df_freq = df_freq.fillna(0)
    df_freq

    # Group similar strings
    th = get_double_input()
    threshold = 0.55  # Adjust this threshold as needed
    ###
    groups, series = threshold_get_groups(df_freq, th)

    # Rest of your code
    x = list(map(int, input("Enter multiple values of groups: ").split()))
    print("List of groups: ", x)
    for wanted in x:
        group_titles = [series[i] for i in groups[wanted]]
        indices = groups[wanted]
        test = df_freq.iloc[indices].sum()
        fig, axes = plt.subplots(nrows=1, ncols=2)
        fig.suptitle(group_titles[0])
        test.plot(ax=axes[0], kind='bar')
        df_freq.iloc[indices].plot(ax=axes[1], kind='bar')
        #plt.title(k)
    plt.show()

    print('this is the file')

    sys.exit(app.exec_())
