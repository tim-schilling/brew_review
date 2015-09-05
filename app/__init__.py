# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
import jinja_filters

# Define the WSGI application object
app = Flask(__name__)

# Filters
app.jinja_env.filters['linebreaks'] = jinja_filters.line_breaks_filter

# Configurations
app.config.from_pyfile('../config.py')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable
from app.review.controllers import review_blueprint
app.register_blueprint(review_blueprint)
