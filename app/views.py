"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from flask_session import Session
from app.forms import LoginForm, newuser,  GetrecomForm, getprofileinfo
from app.models import User_Profile, UserLogin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime
from autocorrect import Speller
from tkinter import *
from spellchecker import SpellChecker

from app.getrecomendations import get_recs

corrector = SpellChecker()
spell = Speller(lang='en')


###
# Routing for the application.
###



@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    if "user_id" in session:
        user_id = session["user_id"]
        form = getprofileinfo()
        today_date = date.today()

        print("this is the front end print",getuseringred(user_id).id)

        user_info = User_Profile.query.get_or_404(user_id)
        useringre = list(getuseringred(user_id).ingredients.split(","))
        user_cat = list(getuseringred(user_id).fav_categories.split(","))
        useral = list(getuseringred(user_id).alergies.split(","))
        usercpyin = useringre.copy()
        usercpycat = user_cat.copy()
        usercpyallr = useral.copy()

        
        if request.method == "POST" and form.validate_on_submit():

            ingredients = request.form.getlist('ingredient')
            ingre = request.form['ingredients']
            
            ingre = list(ingre.split(","))
            ingre = list(i.lstrip() for i in ingre)
            ingre = list(corrector.correction(i) for i in ingre)
            
            if ingredients == []:
                if ingre == ['']:
                    
                    if ingre in usercpyin:
                        usercpyin.remove(ingre)
                    newingre = ','.join(usercpyin)
                else:
                    for i in ingre:
                        if i in usercpyin:
                            usercpyin.remove(i)
                        newingre = ','.join(ingre + usercpyin)

            else:
                for i in ingredients:
                    if i in usercpyin:
                        usercpyin.remove(i)
                for s in ingre:
                    if s in usercpyin:
                        usercpyin.remove(s)
                
                newingre = ','.join(ingre + usercpyin)
                if newingre[0] == ",":
                    newingre =  newingre[1:]
            
            category = request.form.getlist('category')
            categor = request.form.getlist('categories')
            categor = list(i.lstrip() for i in categor)

            if category == []:
                if category == []:
                    newcat = ','.join(usercpycat)
                else:
                    for i in categor:
                        if i in usercpycat:
                            usercpycat.remove(i)
                    newcat = ','.join(categor+usercpycat)

            else:
                for i in category:
                    if i in usercpycat:
                        usercpycat.remove(i)
                for t in categor:
                    if t in usercpycat:
                        usercpycat.remove(t)
                newcat = ','.join(categor + usercpycat)      

            allergies = request.form.getlist('alergy')
            allergi = request.form['alergies']
            allergi = list(allergi.split(","))
            allergi = list(i.lstrip() for i in allergi)
            allergi = list(corrector.correction(i) for i in allergi)
            print("th isi aletgies", allergi, allergies)
            if allergies == []:
                if allergi == ['']:
                    if allergi in usercpyallr:
                        usercpyin.remove(allergi)
                    newallergi = ','.join(usercpyallr)
                else:
                    for i in allergi:
                        if i in usercpyallr:
                            usercpyallr.remove(i)
                        newallergi = ','.join(allergi + usercpyallr)

            else:
                for i in allergies:
                    if i in usercpyallr:
                        usercpyallr.remove(i)
                for s in allergi:
                    if s in usercpyallr:
                        usercpyallr.remove(s)
                newallergi = ','.join(allergi + usercpyallr)
                if newallergi[0] == ",":
                    newallergi =  newallergi[1:]
            
            user_info.ingredients = newingre
            user_info.alergies = newallergi
            user_info.fav_categories = newcat
            user_info.date_added = today_date
            db.session.commit()
            flash("Updated Profile Successfully :) ",'success')
            form.ingredients.data = ""
            form.alergies.data= ""
            return redirect(url_for('profile')) 
        return render_template('profile.html', form = form , user_id = user_id, useringre = useringre, user_cat = user_cat, useral = useral) 
    else:
        return redirect(url_for("login"))
    """Render website's profile page."""

@app.route('/home')
@login_required
def home():
    if "user_id" in session:
        user_id = session["user_id"]
        form = getprofileinfo()
        return render_template('home.html', user_id = user_id) 
    else:
        return redirect(url_for("login"))
    """Render website's profile page."""

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
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
            session["user_id"] = user.id
            flash('Logged in successfully.', 'success')
            return redirect(url_for("profile"))
        else:
            flash('Username or Password is incorrect', 'danger')
                
    flash_errors(form)          
    return render_template("login.html", form=form)



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
            t = UserLogin.query.filter_by(email= emails).all()
            print("this is ", t)
            if user or t:
                flash('username already exists', 'danger')
            elif len(username) < 4:
                flash('Please enter a user with length greater than 4', 'danger')
            elif len(f_name) < 2:
                flash('First Name must be greater than 1 character.', 'danger')
            elif t:
                flash('Email already exist in data base', 'danger')
            elif len(emails) < 4:
                flash('Email must be greater than 4 characters.', 'danger')
            elif len(password) < 7:
                flash('Password length must be greater than 7 characters', 'danger')
            else:     
                         
                new_user = UserLogin(first_name=f_name, last_name=l_name, username=username, email=emails, date=today_date, password=password)
                db.session.add(new_user)
                db.session.commit()
                tr = UserLogin.query.filter_by(email= emails).all()
                print(tr)
                newprofile = User_Profile( id = tr[-1].id  , ingredients ="" , alergies="" , fav_categories = "" , date_added = today_date)
                db.session.add(newprofile)
                db.session.commit()

                login_user(new_user, remember=True)
                session["user_id"] = tr[-1].id
                flash('Account created successfully.', 'success')
                return redirect(url_for("profile"))
            
    return render_template('sign_up.html', form=form)

        
@app.route('/about/')
@login_required
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route("/getrecommendation", methods =["GET","POST"])
@login_required
def getrecommendation():
    if "user_id" in session:
        user_id = session["user_id"]
        form = GetrecomForm()
        print("this is the front end print",getuseringred(user_id).id)
        
        useringre = list(getuseringred(user_id).ingredients.split(","))
    
        if request.method == "POST":
            
            ingredients = request.form.getlist('ingredient')
            ingre = request.form['ingredients']
            ingre = list(ingre.split(","))
            ingre = list(i.lstrip() for i in ingre)
            ingre = list(corrector.correction(x) for x in ingre)
            
            if ingre == ['i']:
                ingreinput = ','.join(ingredients)
            else:
                check = list(dict.fromkeys(ingre + ingredients))
                ingreinput = ','.join(check)
            if ingreinput == "":
                flash('Ingredients must be selected or added in order to get a recommendation', 'danger')
                return redirect(url_for('getrecommendation'))
            
            print("this is the final input", ingreinput)

            categor = request.form.getlist('categories')
            categor = list(i.lstrip() for i in categor)
            
            print("caterory ", categor)

            num = request.form['num']

            print("this is the number list",num)
            recoms = get_recs(ingreinput, int(num), categor)
            print(recoms)
            print(type(recoms))
            print(type(recoms['RecipeId'].tolist()))

            return redirect(url_for('getrecommendation'))
        return render_template('getrecom.html', form = form , user_id = user_id, useringre = useringre) 
    else:
        return redirect(url_for("login"))



@app.route("/secure-page")
@login_required
def secure_page():
    return render_template("secure_page.html")


@app.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    logout_user()
    flash("You have been logged out.", "danger")
    return redirect(url_for("login"))

def getuseringred(user_id):
    result = User_Profile.query.get_or_404(user_id)
    return result



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
