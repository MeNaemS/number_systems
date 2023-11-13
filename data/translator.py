# The translator function takes as parameters the variables russian of the string type, which stores text in Russian,
# english of the string type, which stores the text in English, and lang of the string type, which stores the language
# for displaying information. The subroutine displays text in one of two languages.
def translator(russian: str, english: str, lang: str) -> str:
    match lang:
        case 'ru':
            return russian
        case 'en':
            return english
        case _:
            raise Exception('Unknown language.')
