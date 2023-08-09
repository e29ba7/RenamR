import re
from typing import Callable

from pathlib import Path
from PyQt6.QtCore import pyqtSignal, Qt, QSignalBlocker
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from renamr.ui.unknownmedia import UnknownMediaWindow
from renamr.utils.metadata import Metadata
from renamr.utils.utils import (
    Dir,
    rename_files,
    timer,
)


class Table(QTableWidget):
    '''
    Table class containing many core application functions.
    '''

    button_disable = pyqtSignal(bool)
    app_busy = False

    def __init__(self) -> None:
        super().__init__()
        # Flags
        self.setAlternatingRowColors(True)
        self.setColumnCount(3)
        self.setCornerButtonEnabled(False)
        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSortingEnabled(True)
        self.setWordWrap(False)
        self.verticalHeader().setVisible(False)
        self.cellChanged.connect(self.check_for_errors)
        # Header
        self.horizontalHeader().setHighlightSections(False)
        self.setHorizontalHeaderLabels(['Current Name', 'New Name', 'Error'])
        self.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.Stretch
        )
        self.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch
        )
        self.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )

    def flag_as_busy(func) -> Callable:
        '''
        Decorator to flag the application as busy when running a function
        so another function doesn't try to also run on a different thread.

        Args:
            func (Callable): Function to be run. While running, $app_busy will be True
        '''

        def inner(self, *args, **kwargs):
            if not self.app_busy:
                self.app_busy = True
                func(self, *args, **kwargs)
                self.app_busy = False
        return inner

    def toggle_error_check(func: Callable) -> Callable:
        '''
        Decorator to temporarily block Qt signals before calling the wrapped function.
        Necessary for preventing recursive behavior during function call

        Args:
            func (Callable): Function to be wrapped

        Returns:
            Callable: Passed in function, blocking signals during running.
        '''

        def inner(self, *args, **kwargs):
            with QSignalBlocker(self):
                return func(self, *args, **kwargs)
        return inner

    @toggle_error_check
    @timer
    def populate_table(
        self,
        files: list[Path],
        *args,
        **kwargs
    ) -> None:
        '''
        Iterate through $files, filling `Current Name` with filenames.
        '''

        self.row_count = self.rowCount()
        self._item = 0
        # Get list of items currently loaded in table
        self.current_items: list[str] = [
            self.item(file, 0).data['absolute_path'].__str__()
            for file in range(self.rowCount())
        ]
        # Get items not already loaded from selected files
        self.items_to_add: list[int] = [
            i
            for i, file in enumerate(files)
            if file.__str__() not in self.current_items
        ]
        # Set new row count for table view
        self.setRowCount(self.row_count + len(self.items_to_add))
        # Load $items_to_add to table view
        for row in range((self.row_count), self.rowCount()):
            self.setItem(
                row,
                0,
                Metadata(item=files[self._item])
            )
            self.setItem(row, 1, QTableWidgetItem(''))  # Allows edit when cell empty
            # self.setItem(row, 2, QTableWidgetItem(''))
            self._item += 1
        self.resizeRowsToContents()

    @toggle_error_check
    @timer
    def check_for_errors(self, _row: int = None, _column: int = None) -> None:
        '''
        Check table view for duplicate names in New Name column.
        Also check for invalid characters in New Name.
        Rows that have an error in `New Name` column will be highlighted red.

        Args:
            _row (int): Edited cell's row passed from connected signal.
            _column (int): Edited cell's column from connected signal.
        '''

        self.seen: dict = dict()
        # Iterate through files looking for duplicates in `New Name` column,
        for row in range(self.rowCount()):
            try:
                self._item = self.item(row, 1).text()
                # Assign item text to $_item and check if in $self.seen
                if self._item in self.seen:
                    self.seen[self._item] = True
                    continue
                if self._item:  # Prevents empty cells from being labeled as dupes.
                    self.seen[self._item] = False
            except AttributeError:
                # $_item doesn't have a title, passing
                continue
        # Iterate through files applying errors and tinting errored rows red
        for row in range(self.rowCount()):
            try:
                self._item = self.item(row, 1).text()
                if self.seen.get(self._item):
                    self.set_row_color(row, error = 'Dupe')
                elif re.search(  # Check for invalid characters
                    r'[<>:"/\\\|?*]|[ .]+$',
                    self._item
                ):
                    self.set_row_color(row, error = 'Invalid')
                else:
                    self.set_row_color(row, error = '')
            except AttributeError:
                # $_item doesn't have a title
                self.set_row_color(row, error = '')

    def set_row_color(self, row: int, error: str) -> None:
        '''
        Sets passed in row's color.
        Tint each error row red and add $error to Error column.

        Args:
            row (int): Row to tint red and set Error cell
            error (str): Error text to set in row's Error cell
        '''

        self.setItem(row, 2, QTableWidgetItem(error))
        for column in range(self.columnCount()):
            # Set each column in row to desired color
            # if self.item(row, column):
            if error:
                # Add red tint to errored rows
                self.item(row, column).setBackground(QColor(70, 0, 0, 255))
            else:
                if row == 0 or row % 2 == 0:
                    # Set row background color
                    self.item(row, column).setBackground(QColor(0, 6, 14, 255))
                elif row % 2 > 0:
                    # Set alternate row background color
                    self.item(row, column).setBackground(QColor(0, 31, 43, 255))

    @toggle_error_check
    @flag_as_busy
    @timer
    def movie_lookup(self, provider: Callable) -> None:
        '''
        Iterate through column `Current Name` searching each item with $provider
        for Metadata.
        Sets each 'New Name' column cell with first result from
        provider search results.

        Args:
            provider (Callable): Which provider to probe for information.
        '''

        for file in range(self.rowCount()):
            self._item = self.item(file, 0).data
            # Get movie info from $provider
            self.movie_info: dict = provider(
                query=self._item.get('title'),
                year=self._item.get('year')
            )
            if self.movie_info:
                # Add resolution info to item info dict
                self.movie_info.update({
                    'resolution': self._item.get('resolution', '')
                })
                # Set title in New Name column
                self.setItem(
                    file,
                    1,
                    Metadata(item=self.movie_info)
                )
            else:
                continue
                # Show dialog asking for movie name
                # TODO: Get name and re-search with $provider
                # UnknownMediaWindow(
                #     file=self._item.get('filename'),
                #     title='What movie is this?',
                #     icon=Dir.get_file('icon', 'VHS.png')
                # )
        self.check_for_errors()

    @toggle_error_check
    @flag_as_busy
    @timer
    def tv_lookup(self, provider: Callable) -> None:
        '''
        Loop through files in table view looking for title of series,
        counting seasons along the way.
        Once the series title is found, search Provider for information.
        Provider returns tuple(series_info, season_info, episode_info).
        Apply new episode names to respective files.

        Args:
            provider (Callable): Provider function used to search
        '''

        self.series_title: str = str()
        self.seasons: set[str] = set()
        for file in range(self.rowCount()):
            # Continue to next file looking for title
            if not (item := self.item(file, 0).data)['title']:
                continue
            # Set $series_title
            if not self.series_title:
                self.series_title = item.get('title')
            # Retrieve necessary seasons to search
            if item['season_num']:
                self.seasons.add(int(item['season_num']))
        if not self.seasons:
            return None
        # $provider.tv returns tup(series_info, season_info, episode_info)
        self.series_info, self.seasons_info, self.episodes_info = provider(
            query=self.series_title,
            seasons=self.seasons,
            year=self.item(file, 0).data.get('year', None)
        )
        # If None returned from provider search
        if not self.series_info:
            # TODO
            pass
            # UnknownMediaWindow(
            #     file=item['filename'],
            #     title='What show is this?',
            #     icon=Dir.get_file('icon', 'VHS.png')
            # )
        for file in range(self.rowCount()):
            self.season: str = self.item(file, 0).data.get('season_num', '')
            self.episode: str = self.item(file, 0).data.get('episode_num', '')
            self.data: dict = {
                # Combine Series, Season, and Episode dicts together
                **self.series_info,                                 # Series info
                **self.seasons_info[self.season],                   # Season info
                **self.episodes_info[self.season][self.episode]     # Episode info
            }
            # Set New Name column cell to new filename
            self.setItem(
                file,
                1,
                Metadata(item=self.data)
            )
        self.check_for_errors()

    @toggle_error_check
    @flag_as_busy
    @timer
    def rename_start(self, *args):
        '''
        Check new filenames for forbidden chars, skip over errored filenames,
        and rename files.
        '''

        for row in range(self.rowCount())[::-1]:
            if not self.item(row, 1).text():
                continue
            elif self.item(row, 2).text():
                # TODO
                print('Show fix errors dialog box')
            else:
                rename_files(
                    old_file=(  # Construct old filename
                        (item := self.item(row, 0)).data['directory']
                        .joinpath(item.text()
                        + item.data['extension'])
                    ),
                    new_filename=(  # Construct new filename
                        item.data['directory']
                        .joinpath(self.item(row, 1).text()
                        + item.data['extension'])
                    )
                )
                self.clear_element(row)

    def cancel_process(self, toggle):
        '''
        Cancel running process on main thread
        '''

        print(f'Cancel Process, This is the toggle: {toggle}')

    def clear_table(self) -> None:
        '''
        Clear table view of all items and set row count to 0.
        '''

        self.clearContents()
        self.setRowCount(0)

    def clear_element(self, row: int) -> None:
        '''
        Remove a single row from the table view.

        Args:
            row (int): Row to be removed.
        '''

        self.removeRow(row)
        # self.check_for_errors()
