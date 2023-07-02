# pylint: disable=E1101
import pandas as pd
from Animation import Animation
from Subject import FirstLayerObserver

class AverageYear(FirstLayerObserver):
    def __init__(self):
        FirstLayerObserver.__init__(self)
        self.plot_number = 1

    def update(self, temp_df):
        update_list = []

        try:
            update_list.append(temp_df.iloc[:, 0].mean(axis=0))
            update_list.append(temp_df.iloc[:, 1:13].mean(axis=None))
            self.notify_observers(update_list)

        except IndexError:
            update_list.append(temp_df)
            self.notify_observers(update_list)

class AverageMonth(FirstLayerObserver):
    def __init__(self):
        FirstLayerObserver.__init__(self)
        self.plot_number = 1

    def update(self, temp_df):
        update_list = []

        try:
            update_list.append(temp_df.iloc[:, 0].mean(axis=0))
            update_list.append(temp_df.iloc[:, 1:].mean(axis=0))
            self.notify_observers(update_list)

        except IndexError:
            update_list.append(temp_df)
            self.notify_observers(update_list)
