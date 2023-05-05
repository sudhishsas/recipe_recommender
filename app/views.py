"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, newuser, UserProfile
from app.models import User_Profile, UserLogin
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import date, datetime

###
# Routing for your application.
###

@app.route('/')
@login_required
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
    
        username = form.username.data
        password = form.password.data

        user = UserLogin.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, password):
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True
            
            login_user(user, remember=remember_me)
            flash('Logged in successfully.', 'success')
            return redirect(url_for("home"))
        else:
            flash('Username or Password is incorrect', 'danger')
                
    flash_errors(form)          
    return render_template("login.html", form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserProfile()
    if request.method == "POST":
        if form.validate_on_submit():
            ingredients = form.ingredients.data
            allergies = form.allergies.data
            fav_categories = form.fav_categories.data
            today_date = date.today()
            
            print(ingredients, allergies, fav_categories)         
             
    return render_template("profile.html", form=form)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = newuser()

    if request.method == "POST":
        # change this to actually validate the entire form submission
        # and not just one field
        if form.validate_on_submit():
            username = form.username.data    
            f_name = form.f_name.data
            l_name = form.l_name.data
            emails = form.email.data
            password = form.password.data
            today_date = date.today()
            
            
            user = UserLogin.query.filter_by(username=username).first()
            
            if user:
                flash('username already exists', 'danger')
            elif len(username) < 4:
                flash('Please enter a user with length greater than 4', 'danger')
            elif len(f_name) < 2:
                flash('First Name must be greater than 1 character.', 'danger')
            elif len(emails) < 4:
                flash('Email must be greater than 4 characters.', 'danger')
            elif len(password) < 7:
                flash('Password length must be greater than 7 characters', 'danger')
            else:               
                new_user = UserLogin(first_name=f_name, last_name=l_name, username=username, email=emails, date=today_date, password=password)
                db.session.add(new_user)
                db.session.commit()
              
                login_user(new_user, remember=True)
                flash('Account created successfully.', 'success')
                return redirect(url_for("profile"))
            
    return render_template('sign_up.html', form=form)

        
@app.route('/about/')
@login_required
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route("/secure-page")
@login_required
def secure_page():
    return render_template("secure_page.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "danger")
    return redirect(url_for("home"))




# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserLogin.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
