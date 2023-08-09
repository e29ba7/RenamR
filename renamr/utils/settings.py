import configparser


class Settings:
    '''
    A class for managing application settings using a configuration file.

    Attributes:
        CONFIG_FILE_PATH (str): The path to the configuration file.
        movie_template (str):
            User provided string for movies to use as renaming template
        tv_template (str):
            User provided string for TV shows to use as a renaming template

    Methods:
        __new__(cls): Creates a singleton instance of the Settings class.

        _load_settings():
            Loads all settings from the configuration file into class attributes.

        load_setting(setting: str) -> str or None:
            Loads the value of the specified setting from the configuration file.

        save_setting(setting: str, value: str) -> None:
            Saves a setting with the specified key and value to the configuration file.
    '''

    CONFIG_FILE_PATH = 'config.ini'
    DEFAULT: dict = {
        'movie_template': '%title - (%y) - [%id]',
        'tv_template': '%title - %sx%ep - %et'
    }
    movie_template: str
    tv_template: str
    _instance = None
    config = configparser.ConfigParser()

    def __new__(cls):
        '''
        Creates a singleton instance of the class.

        Returns:
            Settings: The singleton instance of the Settings class.
        '''

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = configparser.RawConfigParser()
            cls._load_settings()
        return cls._instance

    @classmethod
    def _load_settings(cls) -> None:
        '''
        Loads all settings from the configuration file into class attributes.
        '''

        cls._instance.config.read(cls.CONFIG_FILE_PATH)
        cls.movie_template = cls.load_setting('movie_template')
        cls.tv_template = cls.load_setting('tv_template')

    @classmethod
    def load_setting(cls, setting: str) -> str | None:
        '''
        Loads the value of the specified setting from the configuration file.
        If the config file is unavailable, a default value is loaded instead.

        Args:
            setting (str): The key of the setting to be loaded.

        Returns:
            str or None:
                The value of the setting or None if the setting does not exist.
        '''

        try:
            return cls._instance.config['Settings'][setting]
        except KeyError:
            # User-set setting not found, retrieve default if possible
            return cls.DEFAULT.get(setting, '')

    @classmethod
    def save_setting(cls, setting: str, value: str = '') -> None:
        '''
        Saves a setting with the specified key and value to the configuration file.

        Args:
            setting (str): The key of the setting to be saved.
            value (str): The value to be associated with the setting key.
        '''

        if not cls._instance.config.has_section('Settings'):
            # Add missing 'Settings' file section
            cls._instance.config.add_section('Settings')
        # Set key and value to be saved
        cls._instance.config['Settings'][setting] = value

        # Save settings to `config.ini`
        with open(cls.CONFIG_FILE_PATH, 'w') as config_file:
            cls._instance.config.write(config_file)
        # Load saved settings for use during current application run.
        cls._load_settings()
