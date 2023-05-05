# Recipe recommender system

Code for recipe recommender system

# Create database
# make the database in postgress sql shell open the psql shell
$ create user "reciperecom";
$ create database "reciperecom";
$ #\password reciperecom  #Password123
$ alter database reciperecom owner to reciperecom;

# setting up the new env
copy the .env.sample and edit the folowinmg to be like what is below and also remane the file to .env

FLASK_ENV=development
FLASK_RUN_PORT=8080
FLASK_RUN_HOST=0.0.0.0
DATABASE_URL=postgresql://reciperecom:Password123@localhost/reciperecom
SECRET_KEY= ak%jh%asd9#!ad8@*^asd%fa$

# after adding data to the database you can view the data by opening the psql shell and running the following commands after logging in.
$
$ \c reciperecom #allows you to enter the specific database
$ \ dt   # shows the tables in the database
$ select * from "insert table name  here";  #to see the data uploaded to the database remove the ("") when typing in the specific table.

# To begin using this app you can do the following:

1. Clone the repository to your local machine.
2. Create a Python virtual environment e.g. `vpython -m venv venv` (You may need to use `python3` instead)
3. Enter the virtual environment using `source venv/bin/activate` (or `.\venv\Scripts\activate` on Windows)
4. Install the dependencies using Pip. e.g. `pip install -r requirements.txt`. Note: Ensure you have PostgreSQL already installed and a database created.
5. Edit the `app/__init__.py` file and enter your database credentials and database name.
6. Run the migrations by typing `python manage.py db upgrade`
7. Start the development server using `python run.py`.

## Separate Config file

I have included a separate config file `app/config.py` that can be used for setting up
configuration for different environments e.g. Development and Production

Using this separate config file will also require you to set environment variables on your local computer or server at the command line. For example on Linux or MacOS:

```bash
export SECRET_KEY="my-super-secret-key"
export DATABASE_URL="postgresql://yourusername:yourpassword@localhost/databasename"
```

Or on Windows:

```powershell
set SECRET_KEY="my-super-secret-key"
set DATABASE_URL="postgresql://yourusername:yourpassword@localhost/databasename"
```

If using PowerShell on Windows try the following:

```powershell
$env:SECRET_KEY="YourRandomSecretKey"
$env:DATABASE_URL="postgresql://yourusername:yourpassword@localhost/databasename"
```

And on Heroku:

```bash
heroku config:set SECRET_KEY="my-super-secret-key"
heroku config:set DATABASE_URL="postgresql://yourusername:yourpassword@localhost/databasename"
```
