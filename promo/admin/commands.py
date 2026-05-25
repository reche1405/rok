import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from promo.models import db  # Relative import to your models
from promo.models.user import User

@click.command("create-admin")  # Note: Use click.command here, not app.cli.command
@click.argument("username")
@click.password_option()
@with_appcontext
def create_admin(username, password):
    # (Your command logic goes here)
    hashed_pw = generate_password_hash(password)
    new_admin = User(username=username, password_hash=hashed_pw, is_admin=True)
    
    db.session.add(new_admin)
    db.session.commit()
    click.echo(f"Admin {username} created!")