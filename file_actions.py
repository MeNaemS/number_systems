from typing import Union


# The create_settings_file function takes a string variable path_to_file as a parameter, which stores the desired path
# to the settings file. If the settings file is not found at the specified path, the file is overwritten and filled
# with the original information in UTF-8 encoding.
def create_settings_file(path_to_file: str):
    from os.path import exists

    if not exists(path=path_to_file):
        with open(path_to_file, 'w', encoding='utf-8') as file:
            file.writelines([
                'theme—White\n',
                'saves—history\n',
                'other_paths—\n',
                'main_body—1\n',
                'settings_body—1\n',
                'input_text—True\n',
                'language—ru\n',
                'last_update—'
            ])


# The check_directory function takes as parameters the variables path of a string type, which stores the path to the
# folder with saves, and lang of a string type, which stores the language for displaying information. The function
# checks for the presence of the required data folder, which must be located in the same folder as the main.py
# file; if it is not there, the program will display an error and ask the user to reinstall the program. If the data
# folder exists, then the function will check for the presence of a folder with history at the specified path, if there
# is no folder or the path is not complete, then the function will create all the missing directories and return the
# text about the absence of history, otherwise, the function will display that there is a folder with history along the
# specified path.
def check_directory(path: str, lang: str) -> tuple[list, Union[str, None]]:
    from os.path import exists

    if exists(path='data'):
        from os import makedirs

        if not exists(path=path):
            from data.translator import translator

            makedirs(name=path)
            return False, translator(
                russian='У вас нет истории переводов.',
                english='You don\'t have a history of translations.',
                lang=lang
            )
        else:
            return True, None
    else:
        raise Exception('Sorry, but you deleted the data folder, which is necessary for the program to work. Please '
                        'reinstall the program folder.')


# The get_attribute function takes as parameters the variables path_to_file of the string type, which stores the path
# to the file with the settings, name_attribute of the string type, which stores the name of the attribute in which a
# certain value is stored. The function checks for the existence of a settings file by calling the create_settings_file
# function, and then reads data from the file and returns the value of the specified attribute.
def get_attribute(path_to_file: str, name_attribute: str) -> str:
    create_settings_file(path_to_file)
    with open(file=path_to_file, mode='r', encoding='utf-8') as file:
        text = dict([tuple(element.split('—')) for element in file.read().splitlines()])
    return text[name_attribute]


# The set_attribute function takes as parameters the variables path_to_file of the string type, which stores the path
# to the file with the settings, name_attribute of the string type, which stores the name of the attribute in which a
# certain value is stored, new_value of the string type, which stores the new value for the specified attribute. The
# function checks for the presence of a settings file by calling the create_settings_file function, reads data from the
# file, checks for the presence of the attribute and changes its value. If the attribute is 'saves', then the function
# will also change the value of the 'other_paths' attribute.
def set_attribute(path_to_file: str, name_attribute: str, new_value: str):
    create_settings_file(path_to_file)
    with open(file=path_to_file, mode='r', encoding='utf-8') as file:
        values = dict([element.split('—') for element in file.read().splitlines()])
    if name_attribute in values:
        if name_attribute == 'saves':
            if values['other_paths'] == '':
                values = values | {'other_paths': values[name_attribute]}
            else:
                values = values | {'other_paths': f'{values[name_attribute]}, {values["other_paths"]}'}
        values = values | {name_attribute: new_value}
        values = [list(value) for value in values.items()]
        with open(file=path_to_file, mode='w', encoding='utf-8') as file:
            file.write('\n'.join(['—'.join(value) for value in values]))
    else:
        raise Exception('There is no given key in the dictionary!')


# The create_introduction function takes as a parameter a string variable path, which will indicate the path to the
# file with the introduction. The subroutine creates a file at the specified path and fills it with information for
# introduction, dividing it into 2 languages, divided into 2 paragraphs.
def create_introduction(path: str):
    with open(file=path, mode='w', encoding='utf-8') as file:
        text = [
            [
                [
                    'Приложение изначально планировалось как калькулятор для перевода из',
                    'одной системы счисления в другую. В процессе оно будет улучшаться,',
                    'будут новый функции, изменяться некоторые недочеты, а также оптимизироваться.',
                    'Пока в приложении можно только перевести число из одной системы счисления',
                    'в другую, но планируется еще добавить вычисление синусов, косинусов,',
                    'тангенсов, котангенсов, необходимую теоретическую часть и поэтапную',
                    'помощь.'
                ],
                [
                    'The application was originally planned as a calculator for transferring',
                    'from one number system to another. In the process, it will be improved,',
                    'new functions will be added, some shortcomings will be changed, as well',
                    'as optimized. So far, the application can only translate a number from',
                    'one number system to another, but it is also planned to add the',
                    'calculation of sines, cosines, tangents, cotangents, the necessary',
                    'theoretical part and step-by-step assistance.'
                ]
            ],
            [
                [
                    'Пока пользователю доступны такие функции, как:',
                    '"Настройки" — в них можно изменить путь сохранения, изменить',
                    'тему (также тему можно изменить сочитанием Ctrl + R), вернуться назад,',
                    '"Калькулятор" — перевести число из одной системы счисления в другую, а также',
                    'получить теоретическую часть и поэтапное объяснение. Чтобы',
                    'перейти к самому переводу из одной системы счисления в другую,',
                    'необходимо нажать клавиши Ctrl +  F. Перейти назад можно, нажав на клавиши Ctrl + B. Также',
                    'выйти из приложения можно, нажав на клавишу Esc. Чтобы перейти к',
                    'главной странице, требуется нажать пробел. Вернуться назад к вводному окну',
                    'можно, нажав на кнопку "О проекте" или "About".'
                ],
                [
                    'While the user has access to such functions as: "Settings" — in them you',
                    'can change the save path, change the theme (you can also change the theme',
                    'by pressing Ctrl + R), go back, "Calculator" — translate a number from one',
                    'number system to another, as well as get the theoretical part and a',
                    'step-by-step explanation. To switch to the translation itself from one',
                    'number system to another, you need to press Ctrl + F. You can go back by',
                    'pressing Ctrl+ B. You can also exit the application by pressing the',
                    'Esc key. To go to the main page, you need to press the space bar. You can',
                    'go back to the introductory window by clicking on the "About project" or',
                    '"About" button.'
                ]
            ]
        ]
        replaced_text = ''
        for i in range(len(text)):
            replaced_text += '\n\n'.join(['\n'.join(text[i][j]) for j in range(len(text[i]))])
            if i < len(text) - 1: replaced_text += '\n\n\n'
        file.write(replaced_text)


# The get_introduction function takes as parameters the variables path_to_file of a string type, storing the path to
# the file, paragraph of a string or integer type, storing the number of the paragraph to be returned, lang of a string
# type, storing the language in which information from the file should be returned . The subroutine creates an
# "Introduction" file, if it does not exist, using the create_introduction function, reads information from it, then
# returns text in the specified language with the specified paragraph.
def get_introduction(path_to_file: str, paragraph: Union[int, str], lang: str) -> str:
    from os.path import exists

    if not exists(path=path_to_file):
        create_introduction(path_to_file)
    with open(file=path_to_file, mode='r', encoding='utf-8') as file:
        file = file.read().split('\n\n\n')[paragraph - 1]
        lang = 1 if lang == 'en' else 0
    return file.split('\n\n')[lang].replace('\n', ' ')
