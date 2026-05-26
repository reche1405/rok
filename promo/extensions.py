# promo/extensions.py
from flask_caching import Cache
from flask_mailman import Mail
from flask_admin import Admin
from flask_login import LoginManager


# Define the global, uninitialized tools
cache = Cache()
mail = Mail()

# For Flask-Admin, you can set the name and template style here, 
# but don't bind it to an app context yet.
admin = Admin(name='Rok Group Admin')

login_manager = LoginManager()
