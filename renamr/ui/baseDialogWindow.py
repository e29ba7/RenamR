from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
)

from renamr.ui.button import Button
from renamr.utils.utils import Dir


class Titlebar(QFrame):
    '''
    Custom titlebar class for base window.
    Clicking and dragging titlebar allows moving window.
    '''

    def __init__(
        self,
        title: str,
        parent,
        icon: QPixmap
    ):
        super().__init__(parent)
        self.setObjectName('Titlebar')
        self.parent = parent
        self.icon = icon

        # Window Flags
        self.setFixedHeight(25)

        # Layout
        self.title_layout = QHBoxLayout()
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.title_layout)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setToolTip('Made by f09f9095')
        self.icon_label.setContentsMargins(5, 0, 5, 0)
        self.icon_label.setPixmap(self.icon)
        self.title_layout.addWidget(self.icon_label)

        # Titlebar Label
        self.label = QLabel(title)
        self.label.setToolTip('Made by f09f9095')
        self.title_layout.addWidget(self.label)

        # Titlebar Spacer
        self.spacer = QLabel()
        self.title_layout.addWidget(self.spacer, 1)

        # Minimize Button
        self.minimize_button = Button(icon='minimizeButton.png', name='MinimizeButton')
        # self.minimize_button.setFixedWidth(30)
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.title_layout.addWidget(self.minimize_button)

        # Close Button
        self.close_button = Button(icon='xButton.png', name='CloseButton')

        # self.close_button.setFixedWidth(30)
        self.close_button.clicked.connect(self.parent.close)
        self.title_layout.addWidget(self.close_button)

        # For dragging window
        self.dragging = False

    # Begin dragging by titlebar
    def mousePressEvent(self, mouse_event):
        '''
        Handles a mouse press event.

        Args:
            mouse_event: Mouse press event.
        '''

        self.drag_position = mouse_event.globalPosition().toPoint()
        self.dragging = True

    # While dragging by titlebar
    def mouseMoveEvent(self, mouse_event):
        '''
        Handles dragging the window around.
        '''

        if self.dragging:
            self.window().move(
                self.window().pos()
                + mouse_event.globalPosition().toPoint()
                - self.drag_position
            )
            self.drag_position = mouse_event.globalPosition().toPoint()
            mouse_event.accept()

    # After titlebar is released
    def mouseReleaseEvent(self, mouse_event):
        self.dragging = False


class DialogWindow(QDialog):
    '''
    Custom class of QDialog used as the base for windows.
    '''

    def __init__(
            self,
            title: str,
            icon: str = 'VHS.png',
            size: tuple | None = None
    ) -> None:
        super().__init__()
        self.title = title
        self.icon = Dir.get_file('icon', icon)
        self.size = size

        # Window Flags
        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle(self.title)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        if self.size:
            self.setMinimumSize(self.size[0], self.size[1])
        else:
            self.setMinimumSize(800, 400)
            self.setMaximumSize(1600, 800)

        # Main Layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # self.layout.setContentsMargins(10, 10, 10, 0)

        # Titlebar
        self.titlebar = Titlebar(
            parent=self,
            title=self.title,
            icon=QIcon(self.icon).pixmap(24, 24)
        )
        self.layout.setMenuBar(self.titlebar)
