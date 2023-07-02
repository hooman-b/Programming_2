
class Subject():
    def __init__(self):
        self.observer_list = []

    def add_observer(self, observer):
        if observer not in self.observer_list:
            self.observer_list.append(observer)

    def remove_observer(self, observer):
        if observer in self.observer_list:
            self.observer_list.remove(observer)

    def notify_observers(self, temp_df):
        for obsever in self.observer_list:
            obsever.update(temp_df) 