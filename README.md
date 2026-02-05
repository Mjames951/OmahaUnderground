# Omaha Underground
A rebuild of planetplum.net with a chat, bandpages, user profiles and functionality, etc.

## good django tutorial to get started
check out the djangogirls tutorial or any w3schools thing.

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
this install the required python packages into your virtual environment folder:
    pip install -r requirements.txt
### 4. Add the name of your venv folder to the .gitignore if it's not named 'venv'
'venv' is already in .gitignore so don't worry about that
### 5. create your own '.env' in the root directory using '.env.example' as a template
this will give the settings access to required variables (mostly just DEBUG). Feel free to change them as '.env' is ignored
### 6. Run migrations real quick to setup the SQLite database
    python manage.py makemigrations
    python manage.py migrate
### 7. Create your own SuperUser to use the site as the root admin
    python manage.py createsuperuser
### 8 begin running the site
    python manage.py runserver
### 9 login to your superuser
click on 'login' in the top right of the screen and put in the credentials you used to create your superuser

# During Development
### Run server
    python manage.py runserver
### any changes to a model.py file changes the database and will need a migration
    python manage.py makemigrations
### apply new migrations
    python manage.py migrate
### if you add any packages using 'pip install' you must add them to 'requirements.txt'
    pip freeze > requirements.txt
### if someone else adds a new package and it's reflected in 'requirementst.txt' then install it
    pip install -r requirements.txt
### if you get the database in an unfixable state, completely reset it (command from django_extensions)
    python manage.py reset_db

# information on the setup
## the main project is "planetapplication"
This is the root of the website, has the settings and all URLs go through it first.
## the main application is "planetplum"
This is the main application and houses all the Omaha Underground main functionality
## the user application is "users"
This manages the user/account aspect of things. Custom User Model and Authentication.
## the chat application is "chat"
The Forum

### Each application has a models.py file
This file defined the database schema of that application. For example, the 'planetplum' application defines that a show has an image(poster) date, venue, name, price, time, and an 'approved' boolean. 

### planetplum/base.html is the root template in which most every other template extends from. 
Look into django templates to learn how this works.

## views.py in each application do most of the logic
Views are the functions that take data from the database, mess with it, and then chose a 'template' (html file) to serve the data with.
### superviews under 'planetplum' does most of the CRUD logic
any other views mostly deal with reading data or are inclusive to their application

### urls.py maps URLs to view functions

### put reusable html/javascript code under 'planetplum/templates/planetplum/widgets'

# CSS Rules
## This site uses mobile-first design principle
You'll notice in the CSS files toward the bottom we specify media queries for when the user has a larger screen. This makes it so the default computation for each webpage is for a mobile device. This speeds things up for mobile users as PC's can handle the extra computation. Design the elements for mobile first, and then specify the PC changes under the media-queries please.
## all CSS sizing needs to be related to rem or %.
### nothing can be defined using px or vw/vh unless it is the :root
This is to make sure that the site is responsive and looks about the same for every size of screen. Plus I think it's easier to manage. The rem value on the root changes with respect to the screen width until the user's screen is too large at which it is fixed.
## This site uses a 2 color design
### they are var(--textcolor) and var(--primary)
The textcolor is based on the user's darkmode preference (white for darkmode, black default) and the primary is the color that the user choses the site to be. The default light blue color for users was chosen to make text readable for both light and dark modes at first.