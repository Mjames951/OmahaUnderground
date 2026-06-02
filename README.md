# Omaha Underground
A rebuild of planetplum.net with a chat, bandpages, user profiles and functionality, etc.

## Development

### Prerequisites
- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/getting-started/) for dependency / package management
- (optional) [Github CLI](https://cli.github.com/)

### Quick Start

1. **Clone the repository and navigate to project root**
   ```bash
   git clone git@github.com:Mjames951/OmahaUnderground.git omahaunderground.net
   # Or via github CLI
   gh repo clone Mjames951/OmahaUnderground omahaunderground.net

   cd omahaunderground.net
   ```

2. **Install dependencies** (uv will automatically create and manage a virtual environment)
   ```bash
   make install
   # Or manually: uv sync --all-extras
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   - `DEBUG` indicates app will run in development mode
   - `DATABASE_URL` defaults to SQLite in local development (leave empty)
   - In production, set `DATABASE_URL` to your PostgreSQL connection string

   Load environment vars into your shell context
   ```bash
   source .env
   ```
4. **Run database migrations**
   ```bash
   make migrate
   # Or manually: uv run python manage.py migrate
   ```

5. **Create an admin user**
   ```bash
   make createsuperuser
   # Or manually: uv run python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   make run
   # Or manually: uv run python manage.py runserver
   ```
   The site will be available at `http://localhost:8000`


7. Login to admin account [on localhost](http://localhost:8000/accounts/login/)


### Common Development Commands

```makefile
make install         # Install dependencies
make runserver       # Start Django dev server
make migrate         # Apply database migrations
make makemigrations  # Create new migrations after model changes
make shell           # Open Django shell
make test            # Run test suite
make collectstatic   # Collect static files
```

Alternatively, run commands directly with `uv`:
```bash
uv run python manage.py <command>
```

### Adding Dependencies

For production-only packages:

`uv add $package` to update `dependencies` in `pyproject.toml`

`uv sync` to update the lockfile `uv.lock`

For dev packages, add `--dev` to `uv` commands

### VSCode Python Environment

VSCode should automatically detect the uv-managed environment. If not:
1. Open the Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
2. Run "Python: Select Interpreter"
3. Choose the `.venv` environment (uv creates this by default)

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