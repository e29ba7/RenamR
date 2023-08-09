from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QSizePolicy

from renamr.utils.utils import Dir


class Button(QPushButton):
    '''
    Custom button class that applies button settings.
    '''

    def __init__(
        self,
        text: str = '',
        icon: str = '',
        name: str = 'Button',
        minimum: int = 15,
        maximum: int = 30
    ) -> None:
        super().__init__(QIcon(Dir.get_file('icon', icon)), text)
        self.setObjectName(name)  # Needed for QSS to properly identify
        self.setMinimumHeight(minimum)
        self.setMaximumSize(100, maximum)
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding
        )
