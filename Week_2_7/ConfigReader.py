import yaml

class ConfigReader:
    _instance = None

    def __new__(cls):
        """
        This function checks whether an instance of this class has been made before.
        If not it makes an instance of the class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance
    
    def __getitem__(self, key):
        """
        This function allows dictionary-like access to configuration values
        """
        return self.config[key]

    def load_config(self):
        """
        This function loads the configuration file
        """
        with open('config.yaml', 'r',  encoding='utf8') as config_file:
            self.config = yaml.safe_load(config_file)