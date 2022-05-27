
class Feedback():


    def __init__(self, name,email,service,website,additional):
        self.__name=name
        self.__email=email
        self.__service=service
        self.__website=website
        self.__additional=additional
        self.__date=''
        self.__status=''


    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_service(self):
        return self.__service
    def get_website(self):
        return self.__website
    def get_additional(self):
        return self.__additional
    def get_status(self):
        return self.__status
    def get_date(self):
        return self.__date

    def set_name(self,name):
        self.__name=name
    def set_email(self,email):
        self.__email=email
    def set_service(self,service):
        self.__service=service
    def set_website(self,website):
        self.__website=website
    def set_additional(self,additional):
        self.__additional=additional
    def set_status(self,status):
        self.__status=status
    def set_date(self,date):
        self.__date=date