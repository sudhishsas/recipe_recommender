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
from app.forms import LoginForm, newuser,  GetrecomForm
from app.models import User_Profile, UserLogin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime
from autocorrect import Speller
from tkinter import *
from spellchecker import SpellChecker
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import ast
from app.getrecomendations import get_recs
from app.words_parser import allergy_checker

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

        user_info = UserLogin.query.get_or_404(user_id)
        userupinfo = User_Profile.query.get_or_404(user_id)

        #gets the users profile info 
        useringre = list(getuseringred(user_id).ingredients.split(","))
        user_cat = list(getuseringred(user_id).fav_categories.split(","))
        useral = list(getuseringred(user_id).alergies.split(","))
        usercpyin = useringre.copy()
        usercpycat = user_cat.copy()
        usercpyallr = useral.copy()

        #gets users personal info
        fname = user_info.first_name
        lname = user_info.last_name
        username = user_info.username
        email = user_info.email


        if request.method == "POST" and form.validate_on_submit():

            ingredients = request.form.getlist('ingredient')
            ingre = request.form['ingredients']

            #putting the ingredients into a list
            ingre = list(ingre.split(","))
            ingre = list(i.lstrip() for i in ingre)
            print("ingredients after strip", ingre)

            #checks if the words entered are spelled correctly (spell checker)
            newingre = []
            for x in ingre:
                if corrector.correction(x) != "i":
                    if corrector.correction(x) == None:
                        newingre.append(x)
                    else:
                        newingre.append(corrector.correction(x))
            ingre = newingre.copy()
            print("check ingredients",ingre, usercpyin)
            
            if ingredients == []:
                if ingre == []:
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
            print("this is ingredients", newingre)
            #gets the categories and creates a list of categories
            category = request.form.getlist('category')
            prept = request.form.getlist('preptype')
            time = request.form.getlist('time')
            dif = request.form.getlist('diff')
            ftype = request.form.getlist('fotype')
            event = request.form.getlist('events')
            sse = request.form.getlist('seas')
            msc = request.form.getlist('misc')

            #print("prept, time, dif, ftype, event, sse, msc",  prept, time, dif, ftype, event, sse, msc)
            categor = prept+ time+ dif + ftype+ event+sse+msc
            categor = list(i.lstrip() for i in categor)
            
            if category == []:
                if categor == []:
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

            #reteive the allergy input and check for spelling errors
            allergies = request.form.getlist('alergy')
            allergi = request.form.getlist('alergies')
        
            print("th isi aletgies", allergi, allergies)

            if allergies == []:
                if allergi == []:
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
                print("seen it",allergi ,usercpyallr)
                newallergi = ','.join(allergi + usercpyallr)
                
                if newallergi !='':
                    if newallergi[0] == ",":
                        newallergi =  newallergi[1:]
            
            print(newallergi)
            #adds the new information to there assigned column 
            userupinfo.ingredients = newingre
            userupinfo.alergies = newallergi
            userupinfo.fav_categories = newcat
            userupinfo.date_added = today_date

            #updates the database with the new information 
            db.session.commit()
            flash("Updated Profile Successfully :) ",'success')

            #clears the form text feilds empty
            form.ingredients.data = ""
            form.alergies.data= ""

            return redirect(url_for('profile')) 
        return render_template('profile.html', form = form , fname = fname , lname = lname , email = email, username= username, user_id = user_id, useringre = useringre, user_cat = user_cat, useral = useral) 
    else:
        return redirect(url_for("login"))
    """Render website's profile page."""

@app.route('/home')
@login_required
def home():
    if "user_id" in session:
        user_id = session["user_id"]
        user_info = UserLogin.query.get_or_404(user_id)
        #gets users personal info
        fname = user_info.first_name
        lname = user_info.last_name
        username = user_info.username
        email = user_info.email
        rnames = []
        
        if "specurecom" in session:
            user_id = session["user_id"]
            
            prevrecom = session["specurecom"]
            
        
            if prevrecom[0] == user_id:
                
                recom = prevrecom[1]
                rnames = recom['recipe_name'].tolist()

        return render_template('home.html', user_id = user_id, rnames= rnames, fname= fname, lname =lname, username= username, email = email)

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
            print("came to the submit ")
            
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
                print("came here")
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

        #gets the users saved ingredients form the user profile 
        useringre = list(getuseringred(user_id).ingredients.split(","))
        rnames = []
        prnames= []

        if request.method == "POST":

            #gets the information from the form for ingredients
            ingredients = request.form.getlist('ingredient')
            ingre = request.form['ingredients']

            #putting the ingredients into a list
            ingre = list(ingre.split(","))
            ingre = list(i.lstrip() for i in ingre)
            print("ingredients after strip", ingre)
            

            newingre = []
            # Spell checking ingredients if the spell checker can not spell check then it would leave the word as is
            for x in ingre:
                if corrector.correction(x) != "i":
                    if corrector.correction(x) == None:
                        newingre.append(x)
                    else:
                        newingre.append(corrector.correction(x))
            ingre = newingre.copy()
            
            if ingre == ['']:
                ingreinput = ','.join(ingredients)
            else:
                #remove any duplicate ingredients if the user had given the same ingredients as selected 
                check = list(dict.fromkeys(ingre + ingredients))
                print(check)
                ingreinput = ','.join(check)
            #if the user does not enter or selects any ingredients the recommender cannot be used so a error message is displayed to the user
            if ingreinput == "":
                flash('Ingredients must be selected or added in order to get a recommendation', 'danger')
                return redirect(url_for('getrecommendation'))
            
            print("this is the final input", ingreinput)

            #gets all the categories from each type feild 
            categor = request.form.getlist('categories')
            prept = request.form.getlist('preptype')
            time = request.form.getlist('time')
            dif = request.form.getlist('diff')
            ftype = request.form.getlist('fotype')
            event = request.form.getlist('events')
            sse = request.form.getlist('seas')
            msc = request.form.getlist('misc')

            #print("prept, time, dif, ftype, event, sse, msc",  prept, time, dif, ftype, event, sse, msc)
            # adds all the categories to a single list
            categor = prept+ time+ dif + ftype+ event+sse+msc
            categor = list(i.lstrip() for i in categor)
            
            print("caterory ", categor)

            #gets teh number of recommendations the user selected 
            num = request.form['num']

            print("this is the number list", num)
            #calling the get_recs function to get the recommendations
            recs = get_recs(ingreinput, int(num), categor)
            
            #checks if the session was created or has any information prior to the new recommendations this session is used to show the user there previous recommendations
            if "specurecom" in session:
                session.pop("specusrecom", None)

            #this session is used like the first session but this one is used to hold the current recommendations, this clears the session to accept the new recommendations
            if "recommendations" in session:
                session.pop("recommendations", None)

            # adding info to the sessions for current and prev recommendations
            #prev
            session["specurecom"] = [user_id, recs]
            #current
            session["recommendations"] = recs


            #checks if the recommendation session was made and has info before getting recommendation recipe names
            if "user_id" in session and "recommendations" in session:
                user_id = session["user_id"]
                recoms = session["recommendations"]

                #gets the recipe names
                rnames = recoms['recipe_name'].tolist()
            
            return render_template('getrecom.html', form = form , user_id = user_id, useringre = useringre, rnames= rnames, selcat = categor, prnames= prnames)
        
        #if theuser were to leave the recommendation page and come back to it this will check for prev recommendations and return them to the user 
        if "specurecom" in session:
            user_id = session["user_id"]
            prevrecom = session["specurecom"]

            #checks if the user id match 
            if prevrecom[0] == user_id:
                
                recom = prevrecom[1]
                prnames = recom['recipe_name'].tolist()

        return render_template('getrecom.html', form = form , user_id = user_id, useringre = useringre, rnames= rnames, prnames= prnames) 
    else:
        return redirect(url_for("login"))

@app.route("/viewrecipe/<recipeName>")
@login_required
def viewrecipes(recipeName):
    
    if "user_id" in session and "recommendations" in session:
        user_id = session["user_id"]
        recoms = session["recommendations"]
    
        recings = recoms['ingredients'].tolist()
        reccats = recoms['category'].tolist()
        indcheck = recoms['recipe_name'].tolist()
        recinstructs =recoms['recipe_instructions'].tolist()
        useral = list(getuseringred(user_id).alergies.split(","))

        count = 0
        recing = []
        reccat = []

        recinstruct = ''
        #check if the recipe name matches and collects the information for that recipe
        for i in indcheck:
            
            if i == recipeName:
                recing = ast.literal_eval(recings[count])
                reccat = ast.literal_eval(reccats[count])
                recinstruct = recinstructs[count]
            count+=1
        #checks for any of the users allergies relating to the current recipe ingredients
        checkal = allergy_checker(recing)
        finalal = []
        for i in checkal:
            if i in useral:
                finalal.append(i)
        if finalal != []:
            flash('This recipe contains foods that you may be allergic to: Allergies ' + ','.join(finalal)  , 'danger')
        
        
        i = recinstruct.replace("]", "")
        recinstruct = i.replace("[", "")
        recinstruct= list(recinstruct.split(","))

        return render_template("viewrecipe.html", rname = recipeName, recing = recing, reccat = reccat, recinstruct = recinstruct)
    
    
    return redirect(url_for("login"))

@app.route("/secure-page")
@login_required
def secure_page():
    return render_template("secure_page.html")


@app.route("/logout")
@login_required
def logout():
    session.pop("specusrecom", None)
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
