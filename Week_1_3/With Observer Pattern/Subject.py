"""
 I'm not sure I understand what these two classes do...
 (**I made two layer observers pattern. The reason is that it gives 
 me the possibility to add other classes to each layer without 
 interfering with each other. for example I can add other plot maker classes,
 or other data reciever, and each of them can be classified in its specific layer
 In this specific question, this structure may seem unnecessary, but this structure
 can be use in more complicated programs. This was the reason that I tried to use 
 this structure here.**)
"""

class Subject():
    """
    Explanation: A base class representing the subject of an observer pattern.
                 Keeps track of observers and notifies them of updates.
    """
    def __init__(self):
        """
        Explanation: Initializes a Subject instance with an empty list of observers.
        """
        self.observer_list = []

    def add_observer(self, observer):
        """
        Explanation: Adds an observer to the list of observers.

        
        Input: 1. observer: An observer object to be added.
        """
        if observer not in self.observer_list:
            self.observer_list.append(observer)

    def remove_observer(self, observer):
        """
        Explanation: Removes an observer from the list of observers.

       
        Input: 1. observer: An observer object to be removed.
        """
        if observer in self.observer_list:
            self.observer_list.remove(observer)

    def notify_observers(self, *args, **kwargs):
        """
        Explanation: Notifies all registered observers with given arguments and keyword arguments.

        
        Input: 1.  *args: Any positional arguments to be passed to observers.
               2. **kwargs: Any keyword arguments to be passed to observers.
        """
        for obsever in self.observer_list:
            obsever.update(*args, **kwargs) 

class FirstLayerObserver(Subject):
    """
    A base class for first layer observers in an observer pattern.
    Inherits from Subject.
    """
    def __init__(self):
        Subject.__init__(self)

    def update(self, *args, **kwargs):
        """
        Input: 1.  *args: Any positional arguments to be passed to observers.
               2. **kwargs: Any keyword arguments to be passed to observers.
        """
        pass

class SecondLayerObserver(FirstLayerObserver):
    """
    A base class for second layer observers in an observer pattern.
    Inherits from FirstLayerObserver.
    """
    def __init__(self):
        FirstLayerObserver.__init__(self)

    def update(self, *args, **kwargs):
        """
        Input: 1.  *args: Any positional arguments to be passed to observers.
               2. **kwargs: Any keyword arguments to be passed to observers.
        """
        pass