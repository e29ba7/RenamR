from renamr.ui.baseDialogWindow import DialogWindow
from renamr.ui.button import Button

from PyQt6.QtWidgets import QLabel, QLineEdit


class UnknownMediaWindow(DialogWindow):
    def __init__(
            self,
            file: str,
            title: str,
            icon: str | None,
            size: tuple[int, int] = (300, 150),
    ) -> None:
        '''
        Custom dialog shown when media not found
        '''

        super().__init__(
            title,
            icon,
            size
        )
        self.file = file
        # Layout
        self.layout.setContentsMargins(10, 10, 10, 0)
        # File Label
        self.file_label = QLabel(self.file)
        # self.file_label.setObjectName('file_label')
        self.layout.addWidget(self.file_label, 0, 0, 1, -1)
        # User title search
        self.search_title_textbox = QLineEdit()
        # self.search_title_textbox.returnPressed.connect()
        self.layout.addWidget(self.search_title_textbox, 1, 0, 1, 2)
        # Cancel Button
        self.cancel_button = Button('Cancel')
        self.layout.addWidget(self.cancel_button, 2, 0, 1, -1)
        # Search button
        self.search_button = Button('Search')
        self.layout.addWidget(self.search_button, 2, 1, 1, -1)

        self.exec()
