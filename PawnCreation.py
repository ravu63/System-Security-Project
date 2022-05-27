class Pawn_Creation:
    count_id = 0

    def __init__(self, firstname, lastname, nric, contactnumber, email, address, itemname, Descriptionofitem, Category,
                 ItemCondition, offer_price, pawn_period,SUI,pawnstatus):
        Pawn_Creation.count_id += 1
        self.__item_id = Pawn_Creation.count_id
        self.__firstname = firstname
        self.__lastname = lastname
        self.__nric = nric
        self.__contactnumber = contactnumber
        self.__email = email
        self.__address = address
        self.__itemname = itemname
        self.__Descriptionofitem = Descriptionofitem
        self.__category = Category
        self.__ItemCondition = ItemCondition
        self.__offer_price = offer_price
        self.__pawn_period = pawn_period
        self.__SUI = SUI
        self.__pawnstatus = pawnstatus

    def set_status(self,pawnstatus):
        self.__pawnstatus = pawnstatus

    def get_pawnstatus(self):
        return self.__pawnstatus

        
    def set_SUI(self,SUI):
        self.__SUI = SUI

    def get_SUI(self):
        return self.__SUI

    def set_item_id(self, item_id):
        self.__item_id = item_id

    def get_item_id(self):
        return self.__item_id

    def set_firstname(self, firstname):
        self.__firstname = firstname

    def get_firstname(self):
        return self.__firstname

    def set_lastname(self, lastname):
        self.__lastname = lastname

    def get_lastname(self):
        return self.__lastname

    def set_nric(self, nric):
        self.__nric = nric

    def get_nric(self):
        return self.__nric

    def set_contactnumber(self, contactnumber):
        self.__contactnumber = contactnumber

    def get_contactnumber(self):
        return self.__contactnumber

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_address(self, address):
        self.__address = address

    def get_address(self):
        return self.__address

    def set_itemname(self, itemname):
        self.__itemname = itemname

    def get_itemname(self):
        return self.__itemname

    def set_Descriptionofitem(self, Descriptionofitem):
        self.__Descriptionofitem = Descriptionofitem

    def get_Descriptionofitem(self):
        return self.__Descriptionofitem

    def set_category(self, category):
        self.__category = category

    def get_category(self):
        return self.__category

    def set_ItemCondition(self, ItemCondition):
        self.__ItemCondition = ItemCondition

    def get_ItemCondition(self):
        return self.__ItemCondition

    def set_offer_price(self, offer_price):
        self.__offer_price = offer_price

    def get_offer_price(self):
        return self.__offer_price

    def set_pawn_period(self, pawn_period):
        self.__pawn_period = pawn_period

    def get_pawn_period(self):
        return self.__pawn_period

