import re
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem

from renamr.ui.unknownmedia import UnknownMediaWindow
from renamr.utils.settings import Settings
from renamr.utils.utils import (
    clean_title,
    Dir,
    filter_new_title,
    format_new_filename,
    remove_forbidden_chars,
    replace_colon,
)


class Metadata(QTableWidgetItem):
    '''
    Class to extract and hold metadata for files in a table view item.
    This class is then added as an item to the table view.
    $data is a list of dicts.

    Args:
        QTableWidgetItem: Item able to be added to table view

    Returns: Dictionary containing media metadata. See $_extract_metadata
    '''

    settings = Settings()

    def __init__(
            self,
            item: dict | Path,
    ) -> None:
        super().__init__()
        if isinstance(item, Path):  # Pathed file means data sourced from file
            self.data: dict = self._extract_metadata(item)
            self._set_text_and_tooltip(self.data['filename'])
            # Disable item editing by user (Items in first column)
            self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsEditable)
        else:
            # If $item is a dictionary, it's new data from a provider
            self.data: dict = item
            # Determine template type to use for new filename
            self.template = (
                getattr(self.settings, 'movie_template')
                if 'release_date' in self.data.keys()
                else getattr(self.settings, 'tv_template')
            )
            # Get new filename in desired output template
            self.filtered_title: str = format_new_filename(
                new_data=self.data,
                template=self.template
            )
            # self.filtered_title = replace_colon(self.filtered_title)
            self.filtered_title = filter_new_title(text=self.filtered_title)
            # self.filtered_title = remove_forbidden_chars(self.filtered_title)
            self._set_text_and_tooltip(self.filtered_title)

    def _set_text_and_tooltip(self, text: str) -> None:
        '''
        Set current item text and tooltip to provided $text

        Args:
            text (str): String to change displayed item text and tooltip
        '''

        self.setText(text)
        self.setToolTip(text)

    def _extract_metadata(self, pathed_file: Path) -> dict:
        '''
        Extract file metadata from filename and return a dictionary.

        Args:
            pathed_file (Path): Full path to and including file

        Returns:
            dict: {
            filename (str): 'movie.name.1999.480p,
            title (str): 'movie name',
            year (str): '1999',
            directory (path): '/home/user/Desktop/',
            extension (str): '.avi'
        }
        May also contain elements if filename contains series matching regex:
        dict {
            season (str): 1,
            episode (str): 8
        }
        '''

        self.extracted_data: dict = dict()
        self.extracted_data['absolute_path']: str = pathed_file.absolute()
        self.extracted_data['filename']: str = pathed_file.stem
        self.extracted_data['directory']: Path = pathed_file.parent
        self.extracted_data['extension']: str = pathed_file.suffix
        self.extracted_data['title']: str = clean_title(pathed_file.stem)
        if not self.extracted_data['title']:
            # UnknownMediaWindow(
            #     file=self.extracted_data.get('filename'),
            #     title='What is this?',
            #     icon=Dir.get_file('icon', 'VHS.png')
            # )
            # Need to add error for missing title in filename
            print('Title not found in filename.')
        # remove_forbidden_chars(extracted_data['title'])

        # Find resolution in filename
        self.resolution = re.search(
            r'''(?ix)(
                (((14|36|57|72)\d           # Find resolutions such as 576p or 720p
                |1080                       # or find 1080p/i
                |2160)                      # or find 2160p/i
                (p|i))                      # only match above res. if p/i follows
                |4K|2K|FHD|UHD|HD|DVD|SD    # or find these resolutions
            )''',
            pathed_file.stem
        )
        if self.resolution:
            self.extracted_data['resolution']: str = self.resolution.group()
        self.year = re.search(
            r'(18|19|20)\d{2}',
            self.extracted_data['filename']
        )
        # Set year if found in filename or set as ''.
        self.extracted_data['year']: str = self.year.group() if self.year else ''
        # # TV Specific
        try:
            # Find season in common series formats
            self.extracted_data['season_num']: str = re.search(
                r'''(?ix)
                    [1-9]?\d(\ ?)       # Match season number
                    (?=                 # Begin lookahead
                        (e|x|\-)\d      # Look for e, x, or - and digit
                    )
                ''',
                self.extracted_data['filename']
            ).group()
            # Find episode in common series formats
            self.extracted_data['episode_num']: str = re.search(
                r'''(?ix)
                    (?<!\d{2}|s\d)          # Don't match year or season numbers
                    (?<=(e|x|\-|0))         # Lookbehind for e, x, -, or 0
                    ([1-9][0-9]{0,2})       # Match episode numbers
                ''',
                self.extracted_data['filename']
            ).group()
            # breakpoint()
        except AttributeError:
            # Unable to locate season or episode numbers in filename
            pass
        return self.extracted_data
