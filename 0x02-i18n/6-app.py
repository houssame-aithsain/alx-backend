#!/usr/bin/env python3
"""
A Flask app with user locale selection priority.
"""
from flask import Flask, request, render_template, g
from flask_babel import Babel

# Mock user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app = Flask(__name__)
app.config['LANGUAGES'] = ['en', 'fr']
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
babel = Babel(app)


def get_user():
    """Retrieve user from mock data based on login_as parameter."""
    user_id = request.args.get("login_as", type=int)
    return users.get(user_id)


@app.before_request
def before_request():
    """Store user information in global context."""
    g.user = get_user()


@babel.select_locale
def get_locale():
    """Determine the best locale based on URL parameterand default."""
    # 1. Locale from URL parameter
    locale = request.args.get("locale")
    if locale in app.config['LANGUAGES']:
        return locale

    # 2. Locale from user settings
    user = getattr(g, 'user', None)
    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']

    # 3. Locale from request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index():
    """Render the main page."""
    return render_template('6-index.html')


if __name__ == "__main__":
    app.run()
