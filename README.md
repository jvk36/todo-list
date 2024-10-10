
# BEFORE RUNNING THE FILES EXECUTE THE FOLLOWING IN THE TERMINAL FROM THE WORKING FOLDER:
pip install -r requirements.txt

## TO DO List WEB APPLICATION - INTRO:

The implementation of the To-Do List application with authentication uses Python, SQLAlchemy, Flask for the backend, and HTML/CSS/Bootstrap/JavaScript for the frontend.

## DIRECTORY STRUCTURE:

/project_root/
├── app.py               # Contains create_app() and extensions
├── forms.py             # Contains your form definitions
├── models.py            # Contains your SQLAlchemy models
├── routes.py            # Contains your routes (Blueprint)
├── run.py               # Entry point to run the app
├── static
│   └── styles.css
├── templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── tasks.html
└── __init__.py          # Optional if using as a package

# APPLICATION - FUNCTIONAL SPEC:

1. app.py: Uses an application factory function create_app to return a Flask app object. This is done to avoid a circular dependency - app.py importing User and Task from models.py while models.py imports db from app.py. To avoid this circular dependency, the solution is to refactor how db and the models are initialized.

To fix the circular dependency, we use the application factory pattern in Flask, which defers the creation of the app and database until everything is defined:

a) Application Factory (create_app): By using the factory pattern, you initialize the app, database, and other extensions inside a function. This helps break the circular import problem.

b) Blueprint (routes.py): Separating routes into a blueprint helps organize the app and reduces the chance of circular imports. The application then registers the routes by calling "app.register_blueprint(main_routes)" in app.py. 

c) Avoiding db.create_all() at the top level: The database is created after the app context is initialized.

2. routes.py - Separate the URL routes to a separate file - separation of concerns. It uses Flasks Blueprint functionality:

3. run.py - use the create_app() function to create the app and run it. 

4. forms.py, static/styles.css and templates/*.html - Handles the Registration, Login, and Task forms.

5. models.py and instance/site.db: Uses SQLAlchemy library to build the database models using a SQLite database.

NOTES: 

1. user_loader function in app.py: This function is required to load a user from the user ID stored in the session. This function tells Flask-Login how to retrieve a User object from the database, based on the user's ID stored in the session. It needs to be in the same file where you set up login_manager (in app.py, where login_manager is initialized).

By moving the user_loader function inside create_app(), after the User model is imported, we ensure that it has access to the User class and can retrieve users from the database.

2. Flask-Login initialization: login_manager.init_app(app) in app.py initializes login_manager.

3. User model inheritance: User model (models.py) inherits from UserMixin provided by Flask-Login. This ensures that your user objects have the necessary properties and methods that Flask-Login needs to work (like is_authenticated, get_id()).

4. Blueprint routes: when routes are grouped into a Blueprint (like main_routes), it means that each route now belongs to a blueprint namespace. Flask no longer recognizes index directly but expects it to be referenced using the blueprint's name. For example, usage such as url_for('index') needs to be replaced by url_for('main_routes.index') in the templates (templates*.html) and routes (routes.py)

