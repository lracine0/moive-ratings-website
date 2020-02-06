"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of user emails and ids"""

    users = User.query.all()
    for user in users:
        print(user.email)
    return render_template("user_list.html", users=users)

    # EMAIL IS NOT BEING SENT 

@app.route('/user_signed_up')
def user_signed_up():

    # fname = request.args.get("fname")
    email_html = request.args.get("email")
    password_html = request.args.get("password")
    # age = request.args.get("age")
    # zipcode = request.args.get("zipcode")

    email_check = User.query.filter_by(email=email_html).all()
    password_check = User.query.filter_by(password=password_html).all()

    if email_check and password_check:
        ## add their user id to the flask session
        client_id = User.user_id
        session['client_id'] = client_id
        return render_template("homepage.html")
        ## route to homepage

    elif email_check:
        ##flash that password isn't correct
        # print("email checked out, not password though")
        flash("password incorrect!!!!! TRY AGAIN FOOL")

    else:
        ##direct user to sign up page
    # if email == Users.query.filter
        #print("nothing matched with anything")
        flash("please enter all of the information to be signed up
                to have access to movie ratings")

        return render_template("signed_up.html", fname=fname, email=email, 
                            password=password, age=age, zipcode= zipcode)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
