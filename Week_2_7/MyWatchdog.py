# one of the reasons that I gave the name 'MyWatchdog' to this module
# since this is actually what it will be doing. However, to be honest,
# the main reason is that this name is quite fun :)).
# By the way, my reference for these classes are:
# 1. https://medium.com/analytics-vidhya/monitoring-your-file-system-using-watchdog-64f7ad3279f
# 2. https://snyk.io/advisor/python/watchdog/functions/watchdog.observers
# 3. https://pythonhosted.org/watchdog/quickstart.html

# The term watchdog already appears in the computers of the Apollo project (I'm not sure whether
# they coined it, but still).
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DataDirectoryWatcher:
    """
    Type: This class is a normal class
    Explanation: The DataDirectoryWatcher class monitors a specified directory for new .csv
                 files and notifies
    a provided function when a new file is detected.
    Attributes: 1. target_dir (str): The directory to watch for new .csv files.
                2. calling_func (callable): The function to be called when a new .csv 
                file is detected.
    """

    def __init__(self, target_dir, calling_func):
        """
        Input: 1. target_dir (str): The directory to watch for new .csv files.
               2. calling_func (callable): The function to be called when a new .csv file is
                                     detected.
        Explanation: Initializes a new instance of DataDirectoryWatcher.
        """
        self.target_dir = target_dir
        self.calling_func = calling_func

    def start_watching(self):
        """
        Explanation: Begins monitoring the target directory for new .csv files. When a new
                     file is detected, he provided calling_func is invoked.
        Exception: (KeyboardInterrupt): If the user presses Ctrl-C while monitoring is active.
        """
        # Set up an observer which monitors directory for .csv files 
        # and notifies the handler defined above
        event_handler = DataFileHandler(self.calling_func)
        observer = Observer()
        observer.schedule(event_handler, path=self.target_dir, recursive=False)

        # Start the file change monitoring loop until the user presses Ctrl-C.
        observer.start()

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class DataFileHandler(FileSystemEventHandler):
    """
    Type: This class is a child class and it inherits from FileSystemEventHandler
    Explanation: The DataFileHandler class is a file system event handler that
                 triggers when new files are created in a watched directory. It 
                 checks if the newly created file is a CSV file and calls a specified
                 function when a CSV file is detected.
    Attributes: 1. calling_func (callable): The function to be called when a new CSV 
                   file is detected.
    """
    def __init__(self, calling_func):
        """
        Input: 1. calling_func (callable): The function to be called when a new CSV
                  file is detected.
        Explanation: Initializes a new instance of DataFileHandler.
        """
        self.calling_func = calling_func

    def on_created(self, event):
        """
        Input: 1. event (FileSystemEvent): The event object representing the file
                                           creation event.
        Explanation: A callback method triggered when a new file is created. It checks if
                     the created file is a CSV file and calls the specified function if the
                     condition is met.
        """
        # If the event is related to a directory creation, return
        if event.is_directory:
            return

        # if the directory ends with .csv call the calling_func with the file path
        if event.src_path.endswith(".csv"):
            print(f"New data file added: {event.src_path}")

            # Slice the name of the file and pass it to the main function
            filename = os.path.basename(event.src_path)
            self.calling_func(event.src_path, filename)
