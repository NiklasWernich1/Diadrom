from PyQt5.QtWidgets import QDialog, QTableView, QVBoxLayout, QDialogButtonBox, QHeaderView
from PyQt5.QtCore import Qt, QAbstractTableModel
import matplotlib.pyplot as plt

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
        fig, axes = plt.subplots(nrows=1, ncols=2)
        fig.suptitle(group_titles[0])
        test.plot(ax=axes[0], kind='bar')
        df_freq.iloc[indices].plot(ax=axes[1], kind='bar')
        #plt.title(k)
    plt.show()
