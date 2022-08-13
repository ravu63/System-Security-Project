class User:

    def __init__(self, name, gender, phone,birthdate):
        self.__name = name
        self.__gender = gender
        self.__phone = phone
        self.__birthdate=birthdate


    def get_name(self):
        return self.__name

    def get_gender(self):
        return self.__gender

    def get_phone(self):
        return self.__phone

    def get_birthdate(self):
        return self.__birthdate



    def set_name(self, name):
        self.__name = name


    def set_gender(self, gender):
        self.__gender = gender

    def set_phone(self, phone):
        self.__phone= phone

    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate
