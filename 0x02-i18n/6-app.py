#!/usr/bin/env python3
"""
Basic Flask application with multilingual support using Flask-Babel.
"""

from typing import Dict, Union
from flask import Flask, g, request, render_template
from flask_babel import Babel


class Config:
    """
    Configurations for the Flask application, including language settings.
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Initialize Flask application and load configurations
app = Flask(__name__)
app.config.from_object(Config)


# Initialize Babel for localization support
babel = Babel(app)


# Mock user data simulating a database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id: int) -> Union[Dict[str, Union[str, None]], None]:
    """
    Retrieve user data based on ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: User data if found; None otherwise.
    """
    return users.get(user_id)


@babel.localeselector
def get_locale() -> str:
    """
    Determines the best match for locale based on the request.

    Checks the locale in the following order:
    1. URL parameter `locale`
    2. User's preferred locale if logged in
    3. Locale from `Accept-Language` headers
    4. Default locale

    Returns:
        str: The selected locale.
    """
    options = [
        request.args.get('locale', '').strip(),
        g.user.get('locale') if g.user else None,
        request.accept_languages.best_match(app.config['LANGUAGES']),
        app.config['BABEL_DEFAULT_LOCALE']
    ]
    for locale in options:
        if locale in app.config['LANGUAGES']:
            return locale
    return app.config['BABEL_DEFAULT_LOCALE']


@app.before_request
def before_request() -> None:
    """
    Set user information in the global `g` object before each request.
    """
    user_id = request.args.get('login_as', type=int)
    g.user = get_user(user_id) if user_id else None


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Render the main page template.

    Returns:
        str: Rendered HTML template for the homepage.
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run()
