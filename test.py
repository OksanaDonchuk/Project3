import re

def value(new_email):
    SAN_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.search(SAN_EMAIL, str(new_email)):
        raise ValueError(
            f'This email "{new_email}" is not correct.\n')
    else:
        print('correct')


value('doqweqweg@gmail.com')