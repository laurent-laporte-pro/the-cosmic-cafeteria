from flask import Blueprint, render_template
from api.models.user import User

user_pages = Blueprint("user_pages", __name__)

@user_pages.route("/web/users")
def list_users():
    users = User.query.all()
    return render_template("user.html", users=users)
