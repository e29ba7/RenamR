from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QAction,
    QIcon
)
from PyQt6.QtWidgets import QMenu

from renamr.providers.tmdb import TheMovieDB
from renamr.utils.settings import Settings
from renamr.utils.utils import Dir, open_file_dialog
from renamr.ui.baseDialogWindow import DialogWindow
from renamr.ui.button import Button
from renamr.ui.table import Table
from renamr.ui.outputTemplateWindow import TemplateWindow


class Main(DialogWindow):
    '''
    This class represents the main window of the application. It inherits
    from the DialogWindow class and provides additional functionality to
    handle the user interface and user interactions.

    Methods:
        __init__(self) -> None:
            Initializes main window by setting up UI components and connecting signals.

        open_files(self):
            Opens a file dialog to select files and adds files to the table.

        keyPressEvent(self, event):
            Handles when the escape key is pressed, stopping it from closing window.
    '''

    def __init__(self) -> None:
        super().__init__(
            title='RenamR',
            icon='VHS.png',
        )
        '''
        Initializes main window by setting up UI components and connecting signals.
        '''

        # Load settings on application start
        self.settings = Settings()

        # Layout
        # self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 10, 10, 0)
        # self.layout.setRowMinimumHeight(3, 6)
        # self.layout.setRowStretch(15, 0)

        # Table Widget
        self.table = Table()
        self.layout.addWidget(self.table, 0, 0, 2, 10)

        # Open Files Button
        self.open_files_button = Button(text='Open Files')
        self.open_files_button.setDefault(True)
        self.layout.addWidget(self.open_files_button, 2, 0, 1, 1)
        self.open_files_button.clicked.connect(self.open_files)

        # Clear File List Button
        self.clear_file_list_button = Button(text='Clear')
        self.layout.addWidget(self.clear_file_list_button, 2, 1, 1, 1)
        self.clear_file_list_button.clicked.connect(self.table.clear_table)

        # Options Menu Button and Items
        self.options_menu = QMenu('Options Menu')
        self.movie_template_action = QAction(
            icon=QIcon(Dir.get_file('icon', 'make_icon.png')),
            text='Edit Movie Output Template',
            parent=self
        )
        self.tv_template_action = QAction(
            icon=QIcon(Dir.get_file('icon', 'make_icon.png')),
            text='Edit TV Output Template',
            parent=self
        )
        self.options_menu.addAction(self.movie_template_action)
        self.options_menu.addAction(self.tv_template_action)
        self.movie_template_action.triggered.connect(
            lambda: TemplateWindow(
                title='Edit Movie Output Template',
                template_type='movie_template'
            )
        )
        self.tv_template_action.triggered.connect(
            lambda: TemplateWindow(
                title='Edit TV Output Template',
                template_type='tv_template'
            )
        )
        self.options_menu_button = Button(text='Options', icon='searchButton.png')
        self.options_menu_button.setMenu(self.options_menu)
        self.layout.addWidget(self.options_menu_button, 2, 4, 1, 1)

        # Search Menu Button and Items
        self.search_menu = QMenu('Search Menu')
        self.tmdb_movie_action = QAction(
            icon=QIcon(Dir.get_file('icon', 'tmdb.svg')),
            text='TheMovieDB (Movie)',
            parent=self
        )
        self.tmdb_tv_action = QAction(
            icon=QIcon(Dir.get_file('icon', 'tmdb.svg')),
            text='TheMovieDB (TV)',
            parent=self
        )
        self.search_menu.addAction(self.tmdb_movie_action)
        self.search_menu.addSection(QIcon(Dir.get_file('icon', 'xButton.png')), 'TV:')
        self.search_menu.addAction(self.tmdb_tv_action)
        self.tmdb_movie_action.triggered.connect(
            lambda: self.table.movie_lookup(TheMovieDB.movie)
        )
        self.tmdb_tv_action.triggered.connect(
            lambda: self.table.tv_lookup(TheMovieDB.tv)
        )
        self.search_menu_button = Button(text='Search', icon='searchButton.png')
        self.search_menu_button.setMenu(self.search_menu)
        self.layout.addWidget(self.search_menu_button, 2, 5, 1, 1)

        # Rename Button
        self.rename_button = Button(text='Rename')
        self.layout.addWidget(self.rename_button, 2, 9, 1, 1)
        self.rename_button.clicked.connect(self.table.rename_start)

        # Show window
        self.show()

    def open_files(self):
        '''
        Opens a file dialog to select files and adds files to the table.
        '''

        self.file_list: list = open_file_dialog()
        self.table.populate_table(files=self.file_list)

    def keyPressEvent(self, event):
        '''
        Handles when the escape key is pressed, stopping it from closing window.

        Args:
            event: Event when a key is pressed.
        '''

        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
        # else:
        #     super().keyPressEvent(event)
