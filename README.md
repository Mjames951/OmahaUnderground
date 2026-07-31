# Omaha Underground
### a DIY, Open Source Hub for the Omaha, NE music scene!
## Setup
This README goes through the bare-bones setup.
There is an alternative setup that features a mail and PostGreSQL server in the `AlternativeSetup` folder

**Begin by cloning the repository and entering the folder**
```
git clone https://github.com/Mjames951/OmahaUnderground.git
cd OmahaUnderground
```

**Next, create and activate a virtual environment. I name mine 'venv'**

```
python3 -m venv venv
```

- **Activate venv on Windows:** `venv\Scripts\activate`  
- **Activate venv on Linux:**   `Source venv/bin/activate`  
> **ALWAYS ACTIVATE YOUR VIRTUAL ENVIRONMENT BEFORE EVERY SESSION!!**  

  
**Now install all the dependencies from requirements.txt**

```
pip install -r requirements.txt
```

**Create a file named '.env' and copy the contents of `.env.example`**  

**Create/Run database migrations to create the database**

```
python manage.py makemigrations
python manage.py migrate
```
  -  Run these commands whenever a database change is made (models.py)
  - This creates a db.sqlite3 file. That's the database yo.

**Load in the sample data** (found in `planetplum/fixtures/sampledata.json`)
```
python manage.py loaddata sampledata
```
- This creates a superuser with the username **'admin'** and password **'admin'**

**Rename the `media.sample` folder to `media` to show the sample data images**  
- Any images you upload to your development server will be stored here as well.

**Start the development server**
```
python manage.py runserver
```

## Notes
Added a package? Add/Update the requirements.txt document with
```
pip freeze > requirements.txt
```

Reset the Database if you broke it with 
```
python manage.py reset_db
```
- *This command is from the package `django-extensions`*  

If you'd like to add more sample data. Then you can export your database to JSON using
```
python manage.py dumpdata --indent 4 > planetplum/fixtures/sampledata.json
```  
The indent part just makes it look nice

### Email
**Use a Google App Password if you'd like to test out email functionality.**  
 Google that, or create your own email server (idk how to do that).  


### Project Layout
- **the main project is "planetapplication"**
This is the root of the website, has the settings and all URLs go through it first.
- **the main application is "planetplum"**
This is the main application and houses all the Omaha Underground main functionality
- **the user application is "users"**
This manages the user/account aspect of things. Custom User Model and Authentication.
- **the chat application is "chat"**
The Forum

- **Each application has a models.py file**
This file defined the database schema of that application. For example, the 'planetplum' application defines that a show has an image(poster) date, venue, name, price, time, and an 'approved' boolean. 

- **planetplum/base.html is the root template in which most every other template extends from.**
Look into django templates to learn how this works.

- views.py in each application do most of the logic
Views are the functions that take data from the database, mess with it, and then chose a 'template' (html file) to serve the data with.
- **superviews under 'planetplum' does most of the CRUD logic**
any other views mostly deal with reading data or are inclusive to their application

- **urls.py maps URLs to view functions**

- **put reusable html/javascript code under 'planetplum/templates/planetplum/widgets'**

## CSS Rules
### This site uses mobile-first design principle
You'll notice in the CSS files toward the bottom we specify media queries for when the user has a larger screen. This makes it so the default computation for each webpage is for a mobile device. This speeds things up for mobile users as PC's can handle the extra computation. Design the elements for mobile first, and then specify the PC changes under the media-queries please.
### all CSS sizing needs to be related to rem or %.
**nothing can be defined using px or vw/vh unless it is the :root**
This is to make sure that the site is responsive and looks about the same for every size of screen. Plus I think it's easier to manage. The rem value on the root changes with respect to the screen width until the user's screen is too large at which it is fixed.
### This site uses a 2 color design
**they are var(--textcolor) and var(--primary)**
The textcolor is based on the user's darkmode preference (white for darkmode, black default) and the primary is the color that the user choses the site to be. The default light blue color for users was chosen to make text readable for both light and dark modes at first.

## Contributing
**Whether it's a bug fix or enhancement/features, please create an issue for it first**