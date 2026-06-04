import datetime, math
from flask import Blueprint, render_template, flash, request, abort, session, redirect, url_for, send_from_directory, current_app
from flask_login import current_user, login_user
from flask_mailman import EmailMessage
from promo.admin.forms import LoginForm
from promo.extensions import login_manager, cache, mail
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
from promo.forms import ContactForm

main_bp = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))


@main_bp.app_errorhandler(404)
def page_not_found(e):
    # This will catch ALL 404 errors across your entire app
    return render_template('errors/404.html'), 404

@main_bp.app_errorhandler(500)
def internal_server_error(e):
    # This will catch ALL unhandled exceptions across your entire app
    return render_template('errors/500.html'), 500


@main_bp.route('/login', methods=['GET', 'POST'])
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

@main_bp.context_processor
def get_footer():
    cached_links = cache.get('global_site_links')
    
    if cached_links is not None:
        return cached_links
    
    footer = {
        'socials' : Social.get_all(),
        'policies' : Policy.get_all(),
        'current_year' : datetime.datetime.now().year
    }
    cache.set('global_site_links', footer, timeout=86400 )
    return footer

@main_bp.route("/media/<string:rel_path>")
def serve_media(rel_path):
    media_item = Media.query.filter_by(relative_path=rel_path).first()
    if not media_item:
        return abort(404)
    path = current_app.config['UPLOAD_PATH']
    
    # 3. Stream the file securely
    try:
        return send_from_directory(path, rel_path)
    except FileNotFoundError:
        return abort(404)


@main_bp.route("/")
def hello_rok():
    form = ContactForm(request.form, meta={'csrf_context': session})
    lists = List.get_for_tags(['why-rok', 'home-hero'])
    if not lists:
        return abort(404)
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

@main_bp.route("/services")
def service_list():
    context = {
        'categories' : Category.get_all(),
        'page' : Page.get_by_tag('Services'),
        'why_this_matters' : List.get_for_tag('why-this-matters')

    }
    return render_template("pages/service-list.html", **context)

@main_bp.route("/services/<string:slug>")
def service_detail(slug):
    service = Service.get_by_slug(slug)
    if not service:
        return abort(404)
    context ={
        'service' : service,
        'service_areas' : Area.get_all()
    }
    return render_template('pages/service-detail.html', **context)

@main_bp.route("/services/<string:s_slug>/<string:l_slug>")
def service_location(s_slug, l_slug):
    service = Service.get_by_slug(s_slug)
    location = Location.get_by_slug(l_slug)
    if not service or not location:
        return abort(404)
    form = ContactForm(request.form, meta={'csrf_context': session})
    
    context = {
        'service' : service,
        'form' : form,
        'location' : location
    }
    return render_template('pages/service-location.html', **context)

@main_bp.route("/projects")
def project_list():
    page_no = request.args.get('page')
    page_no = 1 if page_no is  None else int(page_no)
    per_page = 9
    project_count = max(1, Project.count())
    print(f"Project Count: {project_count}")
    _page_count = project_count / per_page
    if _page_count < 1:
        _page_count = 1
    elif _page_count % 1 != 0:
        _page_count = math.floor(_page_count + 1)
    else: 
        _page_count = int(_page_count) 
    page_count = _page_count
    print(f"Page Count: {page_count}")
    has_prev = True if page_no > 1 else False
    prev_page_no = page_no - 1 if page_no > 1 else None

    has_next = True if page_no + 1 <= page_count else False
    next_page_no = page_no + 1 if page_no + 1 <= page_count else None
    print(f"Page Number: {page_no}\nHas Next: {has_next}\n Next Page: {next_page_no}")
    context = {
        'projects' : Project.get_page(page_no, per_page),
        'page_no' : page_no,
        'page_count' : page_count,
        'has_prev' : has_prev,
        'prev_page_no' : prev_page_no,
        'has_next' : has_next,
        'next_page_no' : next_page_no,
        'page' : Page.get_by_tag('Projects')

    }
    return render_template("pages/project-list.html", **context)

@main_bp.route("/projects/<path:slug>")
def project_detail(slug):
    project = Project.get_by_slug(slug)

    if not project:
        return abort(404)
    context = {

    'project' : project
    }
    return render_template("pages/project-detail.html", **context)

@main_bp.route("/projects/<string:p_slug>/<string:u_slug>")
def unit_detail(p_slug, u_slug):
    project = Project.get_by_slug(p_slug)
    unit = Unit.get_by_slug(u_slug)
    if project is None or unit is None:
        return abort(404)
    if unit not in project.units:
        return redirect(url_for('project_list'))
    context = {
        'unit' : unit
    }
    return render_template("pages/unit-detail.html", **context)

@main_bp.route("/areas")
def area_list():
    context = {
        'areas' : Area.get_all(),
        'page' : Page.get_by_tag('Areas')

    }
    return render_template("pages/area-list.html", **context)

@main_bp.route("/locations/<string:slug>")
def location_detail(slug):
    location = Location.get_by_slug(slug)
    if not location:
        return abort(404)

    context = {
        'location' : location,
        'services' : Service.get_all(),
    }
    return render_template("pages/location-detail.html", **context)

@main_bp.route("/blog")
def article_list():
    page_no = request.args.get('page')
    page_no = 1 if page_no is  None else int(page_no)
    per_page = 6


    article_count = max(1,Article.count())

    _page_count = article_count / per_page
    if _page_count < 1:
        _page_count = 1
    elif _page_count % 1 != 0:
        _page_count = math.floor(_page_count + 1)
    else: 
        _page_count = int(_page_count) 
    page_count = _page_count
    print(f"Page Count: {page_count}")
    has_prev = True if page_no > 1 else False
    prev_page_no = page_no - 1 if page_no > 1 else None

    has_next = True if page_no + 1 <= page_count else False
    next_page_no = page_no + 1 if page_no + 1 <= page_count else None
    print(f"Page Number: {page_no}\nHas Next: {has_next}\n Next Page: {next_page_no}")
    context = {
        'articles' : Article.get_page(page=page_no, items_per_page=per_page),
        'page_no' : page_no,
        'page_count' : page_count,
        'has_prev' : has_prev,
        'prev_page_no' : prev_page_no,
        'has_next' : has_next,
        'next_page_no' : next_page_no,
        'page' : Page.get_by_tag('Blog')
        

    }
    return render_template("pages/blog/article-list.html", **context)

@main_bp.route("/blog/<string:slug>")
def article_detail(slug):
    article = Article.get_by_slug(slug)
    if article is None:
        return abort(404)
    context = {
        'article':  article
    }
    return render_template(f"pages/blog/{article.blog_form}.html", **context)

@main_bp.route("/contact", methods=['GET', 'POST'])
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
                to=[current_app.config['INBOUND_MAIL']]
            )
            try:
                
                msg.send()
                flash("Message sent successfully, we will respond within 2 business days..", "success")
            except Exception as e:
                print(f"Email failed to send: {e}")
                flash(f"Email failed  to send. {e}", "error")
               
        else: 
            print("Error parsing form data!!!!")
            for error in form.errors.values():
                print(error)
            flash("There was an error parsing your message, please try again.", "error")

        return redirect(url_for('main.hello_rok'))       
    context = {

        'page' : page,
        'form' : form
    }
    return render_template("pages/contact.html", **context)

@main_bp.get('/policy/<string:slug>')
def policy(slug):
    policy = Policy.get_by_slug(slug)
    if not policy:
        return abort(404)
    context = {
        'policy' : policy
    }
    return render_template('pages/policy.html', **context)

@main_bp.post("/submit-query")
def contact_form():
    form = ContactForm(request.form, meta={'csrf_context': session})
   
   