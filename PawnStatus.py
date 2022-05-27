import PawnCreation


class Pawn_Status(PawnCreation.Pawn_Creation):
    def __init__(self, firstname, lastname, nric, contactnumber, email, address, itemname, Descriptionofitem, Category,
                 ItemCondition, offer_price, pawn_period,SUI, status):
        PawnCreation.Pawn_Creation.__init__(self, firstname, lastname, nric, contactnumber, email, address, itemname,
                                           Descriptionofitem, Category,
                                           ItemCondition, offer_price,SUI, pawn_period)
        self.__status = status


    def set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status
