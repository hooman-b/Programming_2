# Using our STEM_EDX_Pipeline logging code
import logging

class log():
    """
    Create log file which will show information about how 
    long processes took and possible errors that could happen
    """
    def __init__(self, directory, file_name):
        logging.basicConfig(filename=f"{directory}/{file_name}.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def write_to_logger(self, text):
        """
        Write info to log file
        """
        self.logger.info(text)

    def error_to_logger(self, text):
        """
        Write error to log file
        """
        self.logger.error(text)