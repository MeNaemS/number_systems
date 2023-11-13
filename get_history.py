# The get_files function takes as a parameter the variable path_to_dir of string type, which stores the path to the
# directory with saves. The subroutine returns all files with the *.docx extension stored in the specified directory.
def get_files(path_to_dir: str) -> list:
    from os import listdir

    files = []
    for file in listdir(path=path_to_dir):
        if file.endswith('.docx'): files.append(file)
    return files


# The read_document function takes as parameters the variables path_to_file of the string type, which stores the path
# to the *.docx file with the translation history, lang of the string type, which stores the language for displaying
# information. If there is no history in the *.docx file, then the subroutine will display that there is no translation
# history, otherwise it will display the text stored in the file.
def read_document(path_to_file: str, lang: str) -> str:
    from docx import Document
    from docx.opc.exceptions import PackageNotFoundError

    try:
        document = Document(docx=path_to_file)
        return '\n------\n'.join([paragraph.text for paragraph in document.paragraphs])
    except PackageNotFoundError:
        return 'У вас нет истории переводов.' if lang == 'ru' else 'You don\'t have a history of translations.'


# The get_last_file function takes as a parameter a string variable path_to_dir, which stores the path to the save
# directory. The routine finds the last file created and returns it.
def get_last_file(path_to_dir: str) -> str:
    from os.path import getctime
    from os import listdir

    files = listdir(path=path_to_dir)
    date_of_files = [getctime(f'{path_to_dir}/{path}') for path in files]
    return files[date_of_files.index(max(date_of_files))]


# The get_gistory function takes as a parameter the path_to_settings variable, which contains the path to the settings.
# The subroutine checks the presence of a directory for saving using the check_directory function, receives a list of
# files stored in this directory using the get_files function, if there are files, then the subroutine will display the
# last file using the get_last_file function, otherwise, the subroutine will check all former directories stored in the
# settings and It will also display the last file, if it is there, otherwise, the subroutine will display information
# about the absence of a translation history.
def get_history(path_to_settings: str) -> str:
    from file_actions import get_attribute
    from file_actions import check_directory

    PATH_TO_FILE: str = path_to_settings
    path = get_attribute(path_to_file=PATH_TO_FILE, name_attribute='saves')
    lang = get_attribute(path_to_file=PATH_TO_FILE, name_attribute='language')
    check_dir = check_directory(path, lang)
    if check_dir[0]:
        from data.translator import translator

        NONE_OUTPUT: str = translator(
            russian='У вас нет истории переводов.',
            english='You don\'t have a history of translations.',
            lang=lang
        )
        docx_files = get_files(path_to_dir=path)
        if docx_files:
            return read_document(path_to_file=f'{path}/{get_last_file(path)}', lang=lang)
        else:
            paths = get_attribute(path_to_file=PATH_TO_FILE, name_attribute='other_paths')
            if paths != '':
                paths = [path for path in paths.split(', ')]
                for path in range(len(paths)):
                    if get_files(path_to_dir=paths[path]):
                        return read_document(path_to_file=f'{paths[path]}/{get_last_file(paths[path])}', lang=lang)
                return NONE_OUTPUT
            else:
                return NONE_OUTPUT
    else:
        return check_dir[1]
