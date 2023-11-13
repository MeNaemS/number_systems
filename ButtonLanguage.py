from data.QObjects import PushButton


# The ButtonLanguage class inherits from the PushButton class. Sets the position of the button, its style, and also
# simplifies changing the application language using the rewrite_language method.
class ButtonLanguage(PushButton):
    def __init__(self, *args, path_to_settings: str):
        from file_actions import get_attribute
        from PyQt6.QtGui import QIcon

        super().__init__(*args)
        self.path_to_settings = path_to_settings
        self.settings_of_language = get_attribute(path_to_file=self.path_to_settings, name_attribute='language')
        self.setRect(750, 20, 20, 20)
        self.setIcon(QIcon('\\'.join(['data', 'images', f'{self.settings_of_language}_icon.ico'])))

    def rewrite_language(self):
        from file_actions import set_attribute, get_attribute
        from PyQt6.QtGui import QIcon

        self.settings_of_language = 'ru' if self.settings_of_language == 'en' else 'en'
        set_attribute(
            path_to_file=self.path_to_settings,
            name_attribute='language',
            new_value=self.settings_of_language
        )
        self.setIcon(QIcon('\\'.join(['data', 'images', f'{self.settings_of_language}_icon.ico'])))
