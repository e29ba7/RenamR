import json
from typing import Callable


class Cache:
    '''
    Class to manipulate a local cache file
    '''

    def __init__(self, func: Callable):
        self.func = func
        self.cache_file = 'cache.json'

    def __call__(self, *args, **kwargs) -> dict:
        '''
        Load cache from file. If data isn't found in cache, the decorated function will
        run, returning a dictionary. 
        '''

        self._load_cache()  # Load data from cache file
        self.provider: str = self.func.__qualname__.split('.')[0]  # Get provider name
        self.type: str = self.func.__name__  # Get name of wrapped function
        self.key: str = kwargs.get('query')  # Get search query (media title)
        self.year: str = kwargs.get('year', '')  # Get media year, maybe

        if self.year:
            self.key += f' {self.year}'  # Add year to $key
        if self.key not in self.cached_data[self.provider][self.type]:
            # If item isn't already cached
            self.new_data: dict = self.func(*args, **kwargs)  # New data from provider
            self.result: dict = {self.key: self.new_data}  # New dict to be saved
            self._save_cache()  # Needed so new info is saved before being overwritten
        if self.type == 'tv':
            self._update_series_info(*args, **kwargs)
            self.result = {
                self.key: self.cached_data[self.provider][self.type][self.key]
            }
            self._save_cache()  # Save new cache info to cache.json file
        return self.cached_data[self.provider][self.type].get(self.key)

    def _load_cache(self) -> None:
        '''
        Load data from cache file.
        '''

        try:
            with open(self.cache_file, 'r') as f:
                self.cached_data: dict = json.load(f)  # Load cached data
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            self.cached_data: dict = {  # Create new dict
                'TheMovieDB': {
                    'movie': dict(),
                    'tv': dict()
                },
                'OMDb': {
                    'movie': dict(),
                    'tv': dict()
                },
            }

    def _save_cache(self) -> None:
        '''
        Write cache file to disk.
        '''

        self._evict_oldest()
        # Update cache dict with new data
        self.cached_data[self.provider][self.type].update(self.result)
        with open(self.cache_file, 'w') as f:
            json.dump(self.cached_data, f, indent=4)  # Save updated cache to cache.json

    def _evict_oldest(self):
        '''
        Remove the oldest dict when cache length hits limit.
        '''

        if len(self.cached_data[self.provider][self.type].keys()) > 14:  # Limit cache
            self.cached_data[self.provider][self.type].pop(
                next(iter(self.cached_data[self.provider][self.type]))
            )

    def _update_series_info(self, *args, **kwargs) -> None:
        '''
        Add new season and episode data to cached show.
        '''

        for season in kwargs['seasons']:
            # Each season, if not cached already
            if season not in self.cached_data[self.provider][self.type][self.key]['season_info']:
                self.new_data: dict = self.func(*args, **kwargs)  # Get new data
                self.cached_data[self.provider][self.type][self.key]['season_info'].update(
                    **self.new_data['season_info']
                )
                self.cached_data[self.provider][self.type][self.key]['episode_info'].update(
                    **self.new_data['episode_info']
                )
