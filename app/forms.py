from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField,IntegerField, SelectField, SubmitField,TextAreaField, PasswordField, BooleanField, RadioField, DateField, SelectMultipleField, widgets
from wtforms.validators import InputRequired, DataRequired, Length,Email



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember me')

class newuser(FlaskForm):
    username = StringField('Username', validators= [InputRequired()])
    f_name = StringField('First Name', validators=[InputRequired()])
    l_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(),Email('Please enter a valid email address')])
    password = PasswordField('Password', validators=[InputRequired()])
    

    

    
   
   
