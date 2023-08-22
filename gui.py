from PyQt5.QtWidgets import QDialog, QTableView, QVBoxLayout, QDialogButtonBox, QHeaderView
from PyQt5.QtCore import Qt, QAbstractTableModel
import matplotlib.pyplot as plt
import pandas as pd

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

def get_group_input():
    x = list(map(int, input("Enter multiple values of groups: ").split()))
    print("List of groups: ", x)
    return x

def display_group_charts(selected_groups, groups, series, df_freq):
    for wanted in selected_groups:
        group_titles = [series[i] for i in groups[wanted]]
        indices = groups[wanted]
        test = df_freq.iloc[indices].sum()
        
        # Create a figure and axes
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))  # Adjust figsize as needed
        
        # Set the title for the entire figure
        fig.suptitle(f"Group: {group_titles[0]}", fontsize=16, y=1.02)
        
        # First subplot (left side)
        ax1 = axes[0]
        test.plot(ax=ax1, kind='bar', color='steelblue')  # You can choose a different color
        ax1.set_title("Total Frequency", fontsize=14)
        ax1.set_xlabel("Categories", fontsize=12)
        ax1.set_ylabel("Frequency", fontsize=12)
        ax1.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility
        
        # Second subplot (right side)
        ax2 = axes[1]
        df_freq.iloc[indices].plot(ax=ax2, kind='bar')  # You can choose a different color
        ax2.set_title("Group Frequency", fontsize=14)
        ax2.set_xlabel("Categories", fontsize=12)
        ax2.set_ylabel("Frequency", fontsize=12)
        ax2.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility
        
        # Adjust spacing between subplots
        plt.tight_layout()
        
        # Show the plots
        plt.show()

def display_word_frequencies(df):
    words = ["embedded", "GIT", "Python", "REST", "C++", "Java", "Azure", "C/", "C ", "C.", "Linux", "SQL", "Matlab", "Jenkins", "Jira", "Simulink", "Kubernetes", "AWS", "AUTOSAR", "javascript", ".net", "CI", "Android", "Openshift", "Iso26262", "Angular", "C#", "Spring", "React", "Cybersecurity", "Kotlin", "Power BI", "Node.js", "YOCTO", "Hibernate", "CAN", "LIN", "Ethernet"]

    description_list = df["Description"].values.tolist()

    word_counts = {word: sum(str(description).count(word) for description in description_list) for word in words}

    # for word, count in word_counts.items():
    #     print(f"{word}: {count}")

    words = list(word_counts.keys())
    counts = list(word_counts.values())

    # Create a bar plot
    plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
    plt.bar(words, counts, color='blue')
    plt.xlabel('Words')
    plt.ylabel('Counts')
    plt.title('Word Counts in Description List')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability

    plt.tight_layout()  # Adjust layout for better appearance
    plt.show()
