class Subject():
    def __init__(self):
        self.observer_list = []

    def add_observer(self, observer):
        if observer not in self.observer_list:
            self.observer_list.append(observer)

    def remove_observer(self, observer):
        if observer in self.observer_list:
            self.observer_list.remove(observer)

    def notify_observers(self, *args, **kwargs):
        for obsever in self.observer_list:
            obsever.update(*args, **kwargs) 

class FirstLayerObserver(Subject):
    def __init__(self):
        Subject.__init__(self)

    def update(self, *args, **kwargs):
        # First layer observer's update logic
        pass

class SecondLayerObserver(FirstLayerObserver):
    def __init__(self):
        FirstLayerObserver.__init__(self)

    def update(self, *args, **kwargs):
        # Second layer observer's update logic
        pass