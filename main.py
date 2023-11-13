from PyQt6.QtCore import pyqtSlot
from data.QObjects import Widget, Label, TextEdit
from data.ButtonLanguage import ButtonLanguage
from typing import Union


# The new_theme function takes as parameters the variables path_to_settings of the string type, which stores the path
# to the file with the settings, background of the Label class, name of the string type, which stores the name of the
# class. The routine changes the theme in the settings, thereby changing the theme of the application.
def new_theme(path_to_settings: str, background: Label, name: str):
    from file_actions import set_attribute, get_attribute

    theme = get_attribute(path_to_file=path_to_settings, name_attribute='theme')
    set_attribute(
        path_to_file=path_to_settings,
        name_attribute='theme',
        new_value='White' if theme == 'Black' else 'Black'
    )
    theme = 'White' if theme == 'Black' else 'Black'
    language = get_attribute(path_to_file=path_to_settings, name_attribute='language')
    background.setImage('\\'.join(['data', 'images', f'{name}_{theme.lower()}_{language}.jpg']))


# The new_language function takes as parameters the variables path_to_settings of the string type, which stores the
# path to the file with the settings, language of the ButtonLanguage class, background of the Label class, name of the
# string type, which stores the name of the class, history of the TextEdit class, which will be None by default. The
# routine changes the language in the settings, thereby changing the language in the application.
def new_language(
        path_to_settings: str,
        language: ButtonLanguage,
        background: Label,
        name: str,
        history: Union[TextEdit, None] = None
):
    from file_actions import get_attribute
    from get_history import get_history

    theme = get_attribute(path_to_file=path_to_settings, name_attribute='theme')
    language.rewrite_language()
    if history is not None: history.setText(get_history(path_to_settings))
    background.setImage(
        path_to_image='\\'.join(['data', 'images', f'{name}_{theme.lower()}_{language.settings_of_language}.jpg'])
    )
    

# The Introduction class inherits from the Widget class. Creates an "Introduction" window, using the TextEdit class and
# the get_introduction function to display text on the window.
class Introduction(Widget):
    def __init__(self, path_to_settings: str):
        from PyQt6.QtGui import QIcon
        from file_actions import get_attribute

        super().__init__(QIcon(r'data\images\icon_1.ico'), 'Introduction')
        self.path_to_settings = path_to_settings
        self.text = TextEdit(
            self,
            font_family=r'data\font\AcromThin.ttf'
        )
        self.main_part()

    def main_part(self):
        from PyQt6.QtGui import QShortcut, QKeySequence
        from file_actions import get_attribute, get_introduction

        text = [
            get_introduction(
                path_to_file=r"data\introduction",
                paragraph=paragraph,
                lang=get_attribute(path_to_file=self.path_to_settings, name_attribute="language")
            ) for paragraph in range(1, 3)
        ]
        space = '<br><br>'
        if get_attribute(path_to_file=self.path_to_settings, name_attribute='theme') == 'White':
            self.text.addStyleSheet('background-color: White;')
        else:
            self.text.addStyleSheet('background-color: rgb(32, 38, 54);')
        self.text.setText(space + space.join(text))
        self.text.alignmentTo('center')
        shortcut = QShortcut(QKeySequence('Space'), self.text)
        shortcut.activated.connect(self.main_window)
        self.show()

    @pyqtSlot()
    def main_window(self):
        from file_actions import get_attribute, set_attribute

        set_attribute(path_to_file=self.path_to_settings, name_attribute='input_text', new_value='False')
        if get_attribute(path_to_file=self.path_to_settings, name_attribute='main_body') == '1':
            self.main_window = FirstMainWindow(self.path_to_settings)
        else:
            self.main_window = SecondMainWindow(self.path_to_settings)
        self.main_window.show()
        self.close()


# The FirstMainWindow and SecondMainWindow classes inherit from the Widget class. They create PushButton buttons and a
# background using the Label class, process keystrokes, and display the translation history using the TextEdit class.
class FirstMainWindow(Widget):
    def __init__(self, path_to_settings: str):
        from PyQt6.QtGui import QIcon
        from data.QObjects import PushButton

        super().__init__(QIcon(r'data\images\icon_1.ico'), 'Main')
        self.path_to_settings, self.font_family = path_to_settings, r"data\font\AcromThin.ttf"
        self.background, self.save_path, self.by = tuple(Label(self, font_family=self.font_family) for _ in range(3))
        self.history = TextEdit(
            self,
            font_family=self.font_family,
            font_size=12,
            font_color='white',
            size=(490, 80, 291, 291)
        )
        self.about, self.calculator, self.settings = tuple(PushButton(self) for _ in range(3))
        self.language = ButtonLanguage(self, path_to_settings=self.path_to_settings)
        self.main_part()

    def main_part(self):
        from PyQt6.QtCore import QRect
        from file_actions import get_attribute
        from get_history import get_history

        theme, language = tuple(
            [get_attribute(path_to_file=self.path_to_settings, name_attribute=name) for name in ['theme', 'language']]
        )
        self.background.setImage('\\'.join(['data', 'images', f'FirstMainWindow_{theme}_{language}.jpg']))
        self.save_path.setGeometry(QRect(175, 324, 241, 25))
        self.save_path.setText(get_attribute(path_to_file=self.path_to_settings, name_attribute='saves')[:25])
        self.by.setGeometry(QRect(740, 382, 47, 61))
        self.by.setText('me')
        self.history.addStyleSheet(
            'background-color: rgba(0, 0, 0, 0);'
            'border: 0px;'
        )
        self.language.clicked.connect(
            lambda: new_language(self.path_to_settings, self.language, self.background, 'FirstMainWindow', self.history)
        )
        self.history.setText(get_history(self.path_to_settings))
        self.settings.setRect(140, 120, 171, 31)
        self.settings.clicked.connect(self.settings_window)
        self.about.setRect(150, 180, 161, 41)
        self.about.clicked.connect(self.About)
        self.calculator.setRect(73, 28, 310, 55)
        self.calculator.clicked.connect(self.translate_window)
        self.show()

    def keyPressEvent(self, e):
        from PyQt6.QtCore import Qt

        match e.key():
            case Qt.Key.Key_F:
                self.translate_window()
            case Qt.Key.Key_R:
                new_theme(path_to_settings=self.path_to_settings, background=self.background, name='FirstMainWindow')
            case Qt.Key.Key_Escape:
                self.close()

    @pyqtSlot()
    def translate_window(self):
        self.translate_screen = Translate(self.path_to_settings)
        self.translate_screen.show()
        self.close()

    @pyqtSlot()
    def settings_window(self):
        from file_actions import get_attribute

        if get_attribute('data/settings', 'settings_body') == '1':
            self.settings_screen = FirstSettings(self.path_to_settings)
        else:
            self.settings_screen = SecondSettings(self.path_to_settings)
        self.settings_screen.show()
        self.close()

    @pyqtSlot()
    def About(self):
        self.input_screen = Introduction(self.path_to_settings)
        self.input_screen.show()
        self.close()


class SecondMainWindow(Widget):
    def __init__(self, path_to_settings: str):
        from PyQt6.QtGui import QIcon
        from data.QObjects import PushButton
        from file_actions import get_attribute

        super().__init__(QIcon(r'data\images\icon_1.ico'), 'Main')
        self.path_to_settings, self.font_family = path_to_settings, r"data\font\AcromThin.ttf"
        self.background, self.save_path = tuple(Label(self, font_family=self.font_family) for _ in range(2))
        self.settings, self.about, self.quit, self.calculator = tuple(PushButton(self) for _ in range(4))
        self.history = TextEdit(
            self,
            font_family=r"data\font\AcromThin.ttf",
            size=(394, 160, 321, 261),
            font_size=12,
            font_color='rgba(55, 197, 151, 0.8)'
        )
        self.language = ButtonLanguage(self, path_to_settings=self.path_to_settings)
        self.main_part()

    def main_part(self):
        from PyQt6.QtCore import QRect
        from file_actions import get_attribute
        from get_history import get_history

        theme, language = tuple(
            [get_attribute(path_to_file=self.path_to_settings, name_attribute=name) for name in ['theme', 'language']]
        )
        self.background.setImage(
            path_to_image='\\'.join(['data', 'images', f'SecondMainWindow_{theme}_{language}.jpg'])
        )
        self.settings.setRect(24, 40, 91, 23)
        self.settings.clicked.connect(self.Settings)
        self.about.setRect(20, 110, 91, 23)
        self.about.clicked.connect(self.About)
        self.quit.setRect(10, 180, 91, 23)
        self.quit.clicked.connect(self.close)
        self.save_path.setGeometry(QRect(168, 150, 141, 20))
        self.save_path.setStyleSheet(
            'color: rgba(55, 197, 151, 0.8);'
            'font-size: 17px;'
        )
        self.save_path.setText(get_attribute(path_to_file=self.path_to_settings, name_attribute='saves')[:18])
        self.history.addStyleSheet(
            'border: 0px;'
            'background-color: rgba(0, 0, 0, 0);'
        )
        self.history.setText(get_history(path_to_settings=self.path_to_settings))
        self.calculator.setRect(390, 22, 331, 51)
        self.calculator.clicked.connect(self.translate_window)
        self.language.clicked.connect(
            lambda: new_language(
                self.path_to_settings, self.language, self.background, 'SecondMainWindow', self.history
            )
        )
        self.show()

    def keyPressEvent(self, e):
        from PyQt6.QtCore import Qt

        match e.key():
            case Qt.Key.Key_F:
                self.translate_window()
            case Qt.Key.Key_R:
                new_theme(path_to_settings=self.path_to_settings, background=self.background, name='SecondMainWindow')
            case Qt.Key.Key_Escape:
                self.close()

    @pyqtSlot()
    def translate_window(self):
        self.translate = Translate(self.path_to_settings)
        self.translate.show()
        self.close()

    @pyqtSlot()
    def Settings(self):
        from file_actions import get_attribute

        if get_attribute(self.path_to_settings, 'settings_body') == '1':
            self.settings_screen = FirstSettings(self.path_to_settings)
        else:
            self.settings_screen = SecondSettings(self.path_to_settings)
        self.settings_screen.show()
        self.close()

    @pyqtSlot()
    def About(self):
        self.about_screen = Introduction(self.path_to_settings)
        self.about_screen.show()
        self.close()


# The FirstSettings and SecondSettings classes are inherited from the Widget class. They create PushButtons that can be
# used to change application settings: theme, version, saving path, printing.
class FirstSettings(Widget):
    def __init__(self, path_to_settings):
        from PyQt6.QtGui import QIcon
        from data.QObjects import Label, PushButton

        super().__init__(QIcon(r'data\images\icon_1.ico'), 'Settings')
        self.path_to_settings, self.font_family = path_to_settings, r'data\font\AcromThin.ttf'
        self.background = Label(self)
        self.save_button, self.theme_button, self.version, self.print_button, self.back = tuple(
            PushButton(self) for _ in range(5)
        )
        self.language = ButtonLanguage(self, path_to_settings=self.path_to_settings)
        self.main_part()

    def main_part(self):
        from file_actions import get_attribute

        theme, language = tuple(
            [get_attribute(path_to_file=self.path_to_settings, name_attribute=name) for name in ['theme', 'language']]
        )
        self.background.setImage(path_to_image='\\'.join(['data', 'images', f'FirstSettings_{theme}_{language}.jpg']))
        self.save_button.setRect(370, 92, 75, 31)
        self.save_button.clicked.connect(self.save_directory)
        self.theme_button.setRect(290, 162, 231, 31)
        self.theme_button.clicked.connect(
            lambda: new_theme(self.path_to_settings, self.background, name='FirstSettings')
        )
        self.version.setRect(360, 232, 81, 31)
        self.version.clicked.connect(self.settings_window)
        self.language.clicked.connect(
            lambda: new_language(self.path_to_settings, self.language, self.background, 'FirstSettings')
        )
        self.print_button.setRect(370, 310, 75, 23)
        self.print_button.clicked.connect(self.print_docx)
        self.back.setRect(370, 380, 75, 31)
        self.back.clicked.connect(self.main_window)

    def save_directory(self):
        from data.QObjects import FileDialog
        from file_actions import set_attribute, get_attribute

        directory = FileDialog.getExistingDirectory(self, directory='')
        if directory not in [get_attribute(path_to_file=self.path_to_settings, name_attribute='saves'), '']:
            set_attribute(path_to_file=self.path_to_settings, name_attribute='saves', new_value=directory)

    def keyPressEvent(self, e):
        from PyQt6.QtCore import Qt

        match e.key():
            case Qt.Key.Key_B:
                self.main_window()
            case Qt.Key.Key_R:
                new_theme(self.path_to_settings, self.background, name='FirstSettings')
            case Qt.Key.Key_Escape:
                self.close()

    def print_docx(self):
        self.printer = Printer(self.path_to_settings)
        self.printer.show()

    @pyqtSlot()
    def main_window(self):
        from file_actions import get_attribute

        if get_attribute(path_to_file=self.path_to_settings, name_attribute='main_body') == '1':
            self.main_body = FirstMainWindow(self.path_to_settings)
        else:
            self.main_body = SecondMainWindow(self.path_to_settings)
        self.main_body.show()
        self.close()

    @pyqtSlot()
    def settings_window(self):
        from file_actions import set_attribute

        for name_attribute in ['settings_body', 'main_body']:
            set_attribute(path_to_file=self.path_to_settings, name_attribute=name_attribute, new_value='2')
        self.settings = SecondSettings(self.path_to_settings)
        self.settings.show()
        self.close()


class SecondSettings(Widget):
    def __init__(self, path_to_settings):
        from PyQt6.QtGui import QIcon
        from data.QObjects import Label, PushButton
        from data.ButtonLanguage import ButtonLanguage

        super().__init__(QIcon(r'data\images\icon_1.ico'), 'Settings')
        self.path_to_settings, self.font_family = path_to_settings, r'data\font\AcromThin.ttf'
        self.background = Label(self)
        self.print_button, self.theme_button, self.save_button, self.version, self.back = tuple(
            PushButton(self) for _ in range(5)
        )
        self.language = ButtonLanguage(self, path_to_settings=self.path_to_settings)
        self.main_part()

    def main_part(self):
        from file_actions import get_attribute

        theme, language = tuple(
            [get_attribute(path_to_file=self.path_to_settings, name_attribute=name) for name in ['theme', 'language']]
        )
        self.background.setImage(path_to_image='\\'.join(['data', 'images', f'SecondSettings_{theme}_{language}.jpg']))
        self.theme_button.setRect(310, 190, 171, 23)
        self.theme_button.clicked.connect(
            lambda: new_theme(self.path_to_settings, self.background, name='SecondSettings')
        )
        self.save_button.setRect(360, 140, 75, 16)
        self.save_button.clicked.connect(self.save_directory)
        self.version.setRect(364, 250, 68, 30)
        self.version.clicked.connect(self.settings_window)
        self.print_button.setRect(374, 310, 61, 21)
        self.print_button.clicked.connect(self.print_docx)
        self.language.clicked.connect(
            lambda: new_language(self.path_to_settings, self.language, self.background, 'SecondSettings')
        )
        self.back.setRect(370, 362, 61, 30)
        self.back.clicked.connect(self.main_window)

    def save_directory(self):
        from data.QObjects import FileDialog
        from file_actions import set_attribute, get_attribute

        directory = FileDialog.getExistingDirectory(self, directory='')
        if directory not in [get_attribute(path_to_file=self.path_to_settings, name_attribute='saves'), '']:
            set_attribute(path_to_file=self.path_to_settings, name_attribute='saves', new_value=directory)

    def keyPressEvent(self, e):
        from PyQt6.QtCore import Qt

        match e.key():
            case Qt.Key.Key_B:
                self.main_window()
            case Qt.Key.Key_R:
                new_theme(self.path_to_settings, self.background, name='SecondSettings')
            case Qt.Key.Key_Escape:
                self.close()

    def print_docx(self):
        self.printer = Printer(self.path_to_settings)
        self.printer.show()

    @pyqtSlot()
    def main_window(self):
        from file_actions import get_attribute

        if get_attribute(path_to_file=self.path_to_settings, name_attribute='main_body') == '1':
            self.main_body = FirstMainWindow(self.path_to_settings)
        else:
            self.main_body = SecondMainWindow(self.path_to_settings)
        self.main_body.show()
        self.close()

    @pyqtSlot()
    def settings_window(self):
        from file_actions import set_attribute

        for name_attribute in ['settings_body', 'main_body']:
            set_attribute(path_to_file=self.path_to_settings, name_attribute=name_attribute, new_value='1')
        self.settings = FirstSettings(self.path_to_settings)
        self.settings.show()
        self.close()


# The Printer class inherits from the Widget class. Displays the text of the story using the TextEdit class, a button
# with which you can preview the text being printed and print the text without preview.
class Printer(Widget):
    def __init__(self, path_to_settings):
        from PyQt6.QtGui import QIcon
        from data.PrinterButton import Button

        super().__init__(QIcon(r'data\images\icon_2.ico'), 'Print')
        self.path_to_settings, self.font_family = path_to_settings, r'data\font\AcromThin.ttf'
        self.setFixedSize(550, 350)
        self.background = Label(self)
        self.printable_text = TextEdit(
            self,
            font_family=self.font_family,
        )
        self.print_button, self.preview_button = tuple(Button(self) for _ in range(2))
        self.main_part()

    def main_part(self):
        from PyQt6.QtWidgets import QGridLayout
        from PyQt6.QtCore import QRect
        from file_actions import get_attribute
        from get_history import get_history

        theme = get_attribute(path_to_file=self.path_to_settings, name_attribute='theme')
        self.background.setGeometry(QRect(0, 0, 550, 350))
        self.background.setStyleSheet(f'background-color: {"White" if theme == "White" else "rgb(32, 38, 54)"}')
        self.printable_text.addStyleSheet(
            'background-color: rgba(0, 0, 0, 0);'
        )
        self.printable_text.setText(get_history(self.path_to_settings))
        layout = QGridLayout(self)
        layout.addWidget(self.printable_text, 0, 0, 1, 2)
        layout.addWidget(self.print_button, 1, 0)
        layout.addWidget(self.preview_button, 1, 1)
        self.print_button.setText('Print')
        self.print_button.clicked.connect(self.print)
        self.preview_button.setText('Preview')
        self.preview_button.clicked.connect(self.preview)

    def print(self):
        from PyQt6.QtPrintSupport import QPrintDialog
        from PyQt6.QtWidgets import QDialog

        dialog = QPrintDialog()
        if dialog.exec() == QDialog.accepted:
            self.printable_text.document().print(dialog.printer())

    def preview(self):
        from PyQt6.QtPrintSupport import QPrintPreviewDialog
        from PyQt6.QtGui import QIcon

        dialog = QPrintPreviewDialog()
        dialog.setWindowIcon(QIcon(r'data\images\icon_2.ico'))
        dialog.paintRequested.connect(self.printable_text.print)
        dialog.exec()


# The Translate class inherits from the Widget class. Creates input fields using the TextEdit class, sends the
# resulting result using the number_systems function, and prints the returned result of this function.
class Translate(Widget):
    def __init__(self, path_to_settings):
        from PyQt6.QtGui import QIcon
        from data.QObjects import PushButton
        from data.ButtonLanguage import ButtonLanguage

        super().__init__(QIcon(r'data\images\icon_1.ico'), 'Translate')
        self.path_to_settings, self.font_family = path_to_settings, r'data\font\AcromThin.ttf'
        self.background, self.translate_label = tuple(Label(self, font_family=self.font_family) for _ in range(2))
        self.translate_button, self.full_answer = tuple(PushButton(self) for _ in range(2))
        self.number, self.system_1, self.system_2 = tuple(
            TextEdit(
                self,
                font_family=self.font_family,
                font_size=17,
                size=size
            ) for size in [(231, 270, 161, 31), (442, 269, 61, 31), (572, 269, 61, 31)]
        )
        self.language = ButtonLanguage(self, path_to_settings=self.path_to_settings)
        self.check_translate = False
        self.main_part()

    def main_part(self):
        from PyQt6.QtCore import QRect
        from PyQt6.QtGui import QIcon
        from file_actions import get_attribute

        theme, language = tuple(
            [get_attribute(path_to_file=self.path_to_settings, name_attribute=name) for name in ['theme', 'language']]
        )
        self.background.setImage(path_to_image='\\'.join(['data', 'images', f'Translate_{theme}_{language}.jpg']))
        self.translate_label.setGeometry(QRect(135, 330, 700, 35))
        self.translate_button.setRect(340, 380, 151, 41)
        self.translate_button.clicked.connect(self.translate_system)
        self.full_answer.setRect(650, 330, 20, 20)
        self.full_answer.setVisible(False)
        self.full_answer.setIcon(QIcon('data/images/full_answer.png'))
        self.full_answer.clicked.connect(self.full_answer_window)
        for number in [self.number, self.system_1, self.system_2]:
            number.addStyleSheet('background-color: rgba(0, 0, 0, 0);')
            number.setReadOnly(False)
        self.language.clicked.connect(
            lambda: new_language(self.path_to_settings, self.language, self.background, 'Translate')
        )
        self.show()

    def keyPressEvent(self, e):
        from PyQt6.QtCore import Qt

        match e.key():
            case Qt.Key.Key_B:
                self.main_window()
            case Qt.Key.Key_R:
                new_theme(self.path_to_settings, self.background, 'Translate')
            case Qt.Key.Key_Escape:
                self.close()

    def translate_system(self):
        from file_actions import get_attribute

        lang = get_attribute(path_to_file=self.path_to_settings, name_attribute='language')
        if self.number.toPlainText() != '' and self.system_1.toPlainText() != '' and self.system_2.toPlainText() != '':
            from data.operations_with_systems import number_systems, saving_the_translation

            number, system_1 = self.number.toPlainText(), self.system_1.toPlainText()
            system_2 = self.system_2.toPlainText()
            result = number_systems(
                number,
                system_1,
                system_2,
                lang
            )
            self.translate_label.setText(result)
            self.full_answer.setVisible(True)
            saving_the_translation(
                path_to_dir=get_attribute(path_to_file=self.path_to_settings, name_attribute='saves'),
                translation_history=number_systems(
                    number=self.number.toPlainText(),
                    system_1=self.system_1.toPlainText(),
                    system_2=self.system_2.toPlainText(),
                    lang=lang,
                    full_answer=True
                )
            )
        else:
            from data.translator import translator

            if (self.number.toPlainText() == '' and self.system_1.toPlainText() == '' and
                    self.system_2.toPlainText() == ''):
                self.translate_label.setText(
                    translator(
                        russian="Вы ничего не ввели!",
                        english="You haven't entered anything!",
                        lang=lang
                    )
                )
            else:
                self.full_answer.setVisible(False)
                if self.number.toPlainText() == '':
                    self.translate_label.setText(
                        translator(
                            russian='Вы не ввели число, которое нужно перевести в другую систему\nсчисления!',
                            english='You have not entered a number that needs to be converted to another number '
                                    'system!',
                            lang=lang
                        )
                    )
                elif self.system_1.toPlainText() == '':
                    self.translate_label.setText(
                        translator(
                            russian='Вы не ввели систему счисления, в которой находится число!',
                            english='You have not entered the number system in which the number is located!',
                            lang=lang
                        )
                    )
                elif self.system_2.toPlainText() == '':
                    self.translate_label.setText(
                        translator(
                            russian='Вы не ввели систему счисления, в которую нужно перевести число!',
                            english='You have not entered the number system into which you need to translate the '
                                    'number!',
                            lang=lang
                        )
                    )

    @pyqtSlot()
    def main_window(self):
        from file_actions import get_attribute

        if get_attribute(path_to_file=self.path_to_settings, name_attribute='main_body') == '1':
            self.main_body = FirstMainWindow(self.path_to_settings)
        else:
            self.main_body = SecondMainWindow(self.path_to_settings)
        self.main_body.show()
        self.close()

    @pyqtSlot()
    def full_answer_window(self):
        self.window_full_answer = FullAnswer(
            self.path_to_settings,
            self.number.toPlainText(),
            self.system_1.toPlainText(),
            self.system_2.toPlainText()
        )
        self.window_full_answer.show()


# The FullAnswer class inherits from the Widget class. Based on the data obtained, it displays the theoretical part and
# a detailed solution on the window.
class FullAnswer(Widget):
    def __init__(self, path_to_settings: str, *last_translate: str):
        from PyQt6.QtGui import QIcon

        super().__init__(QIcon(r'data\images\icon_2.ico'), 'Full Answer')
        self.path_to_settings, self.font_family = path_to_settings, r'data\font\AcromThin.ttf'
        self.number, self.system_1, self.system_2 = last_translate
        self.background = Label(self)
        self.theory, self.full_answer = tuple(
            TextEdit(
                self,
                font_family=r'data\font\AcromThin.ttf',
                size=size
            ) for size in [(10, 10, 430, 140), (10, 170, 430, 180)]
        )
        self.main_part()

    def main_part(self):
        from PyQt6.QtCore import QRect
        from file_actions import get_attribute
        from data.translator import translator
        from data.operations_with_systems import number_systems

        self.setFixedSize(450, 350)
        self.background.setGeometry(QRect(0, 0, 450, 350))
        theme = get_attribute(path_to_file=self.path_to_settings, name_attribute="theme")
        language = get_attribute(path_to_file=self.path_to_settings, name_attribute='language')
        self.background.setStyleSheet(
            f'background-color: {"White" if theme == "White" else "rgb(32, 38, 54)"};'
        )
        for block in [self.theory, self.full_answer]:
            block.addStyleSheet('background-color: rgba(0, 0, 0, 0);')
        if self.system_1 == '10':
            self.theory.setText(
                translator(
                    russian=(
                        '   Чтобы перевести десятичное число в систему счисления с другим основанием, нужно это '
                        'число разделить на основание. Полученное частное снова разделить на основание, и '
                        'дальше до тех пор, пока частное не окажется меньше основания. В результате записать '
                        'в одну строку последнее частное и все остатки, начиная с последнего.'
                    ),
                    english=(
                        '   To convert a decimal number to a number system with a different base, you need to divide '
                        'this number by the base. The resulting quotient is again divided into the base, and '
                        'further until the quotient is less than the base. As a result, write the last quotient '
                        'and all the residuals starting from the last one in one line.'
                    ),
                    lang=language
                )
            )
        elif self.system_2 == '10':
            self.theory.setText(
                translator(
                    russian=(
                        '   Для перевода в десятичную систему, требуется разбить число на цифры, затем умножаешь их на '
                        'основание системы счисления данного числа, возведенное в степень позиции цифры в '
                        'числе. Позиция цифры определяется справа налево, начиная с нуля.'
                    ),
                    english=(
                        '   To convert to the decimal system, you divide the number into digits, then multiply them '
                        'by the base of the number system of this number, raised to the power of the digit position '
                        'in the number. The position of the digit is determined from right to left starting from zero.'
                    ),
                    lang=language
                )
            )
        elif self.system_1 != '10' and self.system_2 != '10':
            self.theory.setText(
                translator(
                    russian=(
                        '   Для перевода какого либо числа из одной системы счисления в другую, проще всего '
                        'сначала перевести данное число в десятичную систему, затем из десятичной - в какую '
                        'требуется.'
                    ),
                    english=(
                        '   To convert a number from one number system to another, the easiest way is to first '
                        'translate this number into the decimal system, then from the decimal system to what is '
                        'required.'
                    ),
                    lang=language
                )
            )
        self.full_answer.setText(number_systems(self.number, self.system_1, self.system_2, language, True))

    def keyPressEvent(self, e):
        from PyQt6.QtCore import Qt

        if e.key() in [Qt.Key.Key_Enter, Qt.Key.Key_Escape]:
            self.close()


def applications(path_to_settings: str):
    from file_actions import get_attribute
    from PyQt6.QtWidgets import QApplication
    from sys import argv, exit

    app = QApplication(argv)
    if get_attribute(path_to_file=path_to_settings, name_attribute='input_text') == 'True':
        ex = Introduction(path_to_settings)
    else:
        main_body = get_attribute(path_to_file=path_to_settings, name_attribute='main_body')
        ex = FirstMainWindow(path_to_settings) if main_body == '1' else SecondMainWindow(path_to_settings)
    exit(app.exec())


def main():
    # from installing_libraries import installing_libraries

    path_to_settings = r'data\settings'
    # installing_libraries(path=path_to_settings, libraries=['PyQt6', 'pyqt-tools', 'python-docx'])
    applications(path_to_settings)


if __name__ == '__main__':
    main()
