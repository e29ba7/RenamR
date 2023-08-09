import pathlib
import sys
import unittest


sys.path.append(pathlib.Path(__file__).parents[1].joinpath('renamr').__str__())
from utils.providers import (
    IMDB,
    TheMovieDB
)


class ProvidersTests(unittest.TestCase):
    def test_IMDB_movie(self):
        '''
        Runs get_results from IMDB
        '''
        self.assertIsInstance(IMDB.movie(query='Sintel'), dict)

    def test_IMDB_tv(self):
        ...

    def test_TheMovieDB_movie(self):
        '''
        Runs get_results from TheMovieDB
        '''        
        self.assertIsInstance(TheMovieDB.movie('Sintel'), dict)

    def test_TheMovieDB_tv(self):
        '''
        Runs get_results from TheMovieDB
        and _soup_me from Provider
        '''        
        self.assertIsInstance(TheMovieDB.tv('Treasure Island'), dict)


if __name__ == '__main__':
    unittest.main()
