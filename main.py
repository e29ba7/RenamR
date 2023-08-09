from PyQt6.QtWidgets import QApplication

from renamr.ui.mainWindow import Main
from renamr.utils.utils import Dir


THEME = 'Dork'

if __name__ == '__main__':
    app = QApplication([])
    try:
        with open(Dir.get_file('theme', f'{THEME}.qss'), 'r') as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print(f'{THEME}.qss not found in `theme`')
    window = Main()
    app.exec()
