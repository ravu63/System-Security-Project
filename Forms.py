from wtforms import Form, StringField, validators, PasswordField, SelectField, ValidationError, TextAreaField
from wtforms.fields import EmailField, DateField, FileField, IntegerField, RadioField, SearchField,SubmitField


class LoginForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired()])


class CreateCustomerForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    phone = StringField('Phone', [validators.Length(min=8, max=8), validators.DataRequired()])
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired(),
                                          validators.EqualTo('confirmpassword', message='Error:Passwords must match')])
    confirmpassword = PasswordField('Confirm Password', [validators.DataRequired()])
    submit=SubmitField('Register')
    def validate_phone(self, phone):
        if not phone.data[1:8].isdigit():
            raise ValidationError("Phone number must not contain letters")
    def validate_email(self,email):
        existing_user_email=User.query.filter.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError('Account already exists.')


class SearchCustomerForm(Form):
    searchCustomer = StringField('Search Customer', [validators.DataRequired()])


class UpdateCustomerForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    phone = StringField('Phone', [validators.Length(min=8, max=8), validators.DataRequired()])
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])

    def validate_phone(self, phone):
        if not phone.data[1:8].isdigit():
            raise ValidationError("Phone number must not contain letters")


class FeedbackForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    service = SelectField('Rate our Service', [validators.DataRequired()],
                          choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                          default='')
    website = SelectField('Rate our Website', [validators.DataRequired()],
                          choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                          default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    additional = TextAreaField('Additional feedback')


class UpdateCustomerForm2(Form):
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired(),
                                          validators.EqualTo('confirmpassword', message='Error:Passwords must match')])
    confirmpassword = PasswordField('Confirm Password', [validators.DataRequired()])


class UpdateStatus(Form):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()],
                       render_kw={'readonly': True})
    service = SelectField('Rate our Service', [validators.DataRequired()],
                          choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                          default='', render_kw={'readonly': True})
    website = SelectField('Rate our Website', [validators.DataRequired()],
                          choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                          default='', render_kw={'readonly': True})
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={'readonly': True})
    additional = TextAreaField('Additional feedback', render_kw={'readonly': True})
    date = DateField('Date of Creation', format='%Y-%m-%d', render_kw={'readonly': True})
    status = SelectField('Status', [validators.DataRequired()],
                         choices=[('Processing', 'Processing'), ('Processed', 'Processed')],
                         default='Processing')


class ForgetPassword(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])


class OTPform(Form):
    otp = StringField('OTP', [validators.DataRequired()])


class ChangePassword(Form):
    password = PasswordField('Password', [validators.EqualTo('confirmpassword', message='Error:Passwords must match')])
    confirmpassword = PasswordField('Confirm Password')


# START OF LOAN FORMS

class CreateLoanForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    Amount = IntegerField('Amount $', [validators.NumberRange(min=1, max=999999), validators.DataRequired()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])

    def validate_amount(self, Amount):
        if Amount.data > 9999:
            raise ValidationError("Amount must not exceed 999999 SGD")
        if Amount.data is not int():
            raise ValidationError("Amount must not contain Letters")



class CreatePlanForm(Form):
    Plan_name = StringField('Plan Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    Plan_Des = StringField('Plan Description', [validators.Length(min=1, max=300), validators.DataRequired()])
    Plan_interest = IntegerField('Interest', [validators.NumberRange(min=1, max=100), validators.DataRequired()])
    # Plan_image = FileField('Profile', validators=[flask_wtf.file.FileRequired(),
    # flask_wtf.file.FileAllowed(['jpg', 'png'], 'Images only!')])


class SearchLoanForm(Form):
    Loan_search = SearchField('Enter Loan Id', [validators.Length(min=1, max=7), validators.DataRequired])


# END OF LOAN FORMS

# Start of Ravu Froms
class PawnCreation(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    nric = StringField('NRIC', [validators.Length(min=9, max=9), validators.DataRequired()])
    contactnumber = StringField('Contact Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    itemname = StringField('Name of Item', [validators.Length(min=1, max=150), validators.DataRequired()])
    Descriptionofitem = TextAreaField('Description of Item', [validators.length(max=200), validators.DataRequired()])
    Category = SelectField('Category', [validators.DataRequired()],
                           choices=[('', 'Select'), ('Jewelry', 'Jewelry'), ('Electronics', 'Electronics'),
                                    ('Musical Instruments', 'Musical Instruments'), ('Watch', 'Watch'),
                                    ('Antiques', 'Antiques'), ('Others', 'Others')], default='')
    ItemCondition = SelectField('ItemCondition', [validators.DataRequired()],
                                choices=[('', 'Select'), ('Heavily Used', 'Heavily Used'),
                                         ('Lightly Used', 'Lightly Used'),
                                         ('Like New', 'Like New'), ('New', 'New')], default='')
    offer_price = StringField('Offer Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    pawn_period = StringField('Pawn Period(Month)', [validators.Length(min=1, max=150), validators.DataRequired()])

    def validate_nric(form, nric):
        if not nric.data[0].isalpha():
            raise ValidationError("IC must start with S or T")
        if not nric.data[1:7].isdigit():
            raise ValidationError("IC needs to have 7 digits in between 2 letters")
        if not nric.data[-1].isalpha():
            raise ValidationError("IC must end with an alphabet")

    def validate_contactnumber(form, contactnumber):
        if not contactnumber.data.isdigit():
            raise ValidationError("Your number should be in digits")


class PawnStatus(Form):
    pawn_status = SelectField('Pawn Status', [validators.DataRequired()],
                              choices=[('Processing', 'Processing'), ('Picked Up', 'Picked Up'),
                                       ('Delivered', 'Delivered'),
                                       ('Inspection', 'Inspection'), ('Offer Accepted', 'Offer Accepted'),
                                       ('Rejected', 'Rejected'), ('Successful', 'Successful')], default='Processing')


class PawnRetrieval(Form):
    SUI_CODE = StringField('Enter in the SUI:', [validators.Length(min=1, max=9), validators.DataRequired()])


class SearchSUI(Form):
    SUI_CODE = StringField('Enter in the SUI:', [validators.Length(min=1, max=9), validators.DataRequired()])


class filterStatus(Form):
    pawn_status = SelectField('Filter by Status:', [validators.DataRequired()],
                              choices=[('', 'Select'), ('Processing', 'Processing'), ('Picked Up', 'Picked Up'),
                                       ('Delivered', 'Delivered'),
                                       ('Inspection', 'Inspection'), ('Offer Accepted', 'Offer Accepted'),
                                       ('Rejected', 'Rejected'), ('Successful', 'Successful')], default='')

# End of Ravu

# Start of Ashton currency
class FeedbackForm1(Form):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    contnumb = StringField('Contact Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    requestyourcurrency = TextAreaField('Currency Requested', [validators.Optional()])

# End of Ashton currency