from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,BooleanField
from wtforms.validators import DataRequired, Length, Email, Optional

class AddressForm(FlaskForm):  
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Optional(), Email()])
    phone_number = StringField("Phone", validators=[DataRequired(), Length(min=10, max=10)])
    address = StringField("Address", validators=[DataRequired()])
    pincode = StringField("Pin Code", validators=[DataRequired(), Length(min=6, max=6)])
    homeoffice = SelectField("Home or Office Address", choices=[("home", "Home"), ("office", "Office")], validators=[Optional()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired()])
    phone_number=StringField("phone number",validators=[DataRequired()])
    submit = SubmitField("Submit")


class CheckoutForm(FlaskForm):
    cod=BooleanField("Cash On Delivery",validators=[DataRequired()])
    submit=SubmitField("submit")


class Feedbackform(FlaskForm):
    name=StringField("Name",validators=[DataRequired()])
    feedback=StringField("Feedback",validators=[DataRequired()])
    submit=SubmitField("Submit")