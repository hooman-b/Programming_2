# one of the reasons that I gave the name 'MyWatchdog' to this module
# since this is actually what it will be doing. However, to be honest,
# the main reason is that this name is quite fun :)).
# By the way, my reference for these classes are:
# 1. https://medium.com/analytics-vidhya/monitoring-your-file-system-using-watchdog-64f7ad3279f
# 2. https://snyk.io/advisor/python/watchdog/functions/watchdog.observers
# 3. https://pythonhosted.org/watchdog/quickstart.html

import os
import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DataDirectoryWatcher:
    def __init__(self, target_dir, calling_func):
        self.target_dir = target_dir
        self.calling_func = calling_func

    def start_watching(self):
        """
        This function is constantly watching the provided directory to 
        see whether a new .csv file is uploaded there.
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
    def __init__(self, calling_func):
        self.calling_func = calling_func

    def on_created(self, event):
        """
        This function determines the condition of the file that should be watched
        """
        # If the event is related to a directory creation, return
        if event.is_directory:
            return

        # if the directory ends with .csv call the calling_func with the file path
        if event.src_path.endswith(".csv"):
            print(f"New data file added: {event.src_path}")

            # Slice the name of the file and pass it to the main function
            filename = os.path.basename(event.src_path)
            self.calling_func(filename)
