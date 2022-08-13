class Feedback1():
    def __init__(self, name,contactnumber,email,currency):
        self.__name=name
        self.__contactnumber=contactnumber
        self.__email=email
        self.__currency=currency



    def get_name(self):
        return self.__name
    def get_contactnumber(self):
        return self.__contactnumber
    def get_email(self):
        return self.__email

    def get_currency(self):
        return self.__currency

    def set_name(self,name):
        self.__name=name

    def set_contactnumber(self,contactnumber):
        self.__contactnumber=contactnumber

    def set_email(self,email):
        self.__email=email

    def set_currency(self,currency):
        self.__currency=currency

