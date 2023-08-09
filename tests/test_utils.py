import pathlib
import sys
import unittest

sys.path.append(pathlib.Path(__file__).parents[1].__str__())
from renamr.utils.utils import (
    Dir,
    clean_title,
    format_new_filename,
    remove_forbidden_chars,
    replace_colon,
)


class UtilitiesTests(unittest.TestCase):
    movie_tv_tests = [
        'media title 2002 1x5',
        'media title 2002 1e5',
        'media title 2002 1x00',
        'media title 2002 1e00',
        'media-title 2002 0e0',
        'media title 2002 0x0',
        'media title 2002 s1e05',
        'media title 2002 s01e5',
        'media-title 2002 s01e05',
        'media title 2002 s15e05',
        'media title 2002 s15e15',
        'media title 2002 s15e00',
        'media title 2002 s00e00',
        'media title s01x15',
        'media-title 1x5',
        'media title 1x0',
        'media title 0x0',
        'media title s0 e0',
        'media title s00 e00',
        'media title s01 e05',
        'media title s0 s5',
        'media-title!꞉ (2013)',
        'media title 1999',
        'media title 1999 1080p',
        'media.title.1999.1080p.x264',
        'media.title.1080p.1999',
        'media title',
        'media title (1)',
        'media-title [1]',
        'media title 1999 $khjf tgfjui6',
        'media title s02e12',
        'media title 1x12',
        """media title 1999 ~!@#$%^&*()_+=-|][}{?';"]"""
    ]

    def test_Directory(self):
        self.assertTrue(Dir.get_file('theme', 'MaterialDark.qss'))

    def test_clean_title_movie(self):
        for test in self.movie_tv_tests:
            self.assertIsInstance(clean_title(test), str)
            self.assertRegex(clean_title(test), r'media title(.?)')

    def test_remove_forbidden_chars(self):
        tests = [
            'Media*Title',
            'Media Title?',
            'Media and a "half" shell',
            '\Media\.\Title',
            '?Me<|dia /T|i>tle??'
        ]
        for test in tests:
            for char in ['/', '\\', '<', '>', '"', '|', '?', '*']:
                self.assertNotIn(char, remove_forbidden_chars(test))

    def test_replace_colon(self):
        tests = [
            'Media Title: The Beginning',
            'Meet Mr. Muppet: A New World',
            'Try this: Back Again'
        ]
        for test in tests:
            self.assertNotIn(":", replace_colon(test))

    def test_movie_filename_format(self):
        self.tests = [
            {
                'title': 'Movie Title',
                'year': '1999',
                'id': '123456'
            },
            {
                'title': 'Movie Title?',
                'year': '1999',
                'id': '123456'
            }
        ]
        for test in self.tests:
            self.assertRegex(
                text=format_new_filename(
                    new_data=test,
                    template='%title - (%y) - [%id]'
                ),
                expected_regex=r'.*\((18|19|20)\d{2}\) - \[\d+\]'
            )

    def test_tv_filename_format(self):
        new = {
            'title': 'TV Show',
            'season_num': '2',
            'episode_num_pad': '45',
            'episode_title': 'Pilot'
        }
        self.assertRegex(
            format_new_filename(
                new_data=new,
                template='%title - %sx%ep - %et'
            ),
            r'(?i).*\dx\d{1,2} -.*'
        )


if __name__ == '__main__':
    unittest.main()
