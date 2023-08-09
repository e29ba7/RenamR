import pathlib
import re
import sys
import unittest


sys.path.append(pathlib.Path(__file__).parents[1].joinpath('renamr').__str__())
from utils.metadata import Metadata


class TestMetadata(unittest.TestCase):
    def test_extract_metadata(self):
        '''
        Testing Metadata's _extract_metadata()
        Passes path to _extract_metadata() to have metadata extracted
            and returned as a dict.
        Both movies and tv filenames are passed to Metadata.
        '''        
        movies = [
            'movie title 1999.mp4',
            'movie title 1999 1080p.mp4',
            'movie.title.1999.1080p.x264.mp4',
            'movie.title.1080p.1999.mp4',
            'movie title.mp4',
            'movie title (1).mp4',
            'movie title [1].mp4',
            'movie title 1999 $khjf tgfjui6.mp4',
            'movie title s02e12.mp4',
            'movie title 1x12.mp4',
            '''movie title 1999 ~!@#$%^&*()_+=-|][}{?';"].mp4'''
        ]
        tv = [
            'tv show 2002 1x5.mp4',
            'tv show 2002 1e5.mp4',
            'tv show 2002 1x01.mp4',
            'tv show 2002 1e26.mp4',
            'tv show 2002 0e4.mp4',
            'tv show 2002 s1e05.mp4',
            'tv show 2002 s01e5.mp4',
            'tv show 2002 s01e05.mp4',
            'tv show 2002 s15e05.mp4',
            'tv show 2002 s15e15.mp4',
            'tv show 2002 s15e05.mp4',
            'tv show 2002 s00e34.mp4',
            'tv show s01x15.mp4',
            'tv show 1x5.mp4',
            'tv show 0x4.mp4',
            'tv show s0 e4.mp4',
            'tv show s00 e04.mp4',
            'tv show s01 e05.mp4',
            'tv show s0 e4 - Episode.mp4',
            'tv show s0 e5 - Episode: Another Word.mp4',
            'tv show (Bonus) s01e40'
        ]
        for test in [movies, tv]:
            for file in test:
                self.meta: dict = Metadata(
                        item=pathlib.Path(__file__).parents[1].joinpath(file)
                    ).data
                self.assertRegex(
                    self.meta['title'],
                    r'(?i)movie title( ?)|tv show( ?)'
                )
                if test is tv:
                    self.assertIn(
                        'season_num',
                        self.meta
                    )
                    self.assertIn(
                        'episode_num',
                        self.meta
                    )

if __name__ == '__main__':
    unittest.main()
