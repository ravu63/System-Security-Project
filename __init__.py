import random
import datetime
import string
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, make_response
from flask_mail import Mail, Message
from Feedback1 import Feedback1
from Forms import OTPform, \
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
import cv2
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from getmac import get_mac_address as gma
import socket

KEY = "8341c4d3ee5842ea9ab5a2f9192a020a"
ENDPOINT = "https://radiant63.cognitiveservices.azure.com/"
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
blob_service_client = BlobServiceClient.from_connection_string(
    "DefaultEndpointsProtocol=https;AccountName=ravu63;AccountKey=Rb3XX8PGQswVKFQPNYGjh+d/1+s98EOyNvltfbuoL89v0c7HcTGa7bPykBuaD8A0FkEVWuNokhhn+AStJVn5+w==;EndpointSuffix=core.windows.net")

s = URLSafeTimedSerializer('ThisIsASecret!')
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
    passAttempt = (db.Column(db.Integer, nullable=False))
    TWOFAStatus = db.Column(db.String(30), nullable=False)
    FUI = db.Column(db.String(300), nullable=True)
    FUI_ID = db.Column(db.String(300), nullable=True)
    verified = db.Column(db.Integer, nullable=True)


class checkNew(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(30),nullable=False)
    device_name=db.Column(db.String(30),nullable=False)
    macaddr=db.Column(db.String(17),nullable=False)

class prevPass(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    dateChange = db.Column(db.Date, nullable=False)


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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postalcode = db.Column(db.Integer, nullable=False)


class LoanData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)


class PlanData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Plan_name = db.Column(db.String(30), nullable=False)
    Plan_description = db.Column(db.String(300), nullable=False)
    Plan_interest = db.Column(db.Integer, nullable=False)


# end Create table

# End of Database

# Start of Forms
# Joshua
class CreateCustomerForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
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
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('F', 'Female'), ('M', 'Male')], default='')
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

# Start of Chest forms
class TransactionForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    city = StringField('City', [validators.Length(min=3, max=150), validators.DataRequired])
    state = StringField('State', [validators.Length(min=3, max=150), validators.DataRequired])
    postalcode = StringField('Postal Code', [validators.Length(min=4, max=6), validators.DataRequired])

    # def validate_name(self, name):

    def validate_postalcode(self, postalcode):
        if not postalcode.data[1:6].isdigit():
            raise ValidationError("Postal Code must not contain letters")

    # def validate_email(self,email):


# End of Chest

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
    try:
        role=session['role']
        x=True
    except:
        x = False
    if x==True:
        if role==1:
            return redirect(url_for('dashboard'))
        elif role==0:
            return redirect(url_for('main'))
    return render_template('home.html')


@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    role = session['role']
    if role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('home'))
    return render_template('main.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    role = session['role']
    if role == 1:
        pass
    else:
        return redirect(url_for('main'))
    return render_template('dashboard.html')


# Joshua
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        current = date.today()
        user = User.query.filter_by(email=form.email.data).first()
        newdev=checkNew.query.filter_by(email=form.email.data).all()
        if user:
            if user.verified==1:
                if user.passAttempt > 2:
                    flash(u'Too many failed password attepmts. Please reset password.')
                else:
                    before = user.passwordChange
                    diff = current - before
                    hostname = socket.gethostname()

                    if diff.days < 30:
                        if bcrypt.check_password_hash(user.password, form.password.data):
                            login_user(user)
                            if diff.days >= 25:
                                msg = Message('Password Expiring', sender='radiantfinancenyp@gmail.com',
                                              recipients=[user.email])
                                msg.body = 'Your password is expiring in {} days'.format(30 - diff.days)
                                mail.send(msg)
                            if user.role == 0:
                                session['id'] = user.id
                                session['role'] = user.role
                                user.passAttempt = 0
                                db.session.commit()
                                check=False
                                for i in range(len(newdev)):
                                    if gma() == newdev[i].macaddr and hostname==newdev[i].device_name:
                                        check=True
                                        if user.TWOFAStatus == "Face":
                                            return redirect(url_for('verifyFace', id=user.id))
                                        elif user.TWOFAStatus == 'Email':
                                            otp = random.randint(1111, 9999)
                                            session['emailotp'] = otp
                                            msg = Message('One Time Password', sender='radiantfinancenyp@gmail.com',
                                                          recipients=[user.email])
                                            msg.body = 'here is your OTP:{}'.format(otp)
                                            mail.send(msg)
                                            return redirect(url_for('emailOTP'))
                                        else:
                                            return redirect(url_for('main'))
                                if check==False:
                                    msg = Message('Login to new Device', sender='radiantfinancenyp@gmail.com',
                                                    recipients=[user.email])
                                    msg.body = 'There is a new device login. If this is not you, please change your password immediately'
                                    mail.send(msg)
                                    new_dev = checkNew(email=form.email.data, device_name=hostname, macaddr=gma())
                                    db.session.add(new_dev)
                                    db.session.commit()
                                    if user.TWOFAStatus == "Face":
                                        return redirect(url_for('verifyFace', id=user.id))
                                    elif user.TWOFAStatus=='Email':
                                        otp = random.randint(1111, 9999)
                                        session['emailotp'] = otp
                                        msg = Message('One Time Password', sender='radiantfinancenyp@gmail.com',
                                                      recipients=[session['email']])
                                        msg.body = 'here is your OTP:{}'.format(otp)
                                        mail.send(msg)
                                        return redirect(url_for('emailOTP'))
                                    else:
                                        return redirect(url_for('main'))

                            elif user.role == 1:
                                session['id'] = user.id
                                session['role'] = user.role
                                user.passAttempt = 0
                                db.session.commit()
                                check = False
                                for i in range(len(newdev)):
                                    if gma() == newdev[i].macaddr and hostname == newdev[i].device_name:
                                        check = True
                                        return redirect(url_for('dashboard'))
                                if check == False:
                                    msg = Message('Login to new Device', sender='radiantfinancenyp@gmail.com',
                                                  recipients=[user.email])
                                    msg.body = 'There is a new device login. If this is not you, please change your password immediately'
                                    mail.send(msg)
                                    new_dev = checkNew(email=form.email.data, device_name=hostname, macaddr=gma())
                                    db.session.add(new_dev)
                                    db.session.commit()
                                    return redirect(url_for('dashboard'))
                            else:
                                return redirect(url_for('home'))
                        else:
                            user.passAttempt += 1
                            db.session.commit()
                            flash(u'Invalid Email or Password')
                    else:
                        flash(u'Password has expired. Please change password.')
            else:
                flash(u'Please verify your email before continuing')
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
                        passwordChange=today, passAttempt=0, TWOFAStatus='None',FUI="None",FUI_ID="None",verified=0)
        db.session.add(new_user)
        db.session.commit()

        msg = Message('Verify Email', sender='radiantfinancenyp@gmail.com',
                      recipients=[form.email.data])
        link = url_for('verify', _external=True)
        msg.body = 'Please click the link to verify your email {}'.format(link)
        mail.send(msg)
        session['verify']=form.email.data

        hostname = socket.gethostname()
        new_dev=checkNew(email=form.email.data,device_name=hostname,macaddr=gma())
        db.session.add(new_dev)
        db.session.commit()
        if new_user.TWOFAStatus == "None":
            return render_template('setup2FA.html')

    return render_template('signup.html', form=form)




#cheston email stuff

@app.route('/verifyEmail', methods=['GET', 'POST'])
def verify():
    email=session['verify']
    user=User.query.filter_by(email=email).first()
    user.verified=1
    db.session.commit()
    return render_template('verified.html')


@app.route('/registerEmail2FA', methods=['GET', 'POST'])
def registerEmail2FA():
    email = session['verify']
    user = User.query.filter_by(email=email).first()
    user.TWOFAStatus = 'Email'
    db.session.commit()
    return render_template('email2fa.html')





@app.route('/emailOTP', methods=['POST', 'GET'])
def emailOTP():
    login_form = OTPform(request.form)
    if request.method == 'POST':
        otp = session['emailotp']
        otp2 = int(request.form['otp3'])
        if otp == otp2:
            return redirect(url_for('main'))
        else:
            flash(u'Invalid OTP provided')
    return render_template('OTP.html', form=login_form)

#end of chestion email stuff

# Ravu Face Verification

# make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass





@app.route('/registerFace', methods=['GET', 'POST'])
def registerFace():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = camera.read()
        frame = cv2.putText(cv2.flip(frame, 1), "Press Space to Capture!", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Register Face", frame)
        k = cv2.waitKey(1)
        if k % 256 == 32:  # Press Space to Capture the Face
            now = datetime.now()
            p = os.path.sep.join(['shots', "shot_{}.jpg".format(str(now).replace(":", ''))])
            cv2.imwrite(p, frame)
            blob_client = blob_service_client.get_blob_client(container='radiant', blob=p)
            with open(p, "rb") as data:
                blob_client.upload_blob(data)
            url = "https://ravu63.blob.core.windows.net/radiant/" + p
            image_url = url
            image_url_name = os.path.basename(url)
            see_face = face_client.face.detect_with_url(url=image_url, detection_model='detection_03',
                                                        recognition_model='recognition_04')
            if not see_face:
                os.remove(p)
                print("Face is not detected")
                continue
            else:
                duncan = see_face[0].face_id
                user = User.query.all()
                user_id = user[-1].id
                row_update = User.query.filter_by(id=user_id).update(dict(FUI=image_url))
                row_update_2 = User.query.filter_by(id=user_id).update(dict(TWOFAStatus="Face"))
                row_update_3 = User.query.filter_by(id=user_id).update(dict(FUI_ID=duncan))
                db.session.commit()
                print("Face is detected")
                os.remove(p)
                camera.release()
                cv2.destroyAllWindows()
                return redirect(url_for('login'))

    return render_template("registerFace.html")


@app.route('/verifyFace/<int:id>', methods=['GET', 'POST'])
def verifyFace(id):
    mock_try = User.query.get(id)
    mock = mock_try.FUI_ID
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = camera.read()
        frame = cv2.putText(cv2.flip(frame, 1), "Press Space to Capture!", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 4)
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Register Face", frame)
        k = cv2.waitKey(10)
        if k % 256 == 32:  # Press Space to Capture the Face
            now = datetime.now()
            p = os.path.sep.join(['shots', "shot_{}.jpg".format(str(now).replace(":", ''))])
            cv2.imwrite(p, frame)
            blob_client = blob_service_client.get_blob_client(container='verification', blob=p)
            with open(p, "rb") as data:
                blob_client.upload_blob(data)
            url = "https://ravu63.blob.core.windows.net/verification/" + p
            image_url = url
            image_url_name = os.path.basename(url)
            see_face = face_client.face.detect_with_url(url=image_url, detection_model='detection_03',
                                                        recognition_model='recognition_04')
            if see_face:
                duncan = see_face[0].face_id
                verify = face_client.face.verify_face_to_face(
                    face_id1=mock,
                    face_id2=duncan
                )
                print(duncan)
                print(mock)
                print(verify.is_identical)
                if verify.confidence > 0.91:
                    os.remove(p)
                    camera.release()
                    cv2.destroyAllWindows()
                    return redirect(url_for('main'))
                else:
                    os.remove(p)
                    continue
            else:
                os.remove(p)
                print("Face is not detected")
                continue

    return render_template('verifyFace.html')


# End of Ravu Face shit


@app.route('/createAdmin', methods=['GET', 'POST'])
@login_required
def create_admin():
    form = CreateCustomerForm()
    role = session['role']
    if role == 1:
        pass
    else:
        return redirect(url_for('main'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        today = date.today()
        new_user = User(name=form.name.data, gender=form.gender.data, phone=form.phone.data,
                        birthdate=form.birthdate.data, email=form.email.data, password=hashed_password, role=1,
                        passwordChange=today, passAttempt=0, TWOFAStatus='idk',verified=1)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('manage_admin'))
    return render_template('createAdmin.html', form=form)


@app.route('/manageCustomer', methods=['GET', 'POST'])
@login_required
def manage_customers():
    role = session['role']
    if role == 1:
        pass
    else:
        return redirect(url_for('main'))
    return render_template('manageCustomer.html', Users=User.query.all())


@app.route('/manageAdmin', methods=['GET', 'POST'])
@login_required
def manage_admin():
    role = session['role']
    if role == 1:
        pass
    else:
        return redirect(url_for('main'))
    return render_template('manageAdmin.html', Users=User.query.all())


@app.route('/updateAdmin/<id>/', methods=['GET', 'POST'])
@login_required
def customer_Admin(id):
    role = session['role']
    if role == 1:
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
    if role == 1:
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
    if role == 1:
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
    session.pop('role',None)
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
    email=user.email
    prev = prevPass.query.filter_by(email=email).all()
    newdev = checkNew.query.filter_by(email=email).all()
    if request.method == 'POST' and form.validate_on_submit():
        prevCheck=False
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        today = date.today()
        if len(prev) == 0:
            prevCheck = True
        else:
            for i in range(len(prev)):
                if bcrypt.check_password_hash(prev[i].password, form.password.data):
                    flash(u'Please do not use the old passwords.')
                else:
                    prevCheck = True
        if prevCheck == True:
            if bcrypt.check_password_hash(user.password,form.password.data):
                flash(u'Your current password is the same as the new password you entered in.')
            else:
                newPrev = prevPass(email=user.email, password=user.password, dateChange=today)
                db.session.add(newPrev)
                db.session.commit()

                user.password = hashed_password
                user.passwordChange = today
                user.passAttempt = 0
                db.session.commit()

                for i in range(len(newdev)):
                    db.session.delete(newdev[i])
                    db.session.commit()

                hostname = socket.gethostname()
                new_dev = checkNew(email=user.email, device_name=hostname, macaddr=gma())
                db.session.add(new_dev)
                db.session.commit()
                session.pop('email', None)
                session.pop('otp', None)
                return redirect(url_for('login'))



    return render_template('changePassword.html', form=form)


@app.route('/manageAccount', methods=['GET', 'POST'])
@login_required
def manage_account():
    role = session['role']
    if role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('home'))
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

    return render_template('manageAccount.html', form=form, user=user)


@app.route('/changeEmail', methods=['GET', 'POST'])
@login_required
def email():
    role = session['role']
    if role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('home'))
    id = session['id']
    user = User.query.get(id)
    email = user.email
    token = s.dumps(email)
    msg = Message('Changing Email', sender='radiantfinancenyp@gmail.com', recipients=[email])
    link = url_for('customer_email', token=token, _external=True)
    msg.body = 'here is the link to change your email {}'.format(link)
    mail.send(msg)
    return redirect(url_for('confirm'))


@app.route('/changeEmailConfirm')
@login_required
def confirm():
    role = session['role']
    if role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('home'))
    return render_template('changeEmailLink.html')


@app.route('/customerChangeEmail/<token>', methods=['GET', 'POST'])
@login_required
def customer_email(token):
    role = session['role']
    if role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('home'))
    try:
        email = s.loads(token, max_age=20)
    except SignatureExpired:
        return redirect(url_for('expired'))
    id = session['id']
    form = UpdateCustomerForm3()
    user = User.query.get(id)
    if request.method == 'POST' and form.validate_on_submit():
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('changeEmail.html', form=form)


@app.route('/expired')
@login_required
def expired():
    role = session['role']
    if role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('home'))
    return render_template('expired.html')


@app.route('/customerChangePass', methods=['GET', 'POST'])
@login_required
def customer_change():
    role = session['role']
    if role == 1 or role == 0:
        pass
    else:
        redirect(url_for('home'))
    id = session['id']
    form = UpdateCustomerForm2()
    user = User.query.get(id)
    email=user.email
    prev=prevPass.query.filter_by(email=email).all()
    newdev = checkNew.query.filter_by(email=email).all()
    if request.method == 'POST' and form.validate_on_submit():
        prevCheck=False
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        today = date.today()
        if len(prev)==0:
            prevCheck=True
        else:
            for i in range(len(prev)):
                if bcrypt.check_password_hash(prev[i].password, form.password.data):
                    flash(u'Please do not use the old passwords.')
                else:
                    prevCheck=True
        if prevCheck==True:
            if bcrypt.check_password_hash(user.password,form.password.data):
                flash(u'Your current password is the same as the new password you entered in.')
            else:
                newPrev = prevPass(email=user.email, password=user.password, dateChange=today)
                db.session.add(newPrev)
                db.session.commit()

                user.password = hashed_password
                user.passwordChange = today
                user.passAttempt = 0
                db.session.commit()

                for i in range(len(newdev)):
                    db.session.delete(newdev[i])
                    db.session.commit()

                hostname = socket.gethostname()
                new_dev = checkNew(email=user.email, device_name=hostname, macaddr=gma())
                db.session.add(new_dev)
                db.session.commit()
                return redirect(url_for('main'))


    return render_template('customerChangePass.html', form=form)


@app.route('/noCustomer')
@login_required
def no_customer():
    role = session['role']
    if role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('home'))
    return render_template('noCustomer.html')


@app.route('/noRecord')
@app.route
def no_record():
    role = session['role']
    if role == 1 or role == 0:
        pass
    else:
        return redirect(url_for('home'))
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
    if request.method == 'POST' and create_loan_form.validate():
        loanentry = LoanData(first_name=create_loan_form.first_name.data,
                             last_name=create_loan_form.last_name.data,
                             amount=create_loan_form.Amount.data,
                             email=create_loan_form.email.data)
        db.session.add(loanentry)
        db.session.commit()
        return redirect(url_for('retrieve_loan'))
    return render_template('createLoan.html', form=create_loan_form)
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


@app.route('/retrieveLoan.html')
def retrieve_loans():
    return LoanData.query.get(int(LoanData.id))


@app.route('/updateLoan.html/<int:id>/', methods=['GET', 'POST'])
def update_loan(id):
    update_loan_form = CreateLoanForm(request.form)
    if request.method == 'POST' and update_loan_form.validate():
        loanentry = LoanData(first_name=update_loan_form.first_name.data,
                             last_name=update_loan_form.last_name.data,
                             amount=update_loan_form.Amount.data,
                             email=update_loan_form.email.data)
        db.session.add(loanentry)
        db.session.commit()
        return redirect(url_for('retrieve_loans'))
    else:
        # loan = LoanData.query.get(int(LoanData.id))
        # update_loan_form.first_name.data = loan.get_loan_first()
        # update_loan_form.last_name.data = loan.get_loan_last()
        # update_loan_form.Amount.data = loan.get_loan_amount()
        return render_template('updateLoan.html', form=update_loan_form)


# @app.route('/deleteLoan/<int:id>', methods=['POST'])
# def delete_loan(id):
#     loans_dict = {}
#     db = shelve.open('Loan.db', 'w')
#     loans_dict = db['Loans']
#
#     loans_dict.pop(id)
#
#     db['Loans'] = loans_dict
#     db.close()
#
#     return redirect(url_for('retrieve_Loans'))


@app.route('/createPlan.html', methods=['GET', 'POST'])
def create_plan():
    create_plan_form = CreatePlanForm(request.form)
    if request.method == 'POST' and create_plan_form.validate():
        planentry = PlanData(id=PlanData.id + 1,
                             Plan_Name=create_plan_form.Plan_name.data,
                             Plan_descripion=create_plan_form.Plan_Des.data,
                             Plan_interest=create_plan_form.Plan_interest.data)
        db.session.add(planentry)
        db.session.commit()
        return redirect(url_for('retrieve_plan'))

    return render_template('createPlan.html', form=create_plan_form)


# @app.route('/retrievePlan.html')
# def retrieve_plan():
#     plans_dict = {}
#     db = shelve.open('Plans.db', 'r')
#     plans_dict = db['Plans']
#     db.close()
#
#     plans_list = []
#     for key in plans_dict:
#         plan = plans_dict.get(key)
#         plans_list.append(plan)
#
#     return render_template('retrievePlan.html', count=len(plans_list), plans_lists=plans_list)


@app.route('/updatePlan.html/<int:id>/', methods=['GET', 'POST'])
def update_plan(id):
    update_plan_form = CreatePlanForm(request.form)
    if request.method == 'POST' and update_plan_form.validate():
        planentry = PlanData(Plan_Name=update_plan_form.Plan_name.data,
                             Plan_descripion=update_plan_form.Plan_Des.data,
                             Plan_interest=update_plan_form.Plan_interest.data)
        db.session.add(planentry)
        db.session.commit()
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


# @app.route('/deletePlan/<int:id>', methods=['POST'])
# def delete_plan(id):
#     plans_dict = {}
#     db = shelve.open('Plans.db', 'w')
#     plans_dict = db['Plans']
#
#     plans_dict.pop(id)
#
#     db['Plans'] = plans_dict
#     db.close()
#
#     return redirect(url_for('retrieve_plan'))


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


if __name__ == '__main__':
    app.run()
