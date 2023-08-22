import sys
from PyQt5.QtWidgets import QApplication
from data_processing import read_dataframe, prepare_dataframe
from gui import display_group_charts, get_group_input
from text_similarity import threshold_get_groups
from utils import get_double_input

if __name__ == "__main__":
    app = QApplication(sys.argv)

    df = read_dataframe()
    df_freq = prepare_dataframe(df)
    th = get_double_input()
    
    groups, series = threshold_get_groups(df_freq, th)
    
    x = get_group_input()
    display_group_charts(x, groups, series, df_freq)
    app.quit()
