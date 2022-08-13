class Plan:
    count_id = 0

    # Loan init
    def __init__(self, plan_name, plan_description, plan_interest):
        Plan.count_id += 1
        self.__PlanId = Plan.count_id
        self.__Plan_name = plan_name
        self.__Plan_description = plan_description
        self.__Plan_interest = plan_interest

    # Plan getter method

    def get_loan_plan_id(self):
        return self.__PlanId

    def get_loan_plan_name(self):
        return self.__Plan_name

    def get_loan_plan_desc(self):
        return self.__Plan_description

    def get_loan_plan_int(self):
        return self.__Plan_interest

    # Plan setter method

    def set_loan_plan_id(self, id):
        self.__PlanId = id
        return self.__PlanId

    def set_loan_plan_name(self, name):
        self.__Plan_name = name
        return self.__Plan_name

    def set_loan_plan_desc(self, desc):
        self.__Plan_description = desc
        return self.__Plan_description

    def set_loan_plan_int(self, int):
        self.__Plan_interest = int
        return self.__Plan_interest
