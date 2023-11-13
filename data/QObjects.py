from PyQt6.QtWidgets import QPushButton, QLabel, QTextEdit, QWidget, QFileDialog
from PyQt6.QtGui import QIcon
from typing import Union


# The Widget class inherits from the QWidget class stored in PyQt6.QtWidgets. The class creates a fixed size for the
# window, an icon and a name received in the parameter.
class Widget(QWidget):
    def __init__(self, icon: QIcon, title: str):
        super().__init__()
        self.setFixedSize(800, 450)
        self.setWindowIcon(icon)
        self.setWindowTitle(title)


# The PushButton class inherits from the QPushButton class stored in PyQt6.QtWidgets. The class makes the button flat
# and also makes it easier to create.
class PushButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFlat(True)

    def setRect(self, *size):
        from PyQt6.QtCore import QRect

        self.setGeometry(QRect(*size))


# The Label class inherits from the QLabel class stored in PyQt6.QtWidgets. The class sets the style for the text and
# also simplifies the creation of the background.
class Label(QLabel):
    def __init__(self, *args, font_family: str = 'Times New Roman'):
        from PyQt6.QtGui import QFont
        from PyQt6.QtCore import QRect

        super().__init__(*args)
        font = QFont()
        font.setFamily(font_family)
        self.setFont(font)
        self.setStyleSheet(
            'font-size: 17px;'
            'color: rgba(76, 195, 253, 0.8);'
        )
        self.setGeometry(QRect(0, 0, 800, 450))

    def setImage(self, path_to_image: str):
        from PyQt6.QtGui import QPixmap

        self.setPixmap(QPixmap(path_to_image))


# The TextEdit class inherits from the QTextEdit class stored in PyQt6.QtWidgets. The class prohibits text editing and
# sets styles for it, simplifies text alignment in paragraphs, and you can also add new styles rather than overwrite
# them.
class TextEdit(QTextEdit):
    def __init__(
            self,
            *args,
            font_family: str = 'Times New Roman',
            font_size: Union[int, str] = 16,
            font_color: str = 'rgba(76, 195, 253, 0.8)',
            size: tuple = (0, 0, 800, 450)
    ):
        from PyQt6.QtGui import QFont
        from PyQt6.QtCore import QRect
        from file_actions import get_attribute

        super().__init__(*args)
        font = QFont()
        font.setFamily(font_family)
        self.style = ''
        self.style += (f'color: {font_color};'
                       'font-weight: bold;'
                       f'font-size: {font_size}px;'
                       'letter-spacing: 2px;'
                       'border: 0px;')
        self.setGeometry(QRect(*size))
        self.setStyleSheet(self.style)
        self.setFont(font)
        self.setReadOnly(True)

    def alignmentTo(self, position: str):
        from PyQt6.QtCore import Qt

        POSITIONS: dict = {
            'center': Qt.AlignmentFlag.AlignCenter,
            'left': Qt.AlignmentFlag.AlignLeft,
            'right': Qt.AlignmentFlag.AlignRight
        }
        self.setAlignment(POSITIONS[position])

    def addStyleSheet(self, style: str):
        self.style += style
        self.setStyleSheet(self.style)


# The FileDialog class inherits from the QFileDialog class stored in PyQt6.QtWidgets. The class sets the icon and title
# for the dialog box.
class FileDialog(QFileDialog):
    def __init__(self, *args):
        from PyQt6.QtGui import QAbstractFileIconProvider

        super().__init__(*args)
        self.setIconProvider(QAbstractFileIconProvider(r'data\images\icon_2.ico'))
        self.setWindowTitle('Choose directory')
