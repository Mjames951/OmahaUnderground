# Planet Application
A rebuild of planetplum.net with a chat, bandpages, user profiles and functionality, etc.

# Setting up your environment (for contributors)
### 1. Remember to create your own virtual environment with Python 3.11
    pip install virtualenv
    virtualenv -p python3.11 venv
'venv' is the name of your virtual environment folder. You can change that if you want
### 2. ALWAYS ACTIVATE YOUR VIRTUAL ENVIRONMENT BEFORE DOING ANYTHING
windows:
    venv\Scripts\activate 
### 3. Then install required modules
make sure that requirements.txt is in your current directory
    pip install -r requirements.txt
this install the required python packages into your virtual environment folder
### 4. Add the name of your venv folder to the .gitignore if it's not named 'venv'
'venv' is already in .gitignore so don't worry about that
### 5. Run migrations real quick so setup the database
    python manage.py makemigrations
    python manage.py migrate
### 6. Create your own SuperUser to access /admin page: http://127.0.0.1:8000/admin
    python manage.py createsuperuser
Now you're good to go

### Run server
    python manage.py runserver

## information on the setup
### the main project is "planetapplication"
### the main application is "planetplum"
### the user application is "users"
### the chat application is "chat"

# other useful stuff
### if you install any new packages using pip:
check requirements.txt is in your current directory
    pip freeze > requirements.txt
this will allow other people to see and install the new package
### if you notice changes in requirements.txt
install new packages
    pip install -r requirements.txt
### if your personal database gets FUCKED UP
wipe the whole thing
    python manage.py reset_db
this is available through the django_extensions package and doesn't come prepackaged with django