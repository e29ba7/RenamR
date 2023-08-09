from PyQt6.QtWidgets import QLabel, QLineEdit, QFrame, QGridLayout

from renamr.ui.baseDialogWindow import DialogWindow
from renamr.ui.button import Button
from renamr.utils.settings import Settings
from renamr.utils.utils import translator


class TemplateWindow(DialogWindow):
    '''
    Custom dialog window to let user set value for a template and save it to the config.
    '''

    def __init__(
        self,
        title: str,
        template_type: str,
    ) -> None:
        super().__init__(
            title=title,
            size=(500, 600)
        )
        self.data: dict = dict()

        # Load application settings from `config.ini`
        self.settings = Settings()

        # Layout
        # self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 10, 10, 0)

        # Window Message label
        self.message_label = QLabel(
            text=f'Edit {template_type.split("_")[0]} template using tokens below.'
        )
        self.message_label.setMaximumHeight(15)  # Find way to remove need for this
        self.layout.addWidget(self.message_label, 0, 0, 1, -1)

        # Template edit box
        # Fill template edit box with saved template or default
        self.template_edit_box = QLineEdit(getattr(self.settings, template_type))
        self.template_edit_box.setPlaceholderText(
            f'Customize {template_type.split("_")[0]} template'
        )
        self.template_edit_box.setMinimumHeight(30)
        self.layout.addWidget(self.template_edit_box, 1, 0, 1, -1)

        # Frame header label
        self.frame_header_label = QLabel('Available Tokens')
        self.frame_header_label.setContentsMargins(0, 10, 0, 0)
        self.frame_header_label.setMaximumHeight(20)  # Find way to remove need for this
        self.frame_header_label.setObjectName('FrameLabel')
        self.layout.addWidget(self.frame_header_label, 2, 0, 1, -1)

        # Frame and frame layout
        self.frame = QFrame()
        self.frame.setObjectName('TemplateFrame')
        # self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_layout = QGridLayout()
        self.frame.setLayout(self.frame_layout)
        self.layout.addWidget(self.frame, 3, 0, 2, 4)

        # Populate frame with labels
        self._populate_frame_table()

        # Cancel Button
        self.cancel_button = Button(
            text='Cancel',
            icon='cancelButton.png',
        )
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button, 5, 1, 1, 1)

        # Save Button
        self.save_button = Button(
            text='Save',
            icon='floppy.png',
        )
        self.save_button.setDefault(True)
        self.save_button.clicked.connect(
            lambda:
            self.save_button_action(
                setting=template_type,
                value=self.template_edit_box.text()
            )
        )
        self.layout.addWidget(self.save_button, 5, 2, 1, 1)

        # Execute window
        self.exec()

    def _populate_frame_table(self) -> None:
        '''
        Populates the frame with tokens and names from the translator.
        Sets headers and linebreaks based on specific keys and increments, respectively.
        '''

        self.column: int = 0
        self.row: int = 0
        # Look through key: item pairs in translator
        for key, item in translator.items():
            # Go to next column after 20 items
            if self.row == 20:
                self.column += 1
                self.row = 0
            # Add various section headers
            if key == '%title':
                self._set_frame_token_header(label='General')
            if key == '%company':
                self._set_frame_token_header(label='Movies')
            if key == '%lay':
                self._set_frame_token_header(label='Series')
            if key == '%st':
                self._set_frame_token_header(label='Seasons')
            if key == '%et':
                self._set_frame_token_header(label='Episodes')
            if key == '%date':
                self._set_frame_token_header(label='Date')
            self.frame_item = QLabel(text=f'{key} - {item}')
            self.frame_layout.addWidget(self.frame_item, self.row, self.column)
            self.row += 1

    def _set_frame_token_header(self, label: str) -> None:
        '''
        Sets the frame token section header with the provided label.

        Args:
            label (str): The label text for the frame token header.
        '''

        self.frame_item = QLabel(text=label)
        self.frame_item.setStyleSheet(
            '''
            text-decoration: underline;
            font-weight: bold;
            qproperty-alignment: right;
            '''
        )
        self.frame_layout.addWidget(self.frame_item, self.row, self.column)
        self.row += 1

    def save_button_action(self, setting, value) -> None:
        '''
        Saves a setting with its corresponding value and closes the current dialog.

        Args:
            setting: The setting to be saved.
            value: The value to be associated with the setting.

        Example:
            >>> save_button_action('movie_template', '%title - %y')
            # Saves setting 'movie_template' as '%title - %y' and closes the dialog.
        '''

        self.settings.save_setting(setting, value)
        self.accept()

