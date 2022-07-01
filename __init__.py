from currency_converter import CurrencyConverter
import Loan
import random
import string
import shelve
import Plan
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from Feedback1 import Feedback1
from Forms import  OTPform, \
     CreateLoanForm, CreatePlanForm, PawnCreation, \
    PawnStatus, \
    PawnRetrieval, SearchSUI, filterStatus, FeedbackForm1
from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SelectField, TextAreaField, \
    SubmitField
from wtforms.fields import EmailField, DateField
from wtforms.validators import ValidationError
from transaction import CustomerPurchase
from Currency import Currency
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_bcrypt import Bcrypt
from captcha_generate import generate_captcha_image
from datetime import datetime, date
import pytz
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

s=URLSafeTimedSerializer('ThisIsASecret!')
app = Flask(__name__)
app.debug = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "radiantfinancenyp@gmail.com"
app.config['MAIL_PASSWORD'] = "xepjuxdlrsmpcnxk"
mail = Mail(app)
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


# Start of database

# Create table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    phone = db.Column(db.String(8), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    passwordChange = db.Column(db.Date, nullable=False)


class Pawn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    nric = db.Column(db.String(9), nullable=False)
    contact_number = db.Column(db.String(8), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    ItemCondition = db.Column(db.String(30), nullable=False)
    offer_price = db.Column(db.String(30), nullable=False)
    period = db.Column(db.String(10), nullable=False)
    sui = db.Column(db.String(10), nullable=False)
    pawn_status = db.Column(db.String(10), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(min=30,max=100), nullable=False)


# end Create table

# End of Database

# Start of Forms
# Joshua
class CreateCustomerForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    phone = StringField('Phone', [validators.Length(min=8, max=8), validators.DataRequired()])
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired(),
                                          validators.EqualTo('confirmpassword', message='Error:Passwords must match')]
                             )
    confirmpassword = PasswordField('Confirm Password', [validators.DataRequired()])
    submit = SubmitField('Register')

    def validate_phone(self, phone):
        if not phone.data[1:8].isdigit():
            raise ValidationError("Phone number must not contain letters")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError(flash(u'User exists'))


class LoginForm(FlaskForm):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired()])
    submit = SubmitField('Login')


class UpdateCustomerForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],choices=[('F', 'Female'), ('M', 'Male')], default='')
    phone = StringField('Phone', [validators.Length(min=8, max=8), validators.DataRequired()])
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    submit = SubmitField('Update')

    def validate_phone(self, phone):
        if not phone.data[1:8].isdigit():
            raise ValidationError("Phone number must not contain letters")

class ForgetPassword(FlaskForm):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    submit = SubmitField('Submit')

class UpdateCustomerForm2(FlaskForm):
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired(),
                                          validators.EqualTo('confirmpassword', message='Error:Passwords must match')])
    confirmpassword = PasswordField('Confirm Password', [validators.DataRequired()])
    submit = SubmitField('Submit')

class UpdateCustomerForm3(FlaskForm):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    submit = SubmitField('Submit')




# End of Joshua
# Start of Ravu
class PawnCreation(FlaskForm):
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
    submit = SubmitField('Submit')

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


class PawnStatus(FlaskForm):
    pawn_status = SelectField('Pawn Status', [validators.DataRequired()],
                              choices=[('Processing', 'Processing'), ('Picked Up', 'Picked Up'),
                                       ('Delivered', 'Delivered'),
                                       ('Inspection', 'Inspection'), ('Offer Accepted', 'Offer Accepted'),
                                       ('Rejected', 'Rejected'), ('Successful', 'Successful')], default='Processing')
    submit = SubmitField('Submit')


class PawnRetrieval(FlaskForm):
    SUI_CODE = StringField('Enter in the SUI:', [validators.Length(min=1, max=9), validators.DataRequired()])
    submit = SubmitField('Submit')


class SearchSUI(FlaskForm):
    SUI_CODE = StringField('Enter in the SUI:', [validators.Length(min=1, max=9), validators.DataRequired()])
    submit = SubmitField('Submit')


class filterStatus(FlaskForm):
    pawn_status = SelectField('Filter by Status:', [validators.DataRequired()],
                              choices=[('', 'Select'), ('Processing', 'Processing'), ('Picked Up', 'Picked Up'),
                                       ('Delivered', 'Delivered'),
                                       ('Inspection', 'Inspection'), ('Offer Accepted', 'Offer Accepted'),
                                       ('Rejected', 'Rejected'), ('Successful', 'Successful')], default='')
    submit = SubmitField('Submit')


# End of Ravu


# End of  Forms



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.config['SECRET_KEY'] = 'mysecret'
app.static_folder = 'static'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    return render_template('main.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


# Joshua
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        current=date.today()
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            before = user.passwordChange
            diff = current - before

            if diff.days < 30:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    if diff.days>=25:
                        msg = Message('Password Expiring', sender='radiantfinancenyp@gmail.com',recipients=[user.email])
                        msg.body = 'Your password is expiring in {} days'.format(30-diff.days)
                        mail.send(msg)
                    if user.role == 0:
                        session['id']=user.id
                        session['role']=user.role
                        return redirect(url_for('main'))
                    else:
                        session['id'] = user.id
                        session['role']=user.role
                        return redirect(url_for('dashboard'))
                else:
                    flash(u'Invalid Email or Password')
            else:
                flash(u'Password has expired. Please change password.')
        else:
            flash(u'Invalid Email or Password')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = CreateCustomerForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        today = date.today()
        new_user = User(name=form.name.data, gender=form.gender.data, phone=form.phone.data,
                        birthdate=form.birthdate.data, email=form.email.data, password=hashed_password, role=0,
                        passwordChange=today)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/createAdmin', methods=['GET', 'POST'])
@login_required
def create_admin():
    form = CreateCustomerForm()
    role = session['role']
    if role != 1:
        return redirect(url_for('main'))
    elif role == 1:
        pass
    else:
        return redirect(url_for('main'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        today = date.today()
        new_user = User(name=form.name.data, gender=form.gender.data, phone=form.phone.data,
                        birthdate=form.birthdate.data, email=form.email.data, password=hashed_password, role=1, passwordChange=today)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('manage_admin'))
    return render_template('createAdmin.html', form=form)


@app.route('/manageCustomer', methods=['GET', 'POST'])
@login_required
def manage_customers():
    role = session['role']
    if role != 1:
        return redirect(url_for('main'))
    elif role == 1:
        pass
    else:
        return redirect(url_for('main'))
    return render_template('manageCustomer.html', Users=User.query.all())


@app.route('/manageAdmin', methods=['GET', 'POST'])
@login_required
def manage_admin():
    role = session['role']
    if role != 1:
        return redirect(url_for('main'))
    elif role == 1:
        pass
    else:
        return redirect(url_for('main'))
    return render_template('manageAdmin.html', Users=User.query.all())


@app.route('/updateAdmin/<id>/', methods=['GET', 'POST'])
@login_required
def customer_Admin(id):
    role = session['role']
    if role != 1:
        return redirect(url_for('main'))
    elif role == 1:
        pass
    else:
        return redirect(url_for('main'))
    form = UpdateCustomerForm()
    user = User.query.get_or_404(id)
    if request.method == 'POST' and form.validate_on_submit():
        user.name = request.form['name']
        user.email = request.form['email']
        birthdate = request.form['birthdate']
        user.birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
        user.phone = request.form['phone']
        user.gender = request.form['gender']
        db.session.commit()
        return redirect(url_for('manage_admin'))

    return render_template('updateAdmin.html', form=form, user=user)


@app.route('/deleteCustomer/<id>', methods=['POST'])
@login_required
def delete_customer(id):
    role = session['role']
    if role != 1:
        return redirect(url_for('main'))
    elif role == 1:
        pass
    else:
        return redirect(url_for('main'))
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('manage_customers'))


@app.route('/deleteAdmin/<id>', methods=['POST'])
@login_required
def delete_admin(id):
    role = session['role']
    if role != 1:
        return redirect(url_for('main'))
    elif role == 1:
        pass
    else:
        return redirect(url_for('main'))
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('manage_admin'))


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('id', None)
    logout_user()
    return redirect(url_for('home'))


@app.route('/forgotPassword', methods=['POST', 'GET'])
def forgot_password():
    form = ForgetPassword()
    try:
        if request.method == 'POST':
            email = User.query.filter_by(email=form.email.data).first()
            if email:
                emaildata = request.form['email']
                session['email'] = emaildata
                return redirect(url_for('getOTP'))
            else:
                flash(u'Invalid email provided')
    except:
        flash(u'Invalid email provided')

    return render_template('forgotPassword.html', form=form)


@app.route('/getOTP', methods=['POST', 'GET'])
def getOTP():
    if request.method == 'POST':
        otp = random.randint(1111, 9999)
        then = datetime.now()
        session['time'] = then
        session['otp'] = otp
        msg = Message('One Time Password', sender='radiantfinancenyp@gmail.com', recipients=[session['email']])
        msg.body = 'here is your OTP:{}'.format(otp)
        mail.send(msg)
        return redirect(url_for('OTP'))
    return render_template('getOTP.html')


@app.route('/OTP', methods=['POST', 'GET'])
def OTP():
    login_form = OTPform(request.form)
    then = session['time']
    if request.method == 'POST':
        otp = session['otp']
        otp2 = int(request.form['otp3'])
        if otp == otp2:
            now = datetime.now()
            utc = pytz.UTC
            now = utc.localize(now)
            current = (now - then).total_seconds()
            if current < 180:
                return redirect(url_for('change_password', id=id))
            else:
                flash(u'OTP has expired please retry again.')
        else:
            flash(u'Invalid OTP provided')
    return render_template('OTP.html', form=login_form)


@app.route('/changePassword', methods=['POST', 'GET'])
def change_password():
    form = UpdateCustomerForm2()
    id = session['email']
    user = User.query.filter_by(email=id).first()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        today = date.today()
        user.password = hashed_password
        user.passwordChange = today
        db.session.commit()
        session.pop('email', None)
        session.pop('otp', None)

        return redirect(url_for('login'))
    return render_template('customerChangePass.html', form=form)


@app.route('/manageAccount', methods=['GET', 'POST'])
@login_required
def manage_account():
    role = session['role']
    if role != 1 or role != 0:
        return redirect(url_for('main'))
    elif role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('main'))
    id = session['id']
    form = UpdateCustomerForm()
    user = User.query.get(id)
    if request.method == 'POST' and form.validate_on_submit():
        user.name = request.form['name']
        birthdate = request.form['birthdate']
        user.birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
        user.phone = request.form['phone']
        user.gender = request.form['gender']
        db.session.commit()

        return redirect(url_for('main'))

    return render_template('manageAccount.html', form=form,user=user)


@app.route('/changeEmail', methods=['GET', 'POST'])
@login_required
def email():
    role = session['role']
    if role != 1 or role != 0:
        return redirect(url_for('main'))
    elif role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('main'))
    id=session['id']
    user=User.query.get(id)
    email=user.email
    token =s.dumps(email)
    msg = Message('One Time Password', sender='radiantfinancenyp@gmail.com', recipients=[email])
    link=url_for('customer_email',token=token, _external=True)
    msg.body = 'here is the link to change your email {}'.format(link)
    mail.send(msg)
    return redirect(url_for('confirm'))

@app.route('/changeEmailConfirm')
@login_required
def confirm():
    role = session['role']
    if role != 1 or role != 0:
        return redirect(url_for('main'))
    elif role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('main'))
    return render_template('changeEmailLink.html')

@app.route('/customerChangeEmail/<token>', methods=['GET', 'POST'])
@login_required
def customer_email(token):
    role = session['role']
    if role != 1 or role != 0:
        return redirect(url_for('main'))
    elif role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('main'))
    try:
        email=s.loads(token, max_age=20)
    except SignatureExpired:
        return redirect(url_for('expired'))
    id=session['id']
    form = UpdateCustomerForm3()
    user = User.query.get(id)
    if request.method == 'POST' and form.validate_on_submit():
        user.email =request.form['email']
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('changeEmail.html', form=form)

@app.route('/expired')
@login_required
def expired():
    role = session['role']
    if role != 1 or role != 0:
        return redirect(url_for('main'))
    elif role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('main'))
    return render_template('expired.html')

@app.route('/customerChangePass', methods=['GET', 'POST'])
@login_required
def customer_change():
    role = session['role']
    if role != 1 or role != 0:
        return redirect(url_for('main'))
    elif role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('main'))
    id = session['id']
    form = UpdateCustomerForm2()
    user = User.query.get(id)
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        today = date.today()
        user.password = hashed_password
        user.passwordChange = today
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('customerChangePass.html', form=form)






@app.route('/noCustomer')
@login_required
def no_customer():
    role = session['role']
    if role != 1:
        return redirect(url_for('main'))
    elif role == 1:
        pass
    else:
        return redirect(url_for('main'))
    return render_template('noCustomer.html')


@app.route('/noRecord')
@app.route
def no_record():
    role = session['role']
    if role != 1:
        return redirect(url_for('main'))
    elif role == 1:
        pass
    else:
        return redirect(url_for('main'))
    return render_template('noRecord.html')





# Joshua

# APP ROUTES FOR LOAN CREATE/RETRIEVE/UPDATE/DELETE
@app.route('/Loan.html')
def loans():
    plans_dict = {}
    db = shelve.open('Plans.db', 'r')
    plans_dict = db['Plans']
    db.close()

    plans_list = []
    for key in plans_dict:
        plan = plans_dict.get(key)
        plans_list.append(plan)

    return render_template('Loan.html', count=len(plans_list), plans_lists=plans_list)


@app.route('/createLoan.html', methods=['GET', 'POST'])
def create_loan():
    create_loan_form = CreateLoanForm(request.form)
    if request.method == "POST" and create_loan_form.validate():
        loans_dict = {}
        db = shelve.open('Loan.db', 'c')
        print("User successfully saved")
        try:
            loans_dict = db['Loans']
        except:
            print("Error in retrieving Users from user.db.")
        loanentry = Loan.Loan(create_loan_form.first_name.data,
                              create_loan_form.last_name.data,
                              create_loan_form.Amount.data,
                              create_loan_form.email.data,
                              )
        loans_dict[loanentry.get_loan_id()] = loanentry
        db['Loans'] = loans_dict
        db.close()
        print("user saved with {0} as Loan Id".format(loanentry.get_loan_id()))
        return redirect(url_for('retrieve_loans'))
    return render_template('createLoan.html', form=create_loan_form)


@app.route('/retrieveLoan.html')
def retrieve_loans():
    loans_dict = {}
    db = shelve.open('Loan.db', 'r')
    loans_dict = db['Loans']
    db.close()

    loans_list = []
    for key in loans_dict:
        loan = loans_dict.get(key)
        loans_list.append(loan)

    return render_template('retrieveLoan.html', count=len(loans_list), loans_lists=loans_list)


@app.route('/updateLoan.html/<int:id>/', methods=['GET', 'POST'])
def update_loan(id):
    update_loan_form = CreateLoanForm(request.form)
    if request.method == 'POST' and update_loan_form.validate():
        loans_dict = {}
        db = shelve.open('Loan.db', 'w')
        loans_dict = db['Loans']

        loan = loans_dict.get(id)
        loan.set_loan_name1(update_loan_form.first_name.data)
        loan.set_loan_name2(update_loan_form.last_name.data)
        loan.set_loan_amount(update_loan_form.Amount.data)
        loan.set_loan_email(update_loan_form.email.data)

        db['Loans'] = loans_dict
        db.close()

        return redirect(url_for('retrieve_loans'))
    else:
        loans_dict = {}
        db = shelve.open('Loan.db', 'r')
        loans_dict = db['Loans']
        db.close()

        loan = loans_dict.get(id)
        update_loan_form.first_name.data = loan.get_loan_first()
        update_loan_form.last_name.data = loan.get_loan_last()
        update_loan_form.Amount.data = loan.get_loan_amount()

        return render_template('updateLoan.html', form=update_loan_form)


@app.route('/deleteLoan/<int:id>', methods=['POST'])
def delete_loan(id):
    loans_dict = {}
    db = shelve.open('Loan.db', 'w')
    loans_dict = db['Loans']

    loans_dict.pop(id)

    db['Loans'] = loans_dict
    db.close()

    return redirect(url_for('retrieve_Loans'))


@app.route('/createPlan.html', methods=['GET', 'POST'])
def create_plan():
    create_plan_form = CreatePlanForm(request.form)
    if request.method == 'POST' and create_plan_form.validate():
        plans_dict = {}
        db = shelve.open('Plans.db', 'c')
        print("User successfully saved")
        try:
            plans_dict = db['Plans']
        except:
            print("Error in retrieving Users from Plans.db.")
        planentry = Plan.Plan(create_plan_form.Plan_name.data,
                              create_plan_form.Plan_Des.data,
                              create_plan_form.Plan_interest.data, )
        plans_dict[planentry.get_loan_plan_id()] = planentry
        db['Plans'] = plans_dict
        db.close()
        print("Plan saved with {0} as Plan Id".format(planentry.get_loan_plan_id()))
        flash('Document uploaded successfully.')

        return redirect(url_for('retrieve_plan'))

    return render_template('createPlan.html', form=create_plan_form)


@app.route('/retrievePlan.html')
def retrieve_plan():
    plans_dict = {}
    db = shelve.open('Plans.db', 'r')
    plans_dict = db['Plans']
    db.close()

    plans_list = []
    for key in plans_dict:
        plan = plans_dict.get(key)
        plans_list.append(plan)

    return render_template('retrievePlan.html', count=len(plans_list), plans_lists=plans_list)


@app.route('/updatePlan.html/<int:id>/', methods=['GET', 'POST'])
def update_plan(id):
    update_plan_form = CreatePlanForm(request.form)
    if request.method == 'POST' and update_plan_form.validate():
        plans_dict = {}
        db = shelve.open('Plans.db', 'w')
        plans_dict = db['Plans']

        plan = plans_dict.get(id)
        plan.set_loan_plan_name(update_plan_form.Plan_name.data)
        plan.set_loan_plan_desc(update_plan_form.Plan_Des.data)
        plan.set_loan_plan_int(update_plan_form.Plan_interest.data)

        db['Plans'] = plans_dict
        db.close()

        return redirect(url_for('retrieve_plan'))
    else:
        plans_dict = {}
        db = shelve.open('Plans.db', 'r')
        plans_dict = db['Plans']
        db.close()

        plan = plans_dict.get(id)
        update_plan_form.Plan_name.data = plan.get_loan_plan_name()
        update_plan_form.Plan_Des.data = plan.get_loan_plan_desc()
        update_plan_form.Plan_interest.data = plan.get_loan_plan_int()

        return render_template('updatePlan.html', form=update_plan_form)


@app.route('/deletePlan/<int:id>', methods=['POST'])
def delete_plan(id):
    plans_dict = {}
    db = shelve.open('Plans.db', 'w')
    plans_dict = db['Plans']

    plans_dict.pop(id)

    db['Plans'] = plans_dict
    db.close()

    return redirect(url_for('retrieve_plan'))


# @app.route('/searchLoan.html', methods=['GET','POST'])
# def search_loan():
#     search_loan_form = SearchLoanForm(request.form)
#     if request.method == 'POST' and search_loan_form.validate_on_submit():
#         search = search_loan_form.Loan_search.data
#         loans_dict = {}
#         db = shelve.open('Loan.db', 'r')
#         loans_dict = db["Loans"]
#         db.close()
#
#         loans_list = []
#         for key in loans_dict:
#             loan = loans_dict.get(key)
#
#             if Loan.get_loan_UEN() == search:
#                 loans_list.append(loan)
#             else:
#                 continue
#
#         if len(loans_list) !=0:
#             return render_template('showLoan.html', count=len(loans_list), loans_list=loans_list)
#
#
#     return render_template('search.html', form=SearchLoanForm)

# END OF LOAN INIT


# Start of Ravu


@app.route('/SUIshower', methods=['GET', 'POST'])
def SUI_Shower():
    pawn_mock = Pawn.query.all()
    pawn = pawn_mock[-1].sui
    return render_template('SUIshower.html', pawn=pawn)


@app.route('/createPawn', methods=['GET', 'POST'])
def createPawn():
    length = 6
    upper = string.ascii_uppercase
    num = string.digits
    all = upper + num
    tmp = random.sample(all, length)
    captcha_text = "".join(tmp)
    generate_captcha_image(captcha_text)
    form = PawnCreation()
    if form.validate_on_submit():
        sample_string = 'abcdefpqrstuvwxy'  # define the specific string
        # define the condition for random string
        SUI = ''.join((random.choice(sample_string)) for x in range(6))
        new_record = Pawn(first_name=form.first_name.data, last_name=form.last_name.data, nric=form.nric.data,
                          contact_number=form.contactnumber.data, email=form.email.data, address=form.address.data,
                          item_name=form.itemname.data, description=form.Descriptionofitem.data,
                          category=form.Category.data, ItemCondition=form.ItemCondition.data,
                          offer_price=form.offer_price.data, period=form.pawn_period.data, sui=SUI,
                          pawn_status="Processing")
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('SUI_Shower'))
    return render_template('createPawn.html', form=form, captcha_text=captcha_text)


@app.route('/retrievePawn')
def retrieve_pawn():
    return render_template('retrievePawn.html', pawn=Pawn.query.all())


@app.route('/deletepawn/<int:id>', methods=['POST'])
def delete_pawn(id):
    pawn = Pawn.query.get(id)
    db.session.delete(pawn)
    db.session.commit()
    return redirect(url_for('retrieve_pawn'))


@app.route('/viewpawn/<int:id>', methods=['GET', 'POST'])
def view_pawn(id):
    pawn = Pawn.query.get(id)
    return render_template('viewPawn.html', pawn=pawn)


@app.route('/updatepawn/<int:id>/', methods=['GET', 'POST'])
def update_pawn(id):
    form = PawnStatus()
    if form.validate_on_submit():
        row_update = Pawn.query.filter_by(id=id).update(dict(pawn_status=form.pawn_status.data))
        db.session.commit()
        return redirect(url_for('retrieve_pawn'))
    return render_template('updateStatuspawn.html', form=form)


@app.route('/retrieveStatus', methods=['GET', 'POST'])
def retrieve_status():
    form = PawnRetrieval()
    if form.validate_on_submit():
        pawn = Pawn.query.filter_by(sui=form.SUI_CODE.data).first()
        if pawn:
            return render_template('showStatus.html', pawn=pawn)
        else:
            return render_template('noshowStatus.html', pawn=pawn)
    return render_template('retrieveSUI.html', form=form)


@app.route('/searchSUI', methods=['GET', 'POST'])
def search_sui():
    form = SearchSUI()
    if form.validate_on_submit():
        pawn = Pawn.query.filter_by(sui=form.SUI_CODE.data).first()
        if pawn:
            return render_template('resultsSUI.html', pawn=pawn)
        else:
            return render_template('noSUI.html')

    return render_template('searchSUI.html', form=form)


@app.route('/filterStatus', methods=['GET', 'POST'])
def filter_status():
    form = filterStatus()
    if form.validate_on_submit():
        pawn = Pawn.query.filter_by(pawn_status=form.pawn_status.data).all()
        return render_template('resultStatus.html', pawn=pawn)

    return render_template('filterStatus.html', form=form)


# End of Ravu


# ashton
def getCurrencyArray():
    c = CurrencyConverter()
    currency = []
    for a in c.currencies:
        currency.append(a)
    currency.sort()
    return currency


def convert(amt, first, second):
    # converter item
    c = CurrencyConverter()
    final = round(c.convert(amt, first, second), 2)
    rate = round(c.convert(1, first, second), 2)
    return final, rate


@app.route('/moneyExchange', methods=['GET'])
def moneyExchangePage():
    return render_template('moneyExchanger.html', countries=getCurrencyArray())


@app.route('/moneyConvert', methods=['GET'])
def moneyConvertPage():
    return render_template('moneyConvert.html', countries=getCurrencyArray())


@app.route('/moneyExchangeUpdate', methods=['GET'])
def moneyExchangeUpdate():
    transactions = shelve.open('transactions')
    transList = list(transactions.keys())
    trans = []
    for id in transList:
        trans.append(transactions[id])
        print(transactions[id])
    allTrans = list(transactions.keys())
    transactions.close()
    return render_template('update.html', transactions=allTrans, objects=trans)


@app.route('/moneyExchangeDelete', methods=['GET'])
def moneyExchangeDelete():
    transactions = shelve.open('transactions')
    transList = list(transactions.keys())
    trans = []
    for id in transList:
        trans.append(transactions[id])
        print(transactions[id])
    allTrans = list(transactions.keys())
    transactions.close()
    return render_template('delete.html', transactions=allTrans, objects=trans)


@app.route('/convertMoney', methods=['POST'])
def moneyExchange():
    final = 0
    # reading of form input
    if request.method == 'POST':
        # currency object.
        convertObject = Currency(request.form.get('amount'), request.form.get('from'), request.form.get('to'))
        amt = convertObject.getAmount()
        first = convertObject.getInitial()
        second = convertObject.getTo()
        result = convert(convertObject.getAmount(), convertObject.getInitial(), convertObject.getTo())
        # pass the price from checkout page to complete checkout page
        session['price'] = result
        # initial currency
        session['from'] = first
        # converted to currency
        session['to'] = second
        print(second)
        session['amount'] = amt
        if 'convert' in request.form:
            # return result
            return render_template('moneyExchanger.html', amt=amt, result=result[0], first=first, second=second,
                                   rate=result[1], countries=getCurrencyArray())

        elif 'checkout' in request.form:
            return render_template('checkout.html', amt=amt, result=result[0], first=first, second=second,
                                   rate=result[1], cost=session['price'], initial=session['from'], after=session['to'],
                                   amount=session['amount'])

        elif 'delete' in request.form:
            transactions = shelve.open('transactions')
            allTrans = list(transactions.keys())
            return render_template('delete.html', transactions=allTrans)

        elif 'update' in request.form:
            transactions = shelve.open('transactions')
            transList = list(transactions.keys())
            trans = []
            for id in transList:
                trans.append(transactions[id])
                print(transactions[id])
            allTrans = list(transactions.keys())
            transactions.close()
            return render_template('update.html', transactions=allTrans, objects=trans)


@app.route('/completeCheckout', methods=['POST'])
def finishCheckout():
    price = session.get('price')
    initial = session.get('from')
    to = session.get('to')
    amt = session.get('amount')
    transactions = shelve.open('transactions')
    print(len(transactions))
    # transaction id is incremented based off the length of transactions shelve

    customerPaid = CustomerPurchase(request.form.get('firstname'), request.form.get('email'),
                                    request.form.get('address'),
                                    request.form.get('city'), request.form.get('state'), request.form.get('zip'),
                                    amount=amt, initial=initial, to=to, price=price[0],
                                    transactionID=(len(transactions) + 1))

    # we set the key to the transaction id: "1" : <object> and so on
    transactions[str(len(transactions) + 1)] = customerPaid

    transactions.close()

    return render_template('finishCheckout.html', message=customerPaid)


@app.route('/deleteTransaction', methods=['POST'])
def transactionProcess():
    transactions = shelve.open('transactions', flag='c')
    transList = list(transactions.keys())

    if 'check' in request.form:
        return render_template('delete.html', details=transactions[request.form.get('tId')], transactions=transList)

    elif 'delete' in request.form:
        id = request.form.get('tId')
        del transactions[id]
        return render_template('delete.html', deleted=id, transactions=transList)


# for now there is only name update, but there can be more added
@app.route('/updateTransaction', methods=['POST'])
def updateTrans():
    name = request.form.get('newName')
    name = str(name)
    email = request.form.get('newEmail1')
    email = str(email)
    address = request.form.get('newAddress')
    address = str(address)
    id = request.form.get('tId')

    if 'update' in request.form:
        print(name)
        print(email)
        # check if the name is a string
        if name.isalpha():
            print("went here")
            transactions = shelve.open('transactions', writeback=True)
            object = transactions[id]
            object.setName(name)
            object.setEmail(email)
            object.setAddress(address)
            transList = list(transactions.keys())
            print(object)
            transactions.close()
            return render_template('update.html', details=object, transactions=transList)

        # update if it is
        else:
            print("went here2")
            transactions = shelve.open('transactions', writeback=True)
            transList = list(transactions.keys())
            transactions.close()
            return render_template('update.html', error="Name is not valid.", transactions=transList)

    elif 'check' in request.form:
        transactions = shelve.open('transactions', writeback=True)
        transList = list(transactions.keys())
        object = transactions[id]
        print(object)
        transactions.close()
        return render_template('update.html', check=object, transactions=transList)


@app.route('/CurrencyRequest', methods=['GET', 'POST'])
def Feedback2():
    create_feedback1_form = FeedbackForm1(request.form)
    if request.method == 'POST' and create_feedback1_form.validate():
        feedback1_dict = {}
        db = shelve.open('feedback1.db', 'c')

        try:
            feedback1_dict = db['Feedback1']

        except:
            print("Error in retrieving feedback from Feedback1.db.")
        try:
            fb = shelve.open('feedback1.db', 'r')
            fb_dict = fb['feedback1.db']
            feedback = Feedback1(
                create_feedback1_form.name.data,
                create_feedback1_form.contnumb.data,
                create_feedback1_form.email.data,
                create_feedback1_form.requestyourcurrency.data
            )
            feedback1_dict[feedback.get_email()] = feedback
            db['Feedback1'] = feedback1_dict
            db.close()
            return redirect(url_for('main'))
        except:
            feedback = Feedback1(
                create_feedback1_form.name.data,
                create_feedback1_form.contnumb.data,
                create_feedback1_form.email.data,
                create_feedback1_form.requestyourcurrency.data
            )
            feedback1_dict[feedback.get_name()] = feedback
            db['Feedback1'] = feedback1_dict
            db.close()
            return redirect(url_for('main'))
    return render_template('request.html', form=create_feedback1_form)


@app.route('/viewFeedback1', methods=['GET', 'POST'])
def view_feedback1():
    feedback1_dict = {}
    db = shelve.open('feedback1.db', 'r')
    feedback1_dict = db['Feedback1']
    db.close()

    feedback1_list = []
    for key in feedback1_dict:
        feedback = feedback1_dict.get(key)
        feedback1_list.append(feedback)
    return render_template('requested.html', count=len(feedback1_list), feedback1_list=feedback1_list)


if __name__ == '__main__':
    app.run()
