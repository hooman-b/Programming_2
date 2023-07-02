# pylint: disable=E1101
import pandas as pd
from Animation import Animation
from Subject import Subject

class AverageYear(Subject):
    def __init__(self):
        Subject.__init__(self)
#        self.animation = Animation()
        self.plot_number = 1

    def update(self, temp_df):
        update_list = []

        update_list.append(temp_df.iloc[:, 0].mean(axis=0))
        update_list.append(temp_df.iloc[:, 1:13].mean(axis=None))
        #title = temp_df.columns.values[0]
        print('hi')
        print(update_list)
        self.notify_observers(update_list)

