from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField,IntegerField, SelectField, SubmitField,TextAreaField, PasswordField, BooleanField, RadioField, DateField
from wtforms.validators import InputRequired, DataRequired, Length,Email
from wtforms import SelectMultipleField, widgets
from markupsafe import Markup


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class newuser(FlaskForm):
    username = StringField('Username', validators= [InputRequired()])
    f_name = StringField('First Name', validators=[InputRequired()])
    l_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(),Email('Please enter a valid email adress')])
    password = PasswordField('Password', validators=[InputRequired()])
    
class BootstrapListWidget(widgets.ListWidget):
 
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = [f"<{self.html_tag} {widgets.html_params(**kwargs)}>"]
        for subfield in field:
            if self.prefix_label:
                html.append(f"<li class='list-group-item'>{subfield.label} {subfield(class_='form-check-input ms-1')}</li>")
            else:
                html.append(f"<li class='list-group-item'>{subfield(class_='form-check-input me-1')} {subfield.label}</li>")
        html.append("</%s>" % self.html_tag)
        return Markup("".join(html))
 
class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.
 
    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = BootstrapListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class GetrecomForm(FlaskForm):
    categories = MultiCheckboxField('Categories',
                                    choices=[('savory', 'Savory'), ('easy','Easy'), ('< 60 min', '< 60 min'), ('meat', 'Meat'), ('dessert', 'Dessert'), ('< 4 hour', '< 4 hour'), ('vegetable', 'Vegetable'), ('< 30 min', '< 30 min'), ('healthy', 'Healthy'), ('low cholesterol', 'Low Cholesterol'), ('inexpensive', 'Inexpensive'), ('beginner cook', 'Beginner Cook'), ('low protein', 'Low Protein'), ('fruit', 'Fruit'),
                                              ('european', 'European'), ('kid friendly', 'Kid Friendly'), ('weeknight', 'Weeknight'), ('lunch/snacks', 'Lunch/Snacks'), ('for large group', 'For Large Group'), ('one dish meal', 'One Dish Meal'), ('< 15 min', '< 15 min'), ('brunch', 'Brunch'), ('bread', 'Bread'), ('breakfast', 'Breakfast'), ('asian', 'Asian'), ('sweet', 'Sweet'), ('very low carbs', 'Very Low Carbs'), ('potluck', 'Potluck'), 
                                              ('vegan', 'Vegan'), ('christmas', 'Christmas'), ('summer', 'Summer'), ('spicy', 'Spicy'), ('winter', 'Winter'), ('high protein', 'High Protein'), ('mexican', 'Mexican'), ('quick bread', 'Quick Bread'), ('from scratch', 'From Scratch'), ('egg free', 'Egg Free'), ('toddler friendly', 'Toddler Friendly'), ('sauce', 'Sauce'), ('thanksgiving', 'Thanksgiving'), ('canadian', 'Canadian'), 
                                              ('kosher', 'Kosher'), ('bar cookie', 'Bar Cookie'), ('pie', 'Pie'), ('lactose free', 'Lactose Free'), ('drop cooky', 'Drop Cooky'), ('beverage', 'Beverage'), ('stew', 'Stew'), ('southwestern u.s.', 'Southwestern U.S.'), ('indian', 'Indian'), ('citrus', 'Citrus'), ('yeast bread', 'Yeast Bread'), ('spring', 'Spring'), ('australian', 'Australian'), ('african', 'African'), ('chinese', 'Chinese'), 
                                              ('candy', 'Candy'), ('greek', 'Greek'), ('frozen dessert', 'Frozen Dessert'), ('savory pie', 'Savory Pie'), ('broil/grill', 'Broil/Grill'), ('stir fry', 'Stir Fry'), ('southwest asia middle east', 'Southwest Asia Middle East'), ('curry', 'Curry'), ('tex mex', 'Tex Mex'), ('thai', 'Thai'), ('german', 'German'), ('camping', 'Camping'), ('caribbean', 'Caribbean'), ('cajun', 'Cajun'), 
                                              ('no cook', 'No Cook'), ('scandinavian', 'Scandinavian'), ('deep fried', 'Deep Fried'), ('south american', 'South American'), ('canning', 'Canning'), ('roast', 'Roast'), ('spanish', 'Spanish'), ('creole', 'Creole'), ('japanese', 'Japanese'), ('moroccan', 'Moroccan'), ('salad dressing', 'Salad Dressing'), ('baking', 'baking'), ('wild game', 'Wild Game'), ('scottish', 'Scottish'),
                                            ('st. patrick day', 'St. Patrick Day'), ('halloween', 'Halloween'), ('hanukkah', 'Hanukkah'), ('new zealand', 'New Zealand' ), ('stock', 'Stock'), ('birthday', 'Birthday'), ('smoothy', 'Smoothy'), ('punch beverage', 'Punch Beverage'), ('russian', 'Russian'), ('hawaiian', 'Hawaiian'), ('polish', 'Polish'), ('swedish', 'Swedish'), ('vietnamese', 'Vietnamese'), ('portuguese', 'Portuguese'), 
                                            ('hungarian', 'Hungarian'), ('swiss', 'Swiss'), ('deer', 'Deer'), ('korean', 'Korean'), ('pumpkin', 'Pumpkin'), ('south african', 'South African'), ('filipino', 'Filipino'), ('pakistani', 'Pakistani'), ('lebanese', 'Lebanese'), ('turkish', 'Turkish'), ('cuban', 'Cuban'), ('ramadan', 'Ramadan'), ('chutney', 'Chutney'), ('danish', 'Danish'), ('dutch', 'Dutch'), ('indonesian', 'Indonesian'), 
                                            ('jelly', 'Jelly'), ('no shell fish', 'No Shell Fish'), ('pennsylvania dutch', 'Pennsylvania Dutch'), ('brazilian', 'Brazilian'), ('norwegian', 'Norwegian'), ('native american', 'Native American'), ('austrian', 'Austrian'), ('shake', 'Shake'), ('cantonese', 'Cantonese'), ('belgian', 'Belgian'), ('dairy free food', 'Dairy Free Food'), ('egyptian', 'Egyptian'), ('manicotti', 'Manicotti'),
                                            ('czech', 'Czech'), ('ice cream', 'Ice Cream'), ('polynesian', 'Polynesian'), ('malaysian', 'Malaysian'), ('finnish', 'Finnish'), ('southwest asia (middle east)', 'Southwest Asia (Middle East)'), ('sourdough bread', 'Sourdough Bread'), ('peruvian', 'Peruvian'), ('high fiber', 'High Fiber'), ('puerto rican', 'Puerto Rican'), ('colombian', 'Colombian'), ('iraqi', 'Iraqi'), ('labor day', 'Labor Day'), 
                                            ('bath/beauty', 'Bath/Beauty'), ('ethiopian', 'Ethiopian'), ('memorial day', 'Memorial Day'), ('tempeh', 'Tempeh'), ('palestinian', 'Palestinian'), ('chilean', 'Chilean'), ('nepalese', 'Nepalese'), ('cambodian', 'Cambodian'), ('homeopathy/remedies', 'Homeopathy/Remedies'), ('icelandic', 'Icelandic'), ('venezuelan', 'Venezuelan'), ('ecuadorean', 'Ecuadorean'), ('hunan', 'hunan'), ('college food', 'college food'),
                                            ('nigerian', 'Nigerian'), ('costa rican', 'Costa Rican'), ('chinese new year', 'Chinese New Year'), ('guatemalan', 'Guatemalan'), ('mongolian', 'Mongolian'), ('georgian', 'Georgian'), ('honduran', 'Honduran'), ('somalian', 'Somalian'), ('sudanese', 'Sudanese')])
    submit = SubmitField('Submit')


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