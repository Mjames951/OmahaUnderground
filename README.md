# Omaha Underground
A rebuild of planetplum.net with a chat, bandpages, user profiles and functionality, etc.

## Development
### Setup Python environment and dependencies
```
pip install virtualenv
virtualenv -p python3.11 .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Alternatively, use [`uv`](https://docs.astral.sh/uv/pip/environments/)
```
uv venv --python 3.11
uv pip install -r requirements.txt
```
This defaults to .venv which is automatically used by later `uv` commands

VSCode handles this via `Python: Create Environment` command

You can add packages with [`uv`](https://docs.astral.sh/uv/pip/packages/)
> uv pip install $dependency

Or update `requirements.txt` manually

### Set environment variables

Copy `.env.example` to `.env` and export env vars to your shell

```
cp .env.example .env
source .env
```
`DATABASE_URL` is an empty string for local development with SQLite

In prod, set `DATABASE_URL`to your Postgres connection string

### Run SQLite migrations

> python manage.py makemigrations && python manage.py migrate

### Create admin user

> python manage.py createsuperuser


## Running local server
### Start Django server
> python manage.py runserver

### Login to admin account
[Login locally](http://localhost:8000/accounts/login/)

### Database Migrations
Any changes to `<app>/model.py` requires a migration
> python manage.py makemigrations
> python manage.py migrate

Reset DB entirely if in a broken state
> python manage.py reset_db

## Project Layout
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

## CSS Rules
## This site uses mobile-first design principle
You'll notice in the CSS files toward the bottom we specify media queries for when the user has a larger screen. This makes it so the default computation for each webpage is for a mobile device. This speeds things up for mobile users as PC's can handle the extra computation. Design the elements for mobile first, and then specify the PC changes under the media-queries please.
## all CSS sizing needs to be related to rem or %.
### nothing can be defined using px or vw/vh unless it is the :root
This is to make sure that the site is responsive and looks about the same for every size of screen. Plus I think it's easier to manage. The rem value on the root changes with respect to the screen width until the user's screen is too large at which it is fixed.
## This site uses a 2 color design
### they are var(--textcolor) and var(--primary)
The textcolor is based on the user's darkmode preference (white for darkmode, black default) and the primary is the color that the user choses the site to be. The default light blue color for users was chosen to make text readable for both light and dark modes at first.