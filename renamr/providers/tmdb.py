from renamr.providers.provider import Provider
from renamr.utils.cache import Cache
from renamr.utils.utils import timer


class TheMovieDB(Provider):
    '''
    Class for getting info from TheMovieDB using the API.
    '''

    TMDB_HEADER = {
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjZThkNzgzOTcwMzFmZDA1MmZkYzk4NTVkMzNmOTk2MCIsInN1YiI6IjY0ODA2YTZjYmYzMWYyMDEzYWRjNWFmMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.KiigGrJRJTzMBdCg_jjWcwGy-CHnxfcnrp_UWVAvP-g'
    }

    @classmethod
    @timer
    def get_results(
        cls,
        query: str,
        search_type: str,
        year: str | None = None
    ) -> list | None:
        '''
        Get search results from The Movie Database (TMDB)
        based on the provided query and search type.
        Year will be appended to url if one is provided.

        Args:
            query (str): The search query to look for in TMDB.
            search_type (str): 
                The type of search to perform. Can be 'movie' or 'tv'.
            year (str | None): 
                The year to filter the search results. Default is None.

        Returns:
            list[dict] | None: 
                A list of dictionaries containing search results
                from TMDB. If no results are found, None is returned.

        Examples:
            >>> get_results(cls, query='Sintel', search_type='movie')
            # Returns {'id': '45745', 'title': 'Sintel', 'genre': 'Animation'}

            >>> get_results(cls, query='New Show', search_type='tv', year='2010')
            # Returns {'id': 123, 'name': 'New Show', 'genre': 'Drama', 'year': '2010'}
        '''

        url = f'https://api.themoviedb.org/3/search/{search_type}?query={query}'
        if year:
            url += f'&year={year}'
        results = cls.request_json(url=url, header=cls.TMDB_HEADER)
        return results.get('results', None)

    @classmethod
    def get_movie_info(cls, movie_id: str) -> dict:
        '''
        Get movie info from The Movie Database (TMDB)
        based on the provided Movie ID.

        Args: movie_id (str): ID of movie on TMDB.

        Returns:
            dict: A dictionary containing movie info from TMDB.
        '''

        result = cls.request_json(
            url=f'https://api.themoviedb.org/3/movie/{movie_id}',
            header=cls.TMDB_HEADER
        )
        movie_info: dict[str] = {
            'title': result.get('title', ''),
            'original_title': result.get('original_title', ''),
            'id': result.get('id', '').__str__(),
            'year': result.get('release_date', '').split('-')[0],
            'month': result.get('release_date', '').split('-')[1],
            'day': result.get('release_date', '').split('-')[2],
            'release_date': result.get('release_date', ''),
            'genre': result.get('genres', '')[0]['name'],
            'movie_language': result.get('original_language', ''),
            'production_company': 
                # Seems most TMDB movies have the more involved prod. company last
                pc[-1]['name']
                    if (pc:=result.get('production_companies'))
                    else [{'name': ''}],
            'production_country': 
                pc[0]['name']
                    if (pc:=result.get('production_countries'))
                    else [{'name': ''}],
            'rating_votes': result.get('vote_count', '').__str__(),
            'rating': result.get('vote_average', '').__str__(),
            'status': result.get('status', ''),
            'tagline': result.get('tagline', ''),
            'overview': result.get('overview', ''),
            'runtime': result.get('runtime', '').__str__(),
            'budget': result.get('budget', '').__str__(),
            'revenue': result.get('revenue', '').__str__(),
            'collection': result.get('belongs_to_collection', '')
        }
        return movie_info

    @classmethod
    def get_series_info(
        cls,
        series_id: str
    ) -> dict:
        '''
        Get Series info from The Movie Database (TMDB)
        based on the provided Series ID.

        Args: Series_id (str): ID of Series on TMDB.

        Returns:
            dict: A dictionary containing Series info from TMDB.
        '''

        series_results = cls.request_json(
            url=f'https://api.themoviedb.org/3/tv/{series_id}',
            header=cls.TMDB_HEADER
        )
        series_info: dict[str] = {
            'title': series_results.get('name', ''),
            'original_title': series_results.get('original_name', ''),
            'id': series_results.get('id', '').__str__(),
            'year': series_results.get('first_air_date', '').split('-')[0],
            'month': series_results.get('first_air_date', '').split('-')[1],
            'day': series_results.get('first_air_date', '').split('-')[2],
            'date': series_results.get('first_air_date', ''),
            'genre': series_results.get('genres', '')[0]['name'],
            'last_air_year': series_results.get('last_air_date', '').split('-')[0],
            'last_air_month': series_results.get('last_air_date', '').split('-')[1],
            'last_air_day': series_results.get('last_air_date', '').split('-')[2],
            'last_air_date': series_results.get('last_air_date', ''),
            'language': series_results.get('languages', '')[0],
            'network': series_results.get('networks', '')[0]['name'],
            'origin_country': series_results.get('origin_country', '')[0],
            'original_language': series_results.get('original_language', ''),
            'rating_votes': series_results.get('vote_count', '').__str__(),
            'rating': series_results.get('vote_average', '').__str__(),
            'seasons': {
                v.get('season_number').__str__(): v
                for v in series_results.get('seasons')
            },
            'status': series_results.get('status', ''),
            'tagline': series_results.get('tagline', ''),
            'type': series_results.get('type', ''),
            'total_episodes': series_results.get('number_of_episodes', '').__str__(),
            'total_seasons': series_results.get('number_of_seasons', '').__str__(),
        }

        return series_info

    @classmethod
    def get_season_info(
        cls,
        season_info: dict
    ) -> dict:
        '''
        Get Season info from The Movie Database (TMDB)
        based on the provided Season ID.

        Args: season_info (dict): Dictionary of season info from TMDB.

        Returns:
            dict: A dictionary containing Season info from TMDB reorganized.
        '''

        return {
            'season_num': season_info.get('season_number', '').__str__(),
            'season_num_pad': season_info.get('season_number', '').__str__().zfill(2),
            'season_title': season_info.get('name', ''),
            'season_overview': season_info.get('overview', ''),
            'season_premiere_year': season_info.get('air_date', '').split('-')[0],
            'season_premiere_month': season_info.get('air_date', '').split('-')[1],
            'season_premiere_day': season_info.get('air_date', '').split('-')[2],
            'season_premiere_date': season_info.get('air_date', ''),
            'season_episode_count': season_info.get('episode_count', '').__str__(),
            'season_rating': season_info.get('vote_average', '').__str__()
        }

    @classmethod
    def get_episode_info(
        cls,
        series_id: str,
        season: str
    ) -> dict:
        '''
        Get Episode info from The Movie Database (TMDB)
        based on the provided Season ID.

        Args:
            series_id (str): ID for Series on TMDB.
            season (str): Season to get episode info for.

        Returns:
            dict: A dictionary containing Episode info from TMDB reorganized.
        '''

        # Get list of episodes from TMDB
        episode_list: list[dict] = cls.request_json(
            url=f'''https://api.themoviedb.org/3/tv/''' \
                f'''{series_id}''' \
                f'''/season/{season}''',
            header=cls.TMDB_HEADER
        )['episodes']
        # Extract episode info from dict returned from $episode_list
        episodes: dict[dict] = {
            episode['episode_number'].__str__(): {
                'season_num': episode.get('season_number', '').__str__(),
                'episode_num': episode.get('episode_number', '').__str__(),
                'episode_num_pad': episode.get('episode_number', '').__str__().zfill(2),
                'episode_title': episode.get('name', ''),
                'episode_id': episode.get('id', '').__str__(),
                'episode_runtime': episode.get('runtime', '').__str__(),
                'episode_score': episode.get('vote_average', '').__str__(),
                'episode_score_votes': episode.get('vote_count', '').__str__(),
                'episode_summary': episode.get('overview', ''),
                'episode_air_year': episode.get('air_date', '').split('-')[0],
                'episode_air_month': episode.get('air_date', '').split('-')[1],
                'episode_air_day': episode.get('air_date', '').split('-')[2],
            }
            for i in range(len(episode_list))
            if (episode := episode_list[i])['episode_number'] > 0
        }

        return episodes

    @classmethod
    @Cache
    def movie(
        cls,
        query: str,
        year: str | None = None
    ) -> dict | None:
        '''
        Get movie info from TheMovieDB using API. Return as dictionary

        Args:
            query (str): Title of movie to be searched

        Returns:
            dict | None: Dictionary containing Movie information from TMDB.
        '''

        search_results: list = cls.get_results(
            query=query,
            search_type='movie',
            year=year
        )
        if search_results:
            # Return (dict): Movie info from first returned search result
            return cls.get_movie_info(movie_id=search_results[0].get('id'))

    @classmethod
    @Cache
    def tv(
        cls,
        query: str,
        seasons: set[str] | None = None,
        year: str | None = None
    ) -> dict | None:
        '''
        Loop through items in `Current Name` column looking for proper name to search.
        If found, get $series_info (dict), $season_info (dict), and $episode_info (dict)
        from results and break loop.
        Loop `Current Name` again and set new names in `New Name` column.

        Args:
            query (str): Title of Series to be searched.

        Returns:
            dict | None: Dictionary containing Movie information from TMDB.
        '''

        # Get search results for series
        search_results: list = cls.get_results(
            query=query,
            search_type='tv',
            year=year
        )
        if search_results:
            # Get series information
            series_info: dict[dict] = cls.get_series_info(
                series_id=search_results[0]['id']
            )
            # Append episode information to $series_info
            seasons_info: dict = dict()
            episodes_info: dict = dict()
            for season_num in seasons:
                seasons_info[season_num]: dict = cls.get_season_info(
                    season_info=series_info['seasons'][season_num]
                )
                episodes_info[season_num] = cls.get_episode_info(
                    series_id=series_info['id'],
                    season=season_num
                )

            return {
                **series_info,
                'season_info': seasons_info,
                'episode_info': episodes_info
            }
        return dict()
