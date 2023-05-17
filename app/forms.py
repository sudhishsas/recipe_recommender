from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField,IntegerField, SelectField, SubmitField,TextAreaField, PasswordField, BooleanField, RadioField, DateField, SelectMultipleField, widgets
from wtforms.validators import InputRequired, DataRequired, Length,Email
from wtforms import SelectMultipleField, widgets
from markupsafe import Markup


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
    num = SelectField('Number of Recommendations', choices = [('5','5'),('10', '10'),('15','15'),('20','20'),('25','25'),('30','30'), ('35','35'), ('40', '40') ])
    ingredients = TextAreaField('Ingredients')
    
    
    countries = MultiCheckboxField('Cuisine', choices = [('european', 'European'), ('asian', 'Asian'), ('mexican', 'Mexican'), ('canadian', 'Canadian'), ('indian', 'Indian'), ('australian', 'Australian'), ('african', 'African'), ('chinese', 'Chinese'), ('greek', 'Greek'), ('thai', 'Thai'), ('german', 'German'), ('cajun', 'Cajun'), ('scandinavian', 'Scandinavian'), ('spanish', 'Spanish'), ('japanese', 'Japanese'), ('moroccan', 'Moroccan'),
                                                          ('scottish', 'Scottish'), ('russian', 'Russian'), ('hawaiian', 'Hawaiian'), ('polish', 'Polish'), ('swedish', 'Swedish'), ('vietnamese', 'Vietnamese'), ('portuguese', 'Portuguese'), ('hungarian', 'Hungarian'), ('swiss', 'Swiss'), ('korean', 'Korean'), ('filipino', 'Filipino'), ('pakistani', 'Pakistani'), ('lebanese', 'Lebanese'), ('turkish', 'Turkish'), ('cuban', 'Cuban'), ('ramadan', 'Ramadan'),
                                                           ( 'danish',  'Danish'), ('dutch', 'Dutch'), ('indonesian', 'Indonesian'), ('brazilian', 'Brazilian'), ('norwegian', 'Norwegian'), ('austrian', 'Austrian'), ('cantonese', 'Cantonese'), ('belgian', 'Belgian'), ('egyptian', 'Egyptian'), ('czech', 'Czech'), ('polynesian', 'Polynesian'), ('malaysian', 'Malaysian'), ('finnish', 'Finnish'), ('peruvian', 'Peruvian'), ('colombian', 'Colombian'),
                                                            ('iraqi', 'Iraqi'), ('ethiopian', 'Ethiopian'), ('palestinian', 'Palestinian'), ('chilean', 'Chilean'), ('nepalese', 'Nepalese'), ('cambodian', 'Cambodian'), ('icelandic', 'Icelandic'), ('venezuelan', 'Venezuelan'), ('ecuadorean', 'Ecuadorean'), ('nigerian', 'Nigerian'), ('guatemalan', 'Guatemalan'), ('mongolian', 'Mongolian'), ('georgian', 'Georgian'), ('honduran', 'Honduran'), ('somalian', 'Somalian'),
                                                              ('sudanese', 'Sudanese'),('southwestern u.s.', 'Southwestern U.S.'), ('southwest asia middle east', 'Southwest Asia Middle East' ), ('caribbean', 'Caribbean'), ('south american', 'South American'), ('native american', 'Native American'), ('pennsylvania dutch', 'Pennsylvania Dutch'), ('costa rican', 'Costa Rican'), ('south african', 'South African'), ('cantonese', 'Cantonese'), ('new zealand', 'New Zealand'), ('hunan', 'Hunan')] )
    time = MultiCheckboxField('Time', choices =[('< 60 min', '< 60 min'), ('< 4 hour', '< 4 hour'), ('< 30 min', '< 30 min'), ('< 15 min', '< 15 min') ] )
    events = MultiCheckboxField('Events', choices =[('weeknight', 'Weeknight'), ('brunch', 'Brunch'), ('potluck', 'Potluck'), ('camping', 'Camping'),( 'christmas', 'Christmas'), ('thanksgiving', 'Thanksgiving'), ('st. patrick day', 'St. Patrick day'), ('halloween', 'Halloween'), ('hanukkah', 'Hanukkah') ,('labor day', 'Labor day'), ('memorial day', 'Memorial day'), ('chinese new year', 'Chinese New Year')])
    preptype = MultiCheckboxField('Preperation Type', choices =[ ('from scratch', 'From scratch'), ('broil/grill', 'Broil/Grill'), ('stir fry', 'Stir Fry'), ('no cook', 'No Cook'), ('deep fried', 'Deep Fried'), ('canning', 'Canning'), ('roast', 'Roast'), ('baking', 'Baking')])
    diff = MultiCheckboxField('Difficulty', choices =[('beginner cook', 'Beginner Cook'), ('kid friendly', 'Kid Friendly'), ('toddler friendly', 'Toddler Friendly'), ('easy', 'Easy')])
    misc = MultiCheckboxField('Misc', choices =[('bath/beauty', 'Bath/Beauty'), ('low cholesterol', 'Low Cholesterol'), ('inexpensive', 'Inexpensive'), ('tex mex', 'Tex Mex'), ('low protein','Low Protein'), ('manicotti', 'Manicotti'), ('ice cream', 'Ice Cream'), ('chutney', 'Chutney'), ('homeopathy/remedies', 'Homeopathy/Remedies'), ('college food', 'College Food'),('no shell fish', 'No Shell Fish'), ('high fiber', 'High Fiber'),('jelly', 'Jelly'),('wild game', 'Wild Game'), ('creole', 'Creole'), ('very low carbs', 'Very Low Carbs'), ('high protein', 'High Protein'),
                                                 ('egg free', 'Egg Free'), ('lactose free', 'Lactose Free')])
    fotype= MultiCheckboxField('Food Type', choices =[('savory', 'Savory'), ('meat', 'Meat'), ('dessert', 'Dessert'), ('vegetable', 'Vegetable'), ('fruit', 'Fruit'), ('healthy', 'Healthy'), ('vegan', 'Vegan'), ('spicy', 'Spicy'), ('quick bread', 'Quick Bread'), ('curry', 'Curry'), ('bread', 'Bread'), ('breakfast', 'Breakfast'), ('sweet', 'Sweet'), ('sauce', 'Sauce'), ('kosher', 'Kosher'), ('one dish meal', 'One Dish Meal'),('bar cookie', 'Bar Cookie'),
                                                       ('pie', 'Pie'), ('drop cooky', 'Drop Cooky'), ('beverage', 'Beverage'), ('stew', 'Stew'), ('lunch/snacks', 'Lunch/Snacks'), ('citrus', 'Citrus'), ('yeast bread', 'Yeast Bread'), ('candy', 'Candy'), ('frozen dessert', 'Frozen Dessert'), ('savory pie', 'Savory Pie'), ('salad dressing', 'Salad Dressing'), ('stock', 'Stock'), ('shake', 'Shake'),( 'sourdough bread',  'Sourdough Bread'), ('smoothy', 'Smoothy'), ('punch beverage', 'Punch Beverage')])
    seas = MultiCheckboxField('Seasonal', choices =[('summer', 'Summer'),( 'winter',  'Winter'),('spring', 'Spring')])
    submit = SubmitField('Submit')

class getprofileinfo(FlaskForm):
    ingredients = TextAreaField('Ingredients')
    
    countries = MultiCheckboxField('Cuisine', choices = [('european', 'European'), ('asian', 'Asian'), ('mexican', 'Mexican'), ('canadian', 'Canadian'), ('indian', 'Indian'), ('australian', 'Australian'), ('african', 'African'), ('chinese', 'Chinese'), ('greek', 'Greek'), ('thai', 'Thai'), ('german', 'German'), ('cajun', 'Cajun'), ('scandinavian', 'Scandinavian'), ('spanish', 'Spanish'), ('japanese', 'Japanese'), ('moroccan', 'Moroccan'),
                                                          ('scottish', 'Scottish'), ('russian', 'Russian'), ('hawaiian', 'Hawaiian'), ('polish', 'Polish'), ('swedish', 'Swedish'), ('vietnamese', 'Vietnamese'), ('portuguese', 'Portuguese'), ('hungarian', 'Hungarian'), ('swiss', 'Swiss'), ('korean', 'Korean'), ('filipino', 'Filipino'), ('pakistani', 'Pakistani'), ('lebanese', 'Lebanese'), ('turkish', 'Turkish'), ('cuban', 'Cuban'), ('ramadan', 'Ramadan'),
                                                           ( 'danish',  'Danish'), ('dutch', 'Dutch'), ('indonesian', 'Indonesian'), ('brazilian', 'Brazilian'), ('norwegian', 'Norwegian'), ('austrian', 'Austrian'), ('cantonese', 'Cantonese'), ('belgian', 'Belgian'), ('egyptian', 'Egyptian'), ('czech', 'Czech'), ('polynesian', 'Polynesian'), ('malaysian', 'Malaysian'), ('finnish', 'Finnish'), ('peruvian', 'Peruvian'), ('colombian', 'Colombian'),
                                                            ('iraqi', 'Iraqi'), ('ethiopian', 'Ethiopian'), ('palestinian', 'Palestinian'), ('chilean', 'Chilean'), ('nepalese', 'Nepalese'), ('cambodian', 'Cambodian'), ('icelandic', 'Icelandic'), ('venezuelan', 'Venezuelan'), ('ecuadorean', 'Ecuadorean'), ('nigerian', 'Nigerian'), ('guatemalan', 'Guatemalan'), ('mongolian', 'Mongolian'), ('georgian', 'Georgian'), ('honduran', 'Honduran'), ('somalian', 'Somalian'),
                                                              ('sudanese', 'Sudanese'),('southwestern u.s.', 'Southwestern U.S.'), ('southwest asia middle east', 'Southwest Asia Middle East' ), ('caribbean', 'Caribbean'), ('south american', 'South American'), ('native american', 'Native American'), ('pennsylvania dutch', 'Pennsylvania Dutch'), ('costa rican', 'Costa Rican'), ('south african', 'South African'), ('cantonese', 'Cantonese'), ('new zealand', 'New Zealand'), ('hunan', 'Hunan')] )
    time = MultiCheckboxField('Time', choices =[('< 60 min', '< 60 min'), ('< 4 hour', '< 4 hour'), ('< 30 min', '< 30 min'), ('< 15 min', '< 15 min') ] )
    events = MultiCheckboxField('Events', choices =[('weeknight', 'Weeknight'), ('brunch', 'Brunch'), ('potluck', 'Potluck'), ('camping', 'Camping'),( 'christmas', 'Christmas'), ('thanksgiving', 'Thanksgiving'), ('st. patrick day', 'St. Patrick day'), ('halloween', 'Halloween'), ('hanukkah', 'Hanukkah') ,('labor day', 'Labor day'), ('memorial day', 'Memorial day'), ('chinese new year', 'Chinese New Year')])
    preptype = MultiCheckboxField('Preperation Type', choices =[ ('from scratch', 'From scratch'), ('broil/grill', 'Broil/Grill'), ('stir fry', 'Stir Fry'), ('no cook', 'No Cook'), ('deep fried', 'Deep Fried'), ('canning', 'Canning'), ('roast', 'Roast'), ('baking', 'Baking')])
    diff = MultiCheckboxField('Difficulty', choices =[('beginner cook', 'Beginner Cook'), ('kid friendly', 'Kid Friendly'), ('toddler friendly', 'Toddler Friendly'), ('easy', 'Easy')])
    misc = MultiCheckboxField('Misc', choices =[('bath/beauty', 'Bath/Beauty'), ('low cholesterol', 'Low Cholesterol'), ('inexpensive', 'Inexpensive'), ('tex mex', 'Tex Mex'), ('low protein','Low Protein'), ('manicotti', 'Manicotti'), ('ice cream', 'Ice Cream'), ('chutney', 'Chutney'), ('homeopathy/remedies', 'Homeopathy/Remedies'), ('college food', 'College Food'),('no shell fish', 'No Shell Fish'), ('high fiber', 'High Fiber'),('jelly', 'Jelly'),('wild game', 'Wild Game'), ('creole', 'Creole'), ('very low carbs', 'Very Low Carbs'), ('high protein', 'High Protein'),
                                                 ('egg free', 'Egg Free'), ('lactose free', 'Lactose Free')])
    fotype= MultiCheckboxField('Food Type', choices =[('savory', 'Savory'), ('meat', 'Meat'), ('dessert', 'Dessert'), ('vegetable', 'Vegetable'), ('fruit', 'Fruit'), ('healthy', 'Healthy'), ('vegan', 'Vegan'), ('spicy', 'Spicy'), ('quick bread', 'Quick Bread'), ('curry', 'Curry'), ('bread', 'Bread'), ('breakfast', 'Breakfast'), ('sweet', 'Sweet'), ('sauce', 'Sauce'), ('kosher', 'Kosher'), ('one dish meal', 'One Dish Meal'),('bar cookie', 'Bar Cookie'),
                                                       ('pie', 'Pie'), ('drop cooky', 'Drop Cooky'), ('beverage', 'Beverage'), ('stew', 'Stew'), ('lunch/snacks', 'Lunch/Snacks'), ('citrus', 'Citrus'), ('yeast bread', 'Yeast Bread'), ('candy', 'Candy'), ('frozen dessert', 'Frozen Dessert'), ('savory pie', 'Savory Pie'), ('salad dressing', 'Salad Dressing'), ('stock', 'Stock'), ('shake', 'Shake'),( 'sourdough bread',  'Sourdough Bread'), ('smoothy', 'Smoothy'), ('punch beverage', 'Punch Beverage')])
    seas = MultiCheckboxField('Seasonal', choices =[('summer', 'Summer'),( 'winter',  'Winter'),('spring', 'Spring')])
    

    alergies = MultiCheckboxField('Allergies', choices =[('Milk Allergy', 'Milk Allergy'), ('Egg Allergy', 'Egg Allergy'), ('Tree nut Allergy', 'Tree Nut Allergy'), ('Peanut Allergy', 'Peanut Allergy'), ('ShellFish Allergy', 'ShellFish Allergy'), ('Wheat Allergy', 'Wheat Allergy'), ('Soy Allergy', 'Soy Allergy'), ('Fish Allergy', 'Fish Allergy'), ('Sesame Allergy', 'Sesame Allergy')] )
    submit = SubmitField('Submit')

    

    
   
   
