from renamr.providers.provider import Provider
from renamr.utils.cache import Cache


class OMDb(Provider):
    '''
    Class for getting info from OMDb using the API.
    '''

    OMDB_KEY = 'e73feaf'

    @classmethod
    def get_result(
        cls,
        query: str,
        search_type: str,
        year: str | None = None
    ) -> dict | None:
        '''
        Get search results from Open Movie Database (OMDb)
        based on the provided query and search type.

        NOTE: OMDb TV results provide very basic episode info. If more info needed,
                a request is required for every episode...

        Args:
            query (str): The search query to look for in OMDb.
            search_type (str): 
                The type of search to perform. Can be 'movie' or 'series'.
            year (str | None): 
                The year to filter the search results. Default is None.

        Returns:
            list[dict] | None: 
                A list of dictionaries containing search results
                from OMDb. If no results are found, None is returned.

        Examples:
            >>> get_results(cls, query='Sintel', search_type='movie')
            # Returns {'id': '45745', 'title': 'Sintel', 'genre': 'Animation'}

            >>> get_results(cls, query='New Show', search_type='series', year='2010')
            # Returns {'title': 'New Show', 'genre': 'Drama', 'year': '2010'}
        '''

        url = f'https://www.omdbapi.com/?type={search_type}&t={query}&apikey={cls.OMDB_KEY}'
        if year:
            url += f'&year={year}'
        return cls.request_json(url=url)

    @classmethod
    def get_series_info(
        cls,
        result_info: dict
    ) -> dict:
        '''
        Get Series info from Open Movie Database (OMDb)
        based on the provided Series ID.

        Args: Series_id (str): ID of Series on OMDb.

        Returns:
            dict: A dictionary containing Series info from OMDb.
        '''

        series_info: dict[str] = {
            'title': result_info.get('Title', ''),
            'id': result_info.get('imdbID', ''),
            'year': result_info.get('Released', '').split(' ')[2],
            'month': result_info.get('Released', '').split(' ')[1],
            'day': result_info.get('Released', '').split(' ')[0],
            'date': result_info.get('Released', ''),
            'genre': result_info.get('Genre', '').split(',')[0],
            'language': result_info.get('Language', '').split(',')[0],
            'origin_country': result_info.get('Country', '').split(',')[0],
            'rating_votes': result_info.get('imdbVotes', ''),
            'rating': result_info.get('imdbRating', ''),
            # 'type': result_info.get('type', ''),
            # 'total_episodes': result_info.get('number_of_episodes', ''),
            'total_seasons': result_info.get('totalSeasons', ''),
        }

        return series_info

    @classmethod
    def get_season_info(
        cls,
        query: str,
        season: str
    ) -> dict:
        '''
        Get Season info from Open Movie Database (OMDb)
        based on the provided Season ID.

        Args: season_info (dict): Dictionary of season info from OMDb.

        Returns:
            dict: A dictionary containing Season info from OMDb reorganized.
        '''

        season_info: dict = cls.request_json(
            url=f'https://www.omdbapi.com/?t={query}&season={season}&type=series&apikey={cls.OMDB_KEY}',
        )['Episodes']
        return {
            'season_num': season,
            'season_num_pad': season.zfill(2),
            'season_premiere_year': season_info[0].get('Released', '').split('-')[0],
            'season_premiere_month': season_info[0].get('Released', '').split('-')[1],
            'season_premiere_day': season_info[0].get('Released', '').split('-')[2],
            'season_premiere_date': season_info[0].get('Released', ''),
            'season_episode_count': season_info.__len__().__str__(),
            'season_episodes': {
                episode['Episode']: episode
                for episode in season_info
            }
        }

    @classmethod
    def get_episode_info(
        cls,
        episodes: dict,
    ) -> dict:
        '''
        Get Episode info from Open Movie Database (OMDb)
        based on the provided Season ID.

        Args:
            series_id (str): ID for Series on OMDb.
            season (str): Season to get episode info for.

        Returns:
            dict: A dictionary containing Episode info from OMDb reorganized.
        '''

        # Get list of episodes from OMDb
        episodes_dict: dict = dict()
        for num, episode in episodes.items():
            # Extract episode info from dict returned from $episode_list
            episodes_dict[episode['Episode']] = {
                'episode_num': episode.get('Episode', ''),
                'episode_num_pad': episode.get('Episode', '').zfill(2),
                'episode_title': episode.get('Title', ''),
                'episode_id': episode.get('imdbID', ''),
                'episode_score': episode.get('imdbRating', ''),
                'episode_air_year': episode.get('Released', '').split('-')[0],
                'episode_air_month': episode.get('Released', '').split('-')[1],
                'episode_air_day': episode.get('Released', '').split('-')[2],
            }

        return episodes_dict

    @classmethod
    @Cache
    def movie(
        cls,
        query: str,
        year: str | None = None
    ) -> dict | None:
        '''
        Get movie info from OMDb using API. Return as dictionary

        Args:
            query (str): Title of movie to be searched

        Returns:
            dict | None: Dictionary with Movie info from OMDb.
        '''

        search_result: list = cls.get_result(  # Get movie info from OMDb
            query=query,
            search_type='movie',
            year=year
        )
        if search_result.get('Title'):
            # Return (dict): Movie info from first returned search result
            movie_info: dict[str] = {
                'title': search_result.get('Title', ''),
                'id': search_result.get('imdbID', ''),
                'year': search_result.get('Released', '').split(' ')[2],
                'month': search_result.get('Released', '').split(' ')[1],
                'day': search_result.get('Released', '').split(' ')[0],
                'release_date': search_result.get('Released', ''),
                'genre': search_result.get('Genre', '').split(',')[0],
                'movie_language': search_result.get('Language', '').split(',')[0],
                'production_country': search_result.get('Country', '').split(',')[0],
                'rating_votes': search_result.get('imdbVotes', ''),
                'rating': search_result.get('imdbRating', ''),
                'overview': search_result.get('Plot', ''),
                'runtime': search_result.get('Runtime', '').split(' ')[0],
                'revenue': search_result.get('BoxOffice', ''),
            }
            return movie_info

    @classmethod
    @Cache
    def tv(
        cls,
        query: str,
        seasons: set[str] | None = None,
        year: str | None = None
    ) -> dict | None:
        '''
        Loops through items in Current Name column looking for proper name to search.
        Once found, search and get $series_info (dict) from results and break loop.
        Loop Current Name again and set New Names.

        NOTE: OMDb TV results provide very basic episode info. If more info needed,
                a request is required for every episode...

        Args:
            query (str): Extracted title of file to be searched

        Returns:
            dict | None:
                Dictionary containing Series, Season, and Episode info
        '''

        # Get search results for series
        search_results: dict = cls.get_result(
            query=query,
            search_type='series',
            year=year
        )
        if search_results:
            # Get series information
            series_info: dict[str] = cls.get_series_info(
                result_info=search_results
            )
            # Append episode information to $series_info
            seasons_info: dict = dict()
            episodes_info: dict = dict()
            for season_num in seasons:
                # Get season information
                seasons_info[season_num]: dict = cls.get_season_info(
                    query=query,
                    season=season_num
                )
                # Get basic episode information for each season
                episodes_info[season_num] = cls.get_episode_info(
                    episodes=seasons_info[season_num]['season_episodes']
                )

            # Return dict containing series, season, and episode dicts combined
            return {
                **series_info,
                'season_info': seasons_info,
                'episode_info': episodes_info
            }
        return dict()
