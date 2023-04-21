from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField,IntegerField, SelectField, SubmitField,TextAreaField, PasswordField, BooleanField, RadioField, DateField
from wtforms.validators import InputRequired, DataRequired, Length,Email



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class newuser(FlaskForm):
    username = StringField('Username', validators= [InputRequired()])
    f_name = StringField('First Name', validators=[InputRequired()])
    l_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(),Email('Please enter a valid email adress')])
    password = PasswordField('Password', validators=[InputRequired()])
    

class Addmember(FlaskForm):
    position = StringField('Position', validators=[InputRequired()])
    age = StringField('Age', validators=[InputRequired()])
    f_name = StringField('First Name', validators=[InputRequired()])
    l_name = StringField('Last Name', validators=[InputRequired()])
    m_name = StringField('Middle Name', validators=[InputRequired()])
    dob = StringField('Date of Birth', validators=[InputRequired()])
    gender = SelectField('Gender', choices = [('general','general'),('Male', 'Male'),('Female','Female')], validators=[InputRequired()])
    address = StringField('Address',  validators=[DataRequired(),InputRequired(),Length(max=700)])
    phonenum = StringField('Phone Number', validators=[InputRequired()])
    email = StringField('Email Address', validators=[InputRequired()])