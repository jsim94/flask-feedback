from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea


class RegisterUser(FlaskForm):

    username = StringField("Username", validators=[
                           Length(max=20), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField("Email", validators=[Length(max=50), InputRequired()])
    first_name = StringField("First Name", validators=[
                             Length(max=30), InputRequired()])
    last_name = StringField("Last Name", validators=[
                            Length(max=30), InputRequired()])


class Login(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=100), InputRequired()])
    content = StringField('Notes', validators=[
                          InputRequired()], widget=TextArea())
