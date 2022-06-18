from currency_converter import CurrencyConverter
import Admin
import Customer
import Feedback
import Loan
import random
import shelve
import Plan
from PawnCreation import Pawn_Creation
from PawnStatus import Pawn_Status
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from Feedback1 import Feedback1
from Forms import   UpdateCustomerForm2, ForgetPassword, OTPform, \
    ChangePassword, FeedbackForm, SearchCustomerForm, UpdateStatus, CreateLoanForm, CreatePlanForm, PawnCreation, \
    PawnStatus, \
    PawnRetrieval, SearchSUI, filterStatus, FeedbackForm1
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, PasswordField, SelectField, ValidationError, TextAreaField, SubmitField
from wtforms.fields import EmailField, DateField, FileField, IntegerField, RadioField, SearchField
from wtforms.validators import InputRequired,length,ValidationError
from transaction import Transaction, CustomerPurchase
from Currency import Currency
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required,logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import date

app = Flask(__name__)
app.debug=True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "radiantfinancenyp@gmail.com"
app.config['MAIL_PASSWORD'] = "Radiant12345"
mail = Mail(app)
bcrypt=Bcrypt(app)

db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

#Create table
class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    phone = db.Column(db.String(8), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role=db.Column(db.Integer, nullable=False)
#end Create table

#Forms
class CreateCustomerForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()],render_kw={"placeholder":"Name:"})
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='',render_kw={"placeholder":"Gender:"})
    phone = StringField('Phone', [validators.Length(min=8, max=8), validators.DataRequired()],render_kw={"placeholder":"Phone Number:"})
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()],render_kw={"placeholder":"Email:"})
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired(),
                                          validators.EqualTo('confirmpassword', message='Error:Passwords must match')],render_kw={"placeholder":"Password:"})
    confirmpassword = PasswordField('Confirm Password', [validators.DataRequired()],render_kw={"placeholder":"Confirm Password:"})
    submit=SubmitField('Register')
    def validate_phone(self, phone):
        if not phone.data[1:8].isdigit():
            raise ValidationError("Phone number must not contain letters")
    def validate_email(self,email):
        existing_user_email=User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError(flash(u'User exists'))


class LoginForm(FlaskForm):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()],render_kw={"placeholder":"Email:"})
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired()],render_kw={"placeholder":"Password:"})
    submit = SubmitField('Login')



class UpdateCustomerForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()],render_kw={"placeholder":"Name:"})
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[ ('F', 'Female'), ('M', 'Male')],default='',render_kw={"placeholder":"Gender:"})
    phone = StringField('Phone', [validators.Length(min=8, max=8), validators.DataRequired()],render_kw={"placeholder":"Phone Number:"})
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()],render_kw={"placeholder":"Email:"})
    submit=SubmitField('Update')

    def validate_phone(self, phone):
        if not phone.data[1:8].isdigit():
            raise ValidationError("Phone number must not contain letters")

#End Fomrs

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

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
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                if user.role==0:
                    return redirect(url_for('main'))
                else:
                    return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form=CreateCustomerForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data)
        new_user=User(name=form.name.data, gender=form.gender.data, phone=form.phone.data, birthdate=form.birthdate.data, email=form.email.data, password=hashed_password, role=0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html',form=form)



@app.route('/createAdmin', methods=['GET', 'POST'])
@login_required
def create_admin():
    form = CreateCustomerForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, gender=form.gender.data, phone=form.phone.data,
                        birthdate=form.birthdate.data, email=form.email.data, password=hashed_password, role=1)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('manage_admin'))
    return render_template('createAdmin.html', form=form)


@app.route('/manageCustomer', methods=['GET', 'POST'])
@login_required
def manage_customers():
    return render_template('manageCustomer.html', Users=User.query.all())


@app.route('/manageAdmin', methods=['GET', 'POST'])
@login_required
def manage_admin():
    return render_template('manageAdmin.html', Users=User.query.all())



@app.route('/updateAdmin/<id>/', methods=['GET', 'POST'])
@login_required
def customer_Admin(id):
    form = UpdateCustomerForm()
    user = User.query.get_or_404(id)
    if request.method == 'POST' and form.validate_on_submit():
        user.name = request.form['name']
        user.email = request.form['email']
       # user.birthdate = int(date(request.form['birthdate']))
        user.phone = request.form['phone']
        user.gender = request.form['gender']
        db.session.commit()
        flash("User updated successfully!")
        return redirect(url_for('manage_admin'))

    return render_template('updateAdmin.html', form=form,user=user)


@app.route('/deleteCustomer/<id>', methods=['POST'])
@login_required
def delete_customer(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('manage_customers'))


@app.route('/deleteAdmin/<id>', methods=['POST'])
@login_required
def delete_admin(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('manage_admin'))


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/forgotPassword', methods=['POST', 'GET'])
def forgot_password():
    login_form = ForgetPassword(request.form)
    try:
        if request.method == 'POST':
            users = shelve.open('signup.db', 'r')
            email = request.form['email']
            users_dict = users['Customers']
            users_keys = list(users_dict.keys())
            user = users_dict[email]
            if user.get_email() == email:
                session['id'] = user.get_email()
                users.close()
                return redirect(url_for('getOTP'))
            else:
                flash(u'Invalid email provided')
    except:
        flash(u'Invalid email provided')

    return render_template('forgotPassword.html', form=login_form)


@app.route('/getOTP', methods=['POST', 'GET'])
def getOTP():
    if request.method == 'POST':
        otp = random.randint(1111, 9999)
        session['otp'] = otp
        msg = Message('One Time Password', sender='radiantfinancenyp@gmail.com', recipients=[session['id']])
        msg.body = 'here is your OTP:{}'.format(otp)
        mail.send(msg)
        return redirect(url_for('OTP'))
    return render_template('getOTP.html')


@app.route('/OTP', methods=['POST', 'GET'])
def OTP():
    login_form = OTPform(request.form)
    if request.method == 'POST':
        otp = session['otp']
        otp2 = int(request.form['otp3'])
        if otp == otp2:
            return redirect(url_for('change_password', id=id))
        else:
            flash(u'Invalid OTP provided')
    return render_template('OTP.html', form=login_form)


@app.route('/changePassword/<id>', methods=['POST', 'GET'])
def change_password(id):
    update_customer_form = UpdateCustomerForm2(request.form)
    id = session['id']

    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('signup.db', 'w')
        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_password(update_customer_form.password.data)

        db['Customers'] = customer_dict
        db.close()

        return redirect(url_for('login'))
    return render_template('customerChangePass.html', form=update_customer_form)


@app.route('/manageAccount/<id>/', methods=['GET', 'POST'])
@login_required
def manage_account(id):
    update_customer_form = UpdateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('signup.db', 'w')
        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_phone(update_customer_form.phone.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_birthdate(update_customer_form.birthdate.data)

        db['Customers'] = customer_dict
        db.close()

        return redirect(url_for('main'))
    else:
        users_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer = customer_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone.data = customer.get_phone()
        update_customer_form.birthdate.data = customer.get_birthdate()

    return render_template('manageAccount.html', form=update_customer_form)


@app.route('/customerChangePass/<id>/', methods=['GET', 'POST'])
@login_required
def customer_change(id):
    update_customer_form = ChangePassword(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('signup.db', 'w')
        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_password(update_customer_form.password.data)

        db['Customers'] = customer_dict
        db.close()

        return redirect(url_for('main'))
    else:
        users_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer = customer_dict.get(id)
        update_customer_form.password.data = customer.get_password()

    return render_template('customerChangePass.html', form=update_customer_form)


@app.route('/searchCustomer', methods=['GET', 'POST'])
@login_required
def search_customer():
    search_customer_form = SearchCustomerForm(request.form)
    if request.method == 'POST' and search_customer_form.validate():
        search = search_customer_form.searchCustomer.data
        customer_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer_list = []
        for key in customer_dict:
            customer = customer_dict.get(key)
            if search in customer.get_email():
                if customer.get_role() == 0:
                    customer_list.append(customer)
            # else:
            # continue

        if len(customer_list) > 0:
            return render_template('showCustomer.html', count=len(customer_list), customer_list=customer_list)
        else:
            return redirect(url_for('no_customer'))
    return render_template('searchCustomer.html', form=search_customer_form)


@app.route('/searchAdmin', methods=['GET', 'POST'])
@login_required
def search_admin():
    search_customer_form = SearchCustomerForm(request.form)
    if request.method == 'POST' and search_customer_form.validate():
        search = search_customer_form.searchCustomer.data
        customer_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer_list = []
        for key in customer_dict:
            customer = customer_dict.get(key)
            if search in customer.get_email():
                if customer.get_role() == 1:
                    customer_list.append(customer)
            # else:
            # continue

        if len(customer_list) > 0:
            return render_template('showAdmin.html', count=len(customer_list), customer_list=customer_list)
        else:
            return redirect(url_for('no_customer'))
    return render_template('searchCustomer.html', form=search_customer_form)


@app.route('/noCustomer')
def no_customer():
    return render_template('noCustomer.html')
@app.route('/noRecord')
def no_record():
    return render_template('noRecord.html')


@app.route('/showCustomer')
def show_customer():
    return render_template('showCustomer.html')

@app.route('/customerStuff',methods=['GET','POST'])
def customer_stuff():
    search_customer_form=SearchCustomerForm(request.form)
    if request.method=='POST'and search_customer_form.validate():
        number=[]
        searchCustomer=search_customer_form.searchCustomer.data
        #transactions = shelve.open('transactions')
        #transList = list(transactions.keys())
        #transactions.close()
        #trans = []
        #for id in transList:
         #   if transList.getEmail()==searchCustomer:
          #      trans.append(transactions[id])
           #     number.append('1')
            #else:
             #   continue


        # transaction_dict={}
        # trans=shelve.open('transactions','r')
        # transaction_dict=trans['Transaction']
        # trans.close()
        #
        # transaction_list=[]
        # for key in transaction_dict:
        #     transaction=transaction_dict.get(key)
        #     if transaction.get_email()==searchCustomer:
        #         transaction_list.append(transaction)
        #         number.append('1')
        #     else:
        #         continue



        loan_dict = {}
        loan = shelve.open('loan.db', 'r')
        loan_dict = loan['Loans']
        loan.close()

        loan_list = []
        for key in loan_dict:
            loan = loan_dict.get(key)
            if loan.get_loan_email() == searchCustomer:
                loan_list.append(loan)
                number.append('1')
            else:
                continue


        pawn_dict ={}
        pawn = shelve.open('pawn1.db', 'r')
        pawn_dict = pawn['Pawns']
        pawn.close()

        pawn_list = []
        for key in pawn_dict:
            pawn = pawn_dict.get(key)
            if pawn.get_email() == searchCustomer:
                pawn_list.append(pawn)
                number.append('1')
            else:
                continue

        if len(number)>0:
            return render_template("customerStuff.html", count=len(number), loan_list=loan_list,pawn_dict=pawn_dict)
        else:
            return redirect(url_for('no_record'))
    return render_template('searchStuff.html',form=search_customer_form)


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

    return render_template('Loan.html',count=len(plans_list), plans_lists=plans_list)


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
                              create_plan_form.Plan_interest.data,)
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




#Start of Ravu


@app.route('/SUIshower', methods=['GET', 'POST'])
def SUI_Shower():
    pawns_dict = {}
    db = shelve.open('pawn1.db', 'c')
    pawns_dict = db['Pawns']
    db.close()

    pawn_list = []
    for key in pawns_dict:
        pawn = pawns_dict.get(key)
        pawn_list.append(pawn)

    return render_template('SUIshower.html', pawn_list=pawn_list, count=len(pawn_list))


@app.route('/createPawn', methods=['GET', 'POST'])
def createPawn():
    create_pawn_form = PawnCreation(request.form)
    if request.method == 'POST' and create_pawn_form.validate():
        pawns_dict = {}
        db = shelve.open('pawn1.db', 'c')
        sample_string = 'abcdefpqrstuvwxy'  # define the specific string
        # define the condition for random string
        SUI = ''.join((random.choice(sample_string)) for x in range(6))
        try:
            pawns_dict = db['Pawns']
        except:
            print("Error in retrieving Users from pawn1.db.")
        pawn = Pawn_Creation(create_pawn_form.first_name.data, create_pawn_form.last_name.data, create_pawn_form.nric.data, create_pawn_form.contactnumber.data, create_pawn_form.email.data, create_pawn_form.address.data, create_pawn_form.itemname.data, create_pawn_form.Descriptionofitem.data, create_pawn_form.Category.data,
                             create_pawn_form.ItemCondition.data, create_pawn_form.offer_price.data, create_pawn_form.pawn_period.data, SUI, 'Processing')
        pawns_dict[pawn.get_item_id()] = pawn
        db['Pawns'] = pawns_dict

        db.close()
        return redirect(url_for('SUI_Shower'))
    return render_template('createPawn.html', form=create_pawn_form)


@app.route('/retrievePawn')
def retrieve_pawn():
    pawns_dict = {}
    db = shelve.open('pawn1.db', 'c')
    pawns_dict = db['Pawns']
    db.close()

    pawn_list = []
    for key in pawns_dict:
        pawn = pawns_dict.get(key)
        pawn_list.append(pawn)

    return render_template('retrievePawn.html', count=len(pawn_list), pawn_list=pawn_list)


@app.route('/deletepawn/<int:id>', methods=['POST'])
def delete_pawn(id):
    pawns_dict = {}
    db = shelve.open('pawn1.db', 'w')
    pawns_dict = db['Pawns']
    if id in pawns_dict:
        pawns_dict.pop(id)
        db['Pawns'] = pawns_dict
        db.close()
        return redirect(url_for('retrieve_pawn'))
    return render_template('retrievePawn.html')


@app.route('/viewpawn/<int:id>', methods=['GET', 'POST'])
def view_pawn(id):
    pawn_dict = {}
    db = shelve.open('pawn1.db', 'w')
    pawns_dict = db['Pawns']

    db['Pawns'] = pawns_dict
    db.close()

    view_list = []
    pawn = pawns_dict.get(id)
    view_list.append(pawn)

    return render_template('viewPawn.html', view_list=view_list)


@app.route('/updatepawn/<int:id>/', methods=['GET', 'POST'])
def update_pawn(id):
    update_pawn_form = PawnStatus(request.form)
    if request.method == 'POST' and update_pawn_form.validate():
        pawns_dict = {}
        db = shelve.open('pawn1.db', 'c')
        pawns_dict = db['Pawns']
        if id in pawns_dict:
            pawn = pawns_dict.get(id)
            pawn.set_firstname(pawn.get_firstname())
            pawn.set_lastname(pawn.get_lastname())
            pawn.set_nric(pawn.get_nric())
            pawn.set_contactnumber(pawn.get_contactnumber())
            pawn.set_email(pawn.get_email())
            pawn.set_address(pawn.get_address())
            pawn.set_itemname(pawn.get_itemname())
            pawn.set_Descriptionofitem(pawn.get_Descriptionofitem())
            pawn.set_category(pawn.get_category())
            pawn.set_ItemCondition(pawn.get_ItemCondition())
            pawn.set_offer_price(pawn.get_offer_price())
            pawn.set_pawn_period(pawn.get_pawn_period())
            pawn.set_SUI(pawn.get_SUI())
            pawn.set_status(update_pawn_form.pawn_status.data)
            db['Pawns'] = pawns_dict
            db.close()

    else:
        pawns_dict = {}
        db = shelve.open('pawn1.db', 'r')
        if id in pawns_dict:
            pawn = pawns_dict.get(id)
            update_pawn_form.pawn_status.data = pawn.get_status()
            pawns_dict = db['Pawns']
            db.close()
            return redirect(url_for('retrieve_pawn'))

    return render_template('updateStatuspawn.html', form=update_pawn_form)


@app.route('/retrieveStatus', methods=['GET', 'POST'])
def retrieve_status():
    retrieve_status_form = PawnRetrieval(request.form)
    if request.method == 'POST' and retrieve_status_form.validate():
        f_search = retrieve_status_form.SUI_CODE.data
        pawns_dict = {}
        db = shelve.open('pawn1.db', 'r')
        pawns_dict = db['Pawns']
        db.close()
        search = str(f_search)
        pawns_list = []
        for key in pawns_dict:
            pawn = pawns_dict.get(key)
            if pawn.get_SUI() == search:
                pawns_list.append(pawn)

            else:
                continue

        if len(pawns_list) != 0:
            return render_template("showStatus.html", count=len(pawns_list), pawns_list=pawns_list)

        else:
            return render_template("noshowStatus.html")

    return render_template('retrieveSUI.html', form=retrieve_status_form)


@app.route('/searchSUI', methods=['GET', 'POST'])
def search_sui():
    search_status_form = SearchSUI(request.form)
    if request.method == 'POST' and search_status_form.validate():
        f_search = search_status_form.SUI_CODE.data
        pawns_dict = {}
        db = shelve.open('pawn1.db', 'r')
        pawns_dict = db['Pawns']
        db.close()
        search = str(f_search)
        pawns_list = []
        for key in pawns_dict:
            pawn = pawns_dict.get(key)
            if pawn.get_SUI() == search:
                pawns_list.append(pawn)

            else:
                continue

        if len(pawns_list) != 0:
            return render_template("resultsSUI.html", count=len(pawns_list), pawns_list=pawns_list)

        else:
            return render_template("noSUI.html")

    return render_template('searchSUI.html', form=search_status_form)


@app.route('/filterStatus', methods=['GET', 'POST'])
def filter_status():
    filter_status_form = filterStatus(request.form)
    if request.method == 'POST' and filter_status_form.validate():
        f_search = filter_status_form.pawn_status.data
        pawns_dict = {}
        db = shelve.open('pawn1.db', 'r')
        pawns_dict = db['Pawns']
        db.close()
        search = str(f_search)
        pawns_list = []
        for key in pawns_dict:
            pawn = pawns_dict.get(key)
            if pawn.get_pawnstatus() == search:
                pawns_list.append(pawn)

            else:
                continue

        if len(pawns_list) != 0:
            return render_template('resultStatus.html', count=len(pawns_list), pawns_list=pawns_list)

        else:
            return render_template("noSUI.html")

    return render_template('filterStatus.html', form=filter_status_form)

#End of Ravu


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
                                   rate=result[1], cost=session['price'], initial=session['from'], after=session['to'], amount=session['amount'])

        elif 'delete' in request.form:
            transactions = shelve.open('transactions')
            allTrans = list(transactions.keys())
            return render_template('delete.html', transactions = allTrans)

        elif 'update' in request.form:
            transactions = shelve.open('transactions')
            transList = list(transactions.keys())
            trans = []
            for id in transList:
                trans.append(transactions[id])
                print(transactions[id])
            allTrans = list(transactions.keys())
            transactions.close()
            return render_template('update.html', transactions = allTrans, objects=trans)


@app.route('/completeCheckout', methods=['POST'])
def finishCheckout():
    price = session.get('price')
    initial = session.get('from')
    to = session.get('to')
    amt = session.get('amount')
    transactions = shelve.open('transactions')
    print(len(transactions))
    # transaction id is incremented based off the length of transactions shelve

    customerPaid = CustomerPurchase(request.form.get('firstname'), request.form.get('email'), request.form.get('address'),
                              request.form.get('city'), request.form.get('state'), request.form.get('zip'),
                                    amount=amt, initial=initial, to=to, price=price[0], transactionID=(len(transactions) + 1))

    # we set the key to the transaction id: "1" : <object> and so on
    transactions[str(len(transactions) + 1)] = customerPaid

    transactions.close()

    return render_template('finishCheckout.html', message = customerPaid)


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
            fb = shelve.open('feedback1.db','r')
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
    app.run(debug=True)
