import re

# этот кусочек кода надо вставить в основной код, где описываются классы
# здесь создан класс email с проверкой данных на валидность


class Email(Field):
    def __init__(self, email):
        self.value = email

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_email):
        SAN_EMAIL = r'[a-zA-Z][a-zA-Z1-9._]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,}\b'
        if not re.search(SAN_EMAIL, str(new_email)):
            raise ValueError(
                f'This email "{new_email}" is not correct.\n')
        else:
            self.__value = new_email
