# Recipe recommender system

Code for recipe recommender system

To begin using this app you can do the following:

1. Clone the repository to your local machine.
2. Create a Python virtual environment e.g. `python -m venv venv` (You may need to use `python3` instead)
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
