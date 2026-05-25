from flask import Flask, request,flash, redirect, url_for, render_template, send_from_directory, abort, session
from models import db
from forms import ContactForm
import os, math, datetime, smtplib, sqlite3
from email.mime.text import MIMEText
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme
from flask_admin.contrib.sqla import ModelView
from admin.views import (
    MediaAdminView, SlugifyAdminView,
    ListAdminView, BaseSecureView,
    SecuredAdminIndexView, ProjectAdminView)
from admin.forms import LoginForm
from admin.commands import create_admin
from flask_login import LoginManager, current_user, login_user
from dotenv import load_dotenv
from flask_mailman import Mail, EmailMessage


load_dotenv()

login_manager = LoginManager()

app = Flask(__name__)
app.cli.add_command(create_admin)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
login_manager.init_app(app)


app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', '127.0.0.1')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 1025))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'False').lower() in ['true', '1']
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() in ['true', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@yourdomain.local')
app.config['INBOUND_MAIL'] = os.environ.get('INBOUND_MAIL')

mail = Mail(app)

admin = Admin(
    app, 
    name='ROK Admin',
    index_view=SecuredAdminIndexView(),
    theme=Bootstrap4Theme(swatch='darkly'))

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


UPLOAD_PATH = os.path.join(BASE_DIR, 'media')

app.config['UPLOAD_PATH'] = UPLOAD_PATH
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'project.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db.init_app(app)
with app.app_context():
    from models.list import List, ListItem
    from models.service import Service
    from models.project import Project, Unit
    from models.media import Media
    from models.area import Area
    from models.location import Location
    from models.meta import Meta, Page
    from models.article import Article
    from models.social import Social
    from models.user import User
    from models.policy import Policy

    db.create_all()
    admin.add_view(ListAdminView(List, db.session, category="Static"))
    admin.add_view(SlugifyAdminView(Service, db.session, category="Services"))
    admin.add_view(ProjectAdminView(Project, db.session))
    admin.add_view(MediaAdminView(Media, db.session, category="Services"))
    admin.add_view(BaseSecureView(Area, db.session, category="Services"))
    admin.add_view(SlugifyAdminView(Location, db.session, category="Services"))
    admin.add_view(BaseSecureView(Meta, db.session, category="Static"))
    admin.add_view(BaseSecureView(Page, db.session, category="Static"))
    admin.add_view(SlugifyAdminView(Article, db.session))
    admin.add_view(BaseSecureView(Social, db.session, category="Static"))
    admin.add_view(BaseSecureView(User, db.session))
    admin.add_view(SlugifyAdminView(Policy, db.session, category="Static"))
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 1. If they are already logged in, send them straight to the admin panel
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.index'))

    form = LoginForm(request.form, meta={'csrf_context': session})

    # 2. Handle form submission
    if form.validate():
        # Find user by username
        user : User = User.query.filter_by(username=form.username.data).first()
        
        # Verify user exists and the password hash matches
        if user and user.verify_password(form.password.data):
            # Log the user in with Flask-Login
            login_user(user)
            print(f"Login function executed. Is user authed? {current_user.is_authenticated}")
            # Handle the 'next' query parameter securely (from Flask-Admin/Flask-Login intercepts)
            next_page = request.args.get('next')
            
            # Simple security check to make sure the next page stays on your domain
            if not next_page:
                next_page = url_for('admin.index')
                
            flash('Logged in successfully!', 'success')
            return redirect(next_page)
        
        # Generic error message so malicious entities don't know if username or password was wrong
        flash('Invalid username or password.', 'danger')
        print(f"Login function not successful. Is user authed? {current_user.is_authenticated}")
        
    return render_template('admin/login.html', form=form)




@app.context_processor
def get_footer():
    socials = Social.get_all()
    policies = Policy.get_all()
    return dict(current_year=datetime.datetime.now().year, socials=socials, policies=policies)

@app.route("/media/<string:rel_path>")
def serve_media(rel_path):
    media_item = Media.query.filter_by(relative_path=rel_path).first_or_404()
    
    path = app.config['UPLOAD_PATH']
    
    # 3. Stream the file securely
    try:
        return send_from_directory(path, rel_path)
    except FileNotFoundError:
        abort(404)

@app.route("/")
def hello_rok():
    form = ContactForm(request.form, meta={'csrf_context': session})
    lists = List.get_for_tags(['why-rok', 'home-hero'])

    context = {
        'projects' : Project.get_featured(),
        'services' : Service.get_home(),
        'areas' : Area.get_home(),
        'page' : Page.get_by_tag('Home'),
        'hero_list' : lists['home-hero'],
        'why_rok' : lists['why-rok'],
        'form' : form
    }
    return render_template("pages/index.html", **context)

@app.route("/services")
def service_list():
    context = {
        'services' : Service.get_all(),
        'page' : Page.get_by_tag('Services'),
        'why_this_matters' : List.get_for_tag('why-this-matters')

    }
    return render_template("pages/service-list.html", **context)

@app.route("/services/<string:slug>")
def service_detail(slug):
    service = Service.get_by_slug(slug)
    if not service:
        return redirect(url_for('service_list'))
    context ={
        'service' : service,
        'service_areas' : Area.get_all()
    }
    return render_template('pages/service-detail.html', **context)

@app.route("/services/<string:s_slug>/<string:l_slug>")
def service_location(s_slug, l_slug):
    service = Service.get_by_slug(s_slug)
    location = Location.get_by_slug(l_slug)
    form = ContactForm(request.form, meta={'csrf_context': session})
    
    context = {
        'service' : service,
        'form' : form,
        'location' : location
    }
    return render_template('pages/service-location.html', **context)

@app.route("/projects")
def project_list():
    context = {
        'projects' : Project.get_all(),
        'page' : Page.get_by_tag('Projects')

    }
    return render_template("pages/project-list.html", **context)

@app.route("/projects/<path:slug>")
def project_detail(slug):
    project = Project.get_by_slug(slug)
    if not project:
        return redirect(url_for('project_list'))
    context = {

    'project' : project
    }
    return render_template("pages/project-detail.html", **context)

@app.route("/areas")
def area_list():
    context = {
        'areas' : Area.get_all(),
        'page' : Page.get_by_tag('Areas')

    }
    return render_template("pages/area-list.html", **context)

@app.route("/locations/<string:slug>")
def location_detail(slug):
    location = Location.get_by_slug(slug)
    if not location:
        return redirect(url_for('area_list'))

    context = {
        'location' : location,
        'services' : Service.get_all(),
    }
    return render_template("pages/location-detail.html", **context)

@app.route("/blog")
def article_list():
    page_no = request.args.get('page')
    page_no = 1 if page_no is  None else int(page_no)
    per_page = 6

    article_count = max(1,Article.count())
    page_count = max(1, math.floor(article_count / per_page))
    print(f"Page Count: {page_count}")
    has_prev = True if page_no > 1 else False
    prev_page_no = page_no - 1 if page_no > 1 else None

    has_next = True if page_no + 1 <= page_count else False
    next_page_no = page_no + 1 if page_no + 1 <= page_count else None
    print(f"Page Number: {page_no}\nHas Next: {has_next}\n Next Page: {next_page_no}")
    context = {
        'articles' : Article.get_page(page_no, per_page),
        'page_no' : page_no,
        'page_count' : page_count,
        'has_prev' : has_prev,
        'prev_page_no' : prev_page_no,
        'has_next' : has_next,
        'next_page_no' : next_page_no,
        'page' : Page.get_by_tag('Blog')
        

    }
    return render_template("pages/blog/article-list.html", **context)

@app.route("/blog/<string:slug>")
def article_detail(slug):
    article = Article.get_by_slug(slug)
    context = {
        'article':  article
    }
    return render_template(f"pages/blog/{article.blog_form}.html", **context)

@app.route("/contact", methods=['GET', 'POST'])
def contact(): 
    page = Page.get_by_tag('Contact')
    form = ContactForm(request.form, meta={'csrf_context': session})
    if request.method == "POST":
        print(form.data)
        if form.validate():
            client_email = form.email.data
            client_name = form.name.data
            client_tel = form.number.data
            message_body = form.message.data

            #TEMP: Print the form data
            print(f"New contact query from:\n{client_name}\nTel:\n{client_tel}\nResponse Email:\n{client_email}\n\nMessage\n\n{message_body}")
            msg = EmailMessage(
                subject="New Website Contact Query",
                body=f"New contact query from:\n{client_name}\nTel:\n{client_tel}\nResponse Email:\n{client_email}\n\nMessage\n\n{message_body}",
                to=[app.config['INBOUND_MAIL']]
            )
            try:
                
                msg.send()
                flash("Message sent successfully, we will respond within 2 business days..", "success")
            except Exception as e:
                print(f"Email failed to send: {e}")
                flash("Email failed  to send. Please try again.", "error")
               
        else: 
            print("Error parsing form data!!!!")
            for error in form.errors.values():
                print(error)
            flash("There was an error parsing your message, please try again.", "error")

        return redirect(url_for('hello_rok'))       
    context = {

        'page' : page,
        'form' : form
    }
    return render_template("pages/contact.html", **context)

@app.get('/policy/<string:slug>')
def policy(slug):
    context = {
        'policy' : Policy.get_by_slug(slug)
    }
    return render_template('pages/policy.html', **context)

@app.post("/submit-query")
def contact_form():
    form = ContactForm(request.form, meta={'csrf_context': session})
   
   


if __name__ == '__main__':
    # Setting debug=True activates the auto-reloader
    app.run(debug=False)