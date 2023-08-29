# pylint: disable=E1101
import pandas as pd
from Subject import FirstLayerObserver

class AverageYear(FirstLayerObserver):
    """
    Explanation: A class for calculating and processing average values for each year.
    Inherits from FirstLayerObserver.
    """
    def __init__(self):
        """
        Explanation: Initializes an AverageYear instance.
        """
        FirstLayerObserver.__init__(self)
        self.plot_number = 1

    def update(self, temp_df):
        """
        Input: temp_df (pd.DataFrame): The DataFrame containing the data to be processed.
        Explanation: Updates the observer with new data and triggers notifications to 
        higher-level observers.
        """
        update_list = []

        try:
            update_list.append(temp_df.iloc[:, 0].mean(axis=0))
            avg_series = pd.Series(temp_df.iloc[:, 1:13].mean(axis=None), index=['year'])
            update_list.append(avg_series)
            self.notify_observers(update_list)

        except IndexError:
            update_list.append(temp_df)
            self.notify_observers(update_list)

class AverageMonth(FirstLayerObserver):
    """
    Explanation: A class for calculating and processing average values for each year.
    Inherits from FirstLayerObserver.
    """

    def __init__(self):
        """
        Explanation: Initializes an AverageMonth instance.
        """
        FirstLayerObserver.__init__(self)
        self.plot_number = 1

    def update(self, temp_df):
        """
        Input: temp_df (pd.DataFrame): The DataFrame containing the data to be processed.
        Explanation: Updates the observer with new data and triggers notifications to 
        higher-level observers.
        """
        update_list = []

        try:
            update_list.append(temp_df.iloc[:, 0].mean(axis=0))
            update_list.append(temp_df.iloc[:, 1:].mean(axis=0))
            self.notify_observers(update_list)

        except IndexError:
            update_list.append(temp_df)
            self.notify_observers(update_list)
