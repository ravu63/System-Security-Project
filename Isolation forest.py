import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest
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
import datetime
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


class LoginData(db.Model):
    LoginEntry = db.Column(db.Integer, primary_key=True)
    LoginEmail = db.Column(db.String(50), nullable=False)
    LoginTime = db.Column(db.Time(), nullable=False)


data = pd.read_csv('marks.csv')
data.head(10)
sns.boxplot(data.marks)
random_state = np.random.RandomState(42)
model = IsolationForest(n_estimators=100, max_samples='auto', contamination=float(0.2), random_state=random_state)
model.fit(data[['marks']])
print(model.get_params())

data['scores'] = model.decision_function(data[['marks']])
data['anomaly_score'] = model.predict(data[['marks']])
data[data['anomaly_score'] == -1].head()
anomaly_count = len(data['anomaly_score'])

accuracy = 100 * list(data['anomaly_score']).count(-1) / anomaly_count
print("Accuracy of the model:", accuracy)
