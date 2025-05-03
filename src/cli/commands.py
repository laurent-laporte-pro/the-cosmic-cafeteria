import click
from flask.cli import with_appcontext
from app import db

@click.command("create-db")
@with_appcontext
def create_db():
    db.create_all()
    click.echo("Database created.")

def register_cli(app):
    app.cli.add_command(create_db)
