from   hashlib import sha256
import User
class Customer(User.User):

    def __init__(self, name,gender,phone,birthdate,email,password):
        super().__init__(name,gender,phone,birthdate)
        self.__email=email
        self.__password = sha256(password.encode("utf8")).hexdigest()
        self.__role = 1







    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_role(self):
        return self.__role





    def set_email(self,email):
        self.__email=email

    def set_password(self,password):
        self.__password = sha256(password.encode("utf8")).hexdigest()

    def check_password(self, password: str):
        return self.__password == sha256(password.encode("utf8")).hexdigest()

    def set_role(self,role):
        self.__role=role


