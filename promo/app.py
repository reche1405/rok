from flask import Flask
from promo.models import db
import os
from promo.admin.commands import create_admin
from dotenv import load_dotenv

from promo.extensions import mail, admin, cache, login_manager


load_dotenv()

def create_app():
    from promo.admin.views import (
    MediaAdminView, SlugifyAdminView,
    ListAdminView, BaseSecureView,
     ProjectAdminView, UnitAdminView,
    CachedAdminView, SecuredAdminIndexView,
    ArticleAdminView)
    from promo.routes import main_bp

    app = Flask(__name__)

    app.cli.add_command(create_admin)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_SECRET_KEY')

    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') in ['True', 'true', '1', 1]
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL') in ['False', 'false', '0', 0]
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'info@therokgroup.co.uk')
    app.config['INBOUND_MAIL'] = os.environ.get('INBOUND_MAIL')
    app.config['MAIL_DEBUG'] = True
    app_env = os.environ.get('FLASK_ENV')
    if app_env is None:
        app_env = 'production'
    app.config['FLASK_ENV'] = app_env

    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 86400 # Cache for 24 hours by default

    login_manager.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    admin.init_app(app, index_view=SecuredAdminIndexView())

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))


    UPLOAD_PATH = os.path.join(BASE_DIR, 'media')

    app.config['UPLOAD_PATH'] = UPLOAD_PATH
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(PARENT_DIR, 'project.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




    db.init_app(app)

    with app.app_context():
        from promo.models.list import List, ListItem
        from promo.models.service import Service, Category
        from promo.models.project import Project, Unit
        from promo.models.media import Media
        from promo.models.area import Area
        from promo.models.location import Location
        from promo.models.meta import Meta, Page
        from promo.models.article import Article
        from promo.models.social import Social
        from promo.models.user import User
        from promo.models.policy import Policy

        db.create_all()
        admin.add_view(ListAdminView(List, db.session, category="Static"))
        admin.add_view(SlugifyAdminView(Service, db.session, category="Services"))
        admin.add_view(BaseSecureView(Category, db.session, category="Services"))
        admin.add_view(ProjectAdminView(Project, db.session, category="Projects"))
        admin.add_view(UnitAdminView(Unit, db.session, category="Projects"))
        admin.add_view(MediaAdminView(Media, db.session, category="Static"))
        admin.add_view(BaseSecureView(Area, db.session, category="Areas"))
        admin.add_view(SlugifyAdminView(Location, db.session, category="Areas"))
        admin.add_view(BaseSecureView(Meta, db.session, category="Static"))
        admin.add_view(BaseSecureView(Page, db.session, category="Static"))
        admin.add_view(ArticleAdminView(Article, db.session, category="Blog"))
        admin.add_view(CachedAdminView(Social, db.session, category="Static"))
        admin.add_view(BaseSecureView(User, db.session, category="Auth"))
        admin.add_view(CachedAdminView(Policy, db.session, category="Static"))


    app.register_blueprint(main_bp)
    return app
    



if __name__ == '__main__':
    # Setting debug=True activates the auto-reloader
    app = create_app()
    app.run(debug=app.config['FLASK_ENV'] == 'development')