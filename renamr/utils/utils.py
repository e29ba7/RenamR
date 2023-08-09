import re
import time

from pathlib import Path
from PyQt6.QtWidgets import QFileDialog
from typing import Callable


'''
Contains general classes, functions, and decorators used throughout RenamR.
'''


class Dir:
    '''
    A utility class to handle directory paths and resources.

    Attributes:
        root (Path): The root path of the application.
        resource_dir (Path): The path to the resources directory, relative to base path.
        themes (Path): The path to the themes directory within the resources directory.
        icons (Path): The path to the icons directory within the resources directory.

    Methods:
        root(cls, filename: str) -> str:
            Returns the absolute path of a file in the app's root directory.

        theme(cls, filename: str) -> str:
            Returns the absolute path of a QSS file in the app's theme directory.

        icon(cls, filename: str) -> str:
            Returns the absolute path of an icon file in the app's icon directory.
    '''

    root = Path(__file__).parents[2]
    resource_dir = root / 'renamr/ui/resources'
    theme = resource_dir / 'themes'
    icon = resource_dir / 'icons'

    @classmethod
    def get_file(cls, path: str, filename: str) -> str:
        '''
        Returns the absolute path of a file in the app's specified directory.

        Args:
            dir_name (str): The directory name to be searched
            filename (str): The name of the file to be located in the root directory.

        Returns:
            str: The absolute path of the specified icon file in the icon directory.
        '''

        return str(getattr(Dir, path) / filename)


def timer(func: Callable) -> Callable:
    '''
    A decorator that measures the execution time of the given function,
    prints the result to console, then returns the result of given function.

    Args:
        func (Callable): Function to be wrapped and timed.

    Returns:
        Result of decorated function
    '''

    def inner(self, *args, **kwargs):
        start = time.time()
        res = func(self, *args, **kwargs)
        print(f'{func.__name__} took {time.time() - start:.2f}s')
        return res
    return inner


def open_file_dialog() -> list[Path]:
    '''
    Open file dialog, allowing video file types.
    Multiple files can be selected.

    Returns:
        list: Path objects of all selected files in file dialog
    '''

    files = QFileDialog.getOpenFileNames(
        caption='Select File(s)',
        filter='''
            Video Files (*.avi *.mkv *.mov *.mp4 *.ts *.vob);;
            All Files (*.*)
        '''
    )
    files = [Path(file) for file in files[0]]
    return files


def clean_title(title: str) -> str | None:
    '''
    Clean and sanitize a filename string for use as the search query with providers.

    This function takes a filename as input and performs the following operations:
        1. Remove error-prone characters and bulk rename elements.
        2. Replace hyphens and periods with spaces.
        3. Extract the title from the filename based on specific patterns.
        4. Remove forbidden filename characters like / \\ < > " | ? *.
        5. Replace colons (:) with hyphens ( -).
        6. Reduce multiple consecutive spaces to a single space.
        7. Remove trailing spaces from the title.

    Args:
        title (str): The input filename string to extract title and clean.

    Returns:
        str | None: The cleaned title string, or None if the title extraction step
            results in no match.

    Examples:
        >>> clean_title("My.Movie.Title.2023.1080p.BluRay")
        # 'My Movie Title'
        >>> clean_title("TV.Show.S01E01.Pilot.HDTV.x264")
        # 'TV Show'
        >>> clean_title("movie_with_s [year] 2023 - 1080p")
        # 'movie with s'
    '''

    try:
        # Remove error prone characters
        title = re.sub(
            r'''(?ix)
                [^a-z0-9\ \-\'\"\.()\[\]\!]     # Remove chars not in this list
                |(\(|\[)\d{1,2}(\)|\])          # Remove bulk rename elements
            ''',
            '',
            title
        )
        # Replace - and . with a space
        title = re.sub(
            r'\-|\.',
            ' ',
            title
        )
        # Get title from filename
        title = re.search(
            r'''(?ix)
                ^[a-z0-9\ \'\"\.()\[\]\-=+&%$#@\!]*?   # Match these characters
                (?=                                    # Begin lookahead
                    (?:[0-6]?[0-9](e|x|\-)             # Find season number
                    |(?:s\d+)                          # Or find season with preceding s
                    |(?:(18|19|20)\d{2})               # Or find year
                    |(?:(1080|720|512|480)(p|i))       # Or find resolution
                    |(?:[\[\]\(\)]))                   # Or find brackets
                )
            ''',
            title
        ).group()
    except AttributeError:
        # Title Regex search returned no result
        pass
    finally:
        title = re.sub(r'[/\\<>"|?*]', '', title)  # Remove forbidden filename chars
        title = re.sub(r':', ' -', title)          # Replace colon (:) with hyphen ( -)
        title = re.sub(                            # Reduce multiple spaces
            r'[ ]{2,}',
            ' ',
            title
        )
        title = re.sub(                            # Remove space from end of title
            r' +$',
            '',
            title
        )
    return title


def remove_forbidden_chars(s: str) -> str:
    '''
    Remove common OS forbidden filename characters from string

    Args:
        s (str): String to remove forbidden OS filename characters from

    Returns:
        str: Cleaned string, free from forbidden characters
    '''

    return re.sub(r'[/\\<>"|?*]', '', s)


def replace_colon(s: str) -> str:
    '''
    Replace any occurring `:` (colon) with ` -`(space, hyphen) in string

    Args:
        s (str): String to be cleaned

    Returns:
        str: String with any occurring `:` replaced with ` -`
    '''

    return re.sub(r':', ' -', s)


def format_new_filename(new_data: dict, template: str) -> str:
    '''
    Format a new filename string using new data and a user specified
    template loaded from `config.ini`.

    It uses regex substitution and the $translator dictionary to match
    placeholders in user template with keys in the `new_data` dictionary
    and replaces them with the corresponding values.

    Args:
        new_data (dict):
            A dictionary containing data to be pulled from. Used to replace
            placeholders in retrieved template from settings.

        template (str):
            The template containing placeholders to be replaced with data
            from the `new_data` dictionary.

    Returns:
        str: 
            String with placeholders replaced by the corresponding data from `new_data`.

    Movie Example:
        new_data = {title: Sintel, year: '2010', id: '45745'}
        movie_template = '%title - (%y) - [%id]'
        >>> result = format_new_filename(new_data, template)
        # Result: 'Sintel - (2010) - [45745]'

    TV Example:
        new_data = {title: 'Show', episode: '2', season: '3', episode_title: 'Pilot'}
        tv_template = '%title - %sx%ep - %et'
        >>> result = format_new_filename(new_data, template)
        # Result: 'Show - 3x02 - Pilot'
    '''

    return re.sub(
        r'|'.join(translator.keys()),                       # Join list of tokens
        lambda m: new_data.get(translator[m.group()], ''),  # Get data matching token
        template                                            # Filename output template
    )


def filter_new_title(text: str) -> str:
    '''
    Filters a given text by replacing '/' with ' - ' and ':' with ' -'.

    Args:
        text (str): The input text to be filtered.

    Returns:
        str: The filtered text with '/' replaced by ' - ' and ':' replaced by ' -'.

    Examples:
        >>> filter_new_title('Hello World: Example')
        # 'Hello World - Example'
        >>> filter_new_title('Hello World 1/2: Example)
        # 'Hello World 1 - 2 - Example
    '''

    text = text.replace('/', ' - ')
    text = text.replace(':', ' -')
    return text


def rename_files_by_move(old_file: Path, new_filename):
    ...


def rename_files(old_file: Path, new_filename: Path) -> None:
    '''
    Renames a file specified by $old_file to provided $new_filename
    using pathlib.rename().

    Args:
        old_file (Path): Full path and filename of file to be renamed
        new_filename (Path): Full path and filename for $old_file to be renamed to
    '''

    # Simple file rename, should improve
    try:
        old_file.rename(new_filename)
    except (FileNotFoundError, FileExistsError):
        # Old file not found
        # or new file already exists
        pass


# Dictionary for translating user custom naming schemes from tokens to text.
# Notice tokens %t, %s, and %e are the last of the t, s, and e tokens.
# Tokens must be in (somewhat) reverse alphabetical order for proper functionality.
translator: dict = {
    # General
    r'%title': 'title',
    r'%ot': 'original_title',
    r'%id': 'id',
    r'%g': 'genre',
    r'%res': 'resolution',
    r'%status': 'status',
    r'%tag': 'tagline',
    r'%o': 'overview',
    r'%rv': 'rating_votes',
    r'%r': 'rating',
    r'%type': 'type',
    # Movie specific
    r'%company': 'production_company',
    r'%country': 'production_country',
    r'%ml': 'movie_language',
    r'%mrun': 'runtime',
    r'%b': 'budget',
    r'%p': 'profit',
    r'%col': 'collection',
    # Series specific
    r'%lay': 'last_air_year',
    r'%lam': 'last_air_month',
    r'%lad': 'last_air_day',
    r'%ladate': 'last_air_date',
    r'%c': 'origin_country',
    r'%lo': 'original_language',
    r'%l': 'language',
    r'%n': 'network',
    r'%te': 'total_episodes',
    r'%ts': 'total_seasons',
    # Season specific
    r'%st': 'season_title',
    r'%so': 'season_overview',
    r'%spy': 'season_premiere_year',
    r'%spm': 'season_premiere_month',
    r'%spd': 'season_premiere_day',
    r'%spdate': 'season_premiere_date',
    r'%sec': 'season_episode_count',
    r'%sr': 'season_rating',
    r'%sp': 'season_num_pad',
    r'%s': 'season_num',
    # Episode specific
    r'%et': 'episode_title',
    r'%eid': 'episode_id',
    r'%erun': 'episode_runtime',
    r'%er': 'episode_rating',
    r'%evotes': 'episode_rating_votes',
    r'%esummary': 'episode_summary',
    r'%ey': 'episode_air_year',
    r'%em': 'episode_air_month',
    r'%ed': 'episode_air_day',
    r'%ep': 'episode_num_pad',
    r'%e': 'episode_num',
    # Date
    r'%date': 'release_date',
    r'%y': 'year',
    r'%m': 'month',
    r'%d': 'day',
}
