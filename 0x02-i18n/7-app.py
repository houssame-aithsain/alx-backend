#!/usr/bin/env python3
"""
Basic Flask application supporting multiple languages and timezones.
"""

import pytz
from typing import Dict, Union
from flask import Flask, g, request, render_template
from flask_babel import Babel


class Config:
    """
    Configures available language.
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Initialize the Flask application and load configurations
app = Flask(__name__)
app.config.from_object(Config)


# Integrate Babel for i18n and timezone support
babel = Babel(app)


# Mock data simulating user preferences
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id: int) -> Union[Dict[str, Union[str, None]], None]:
    """
    Fetch user details based on the provided user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary of user details or None if the user does not exist.
    """
    return users.get(user_id)


@babel.localeselector
def get_locale() -> str:
    """
    Selects the best locale for the user based on various sources.

    Checks the following in order:
    1. 'locale' parameter in the URL
    2. User's stored locale preference (if logged in)
    3. The 'Accept-Language' header from the request
    4. Default locale from app configuration

    Returns:
        str: The chosen locale.
    """
    locale_options = [
        request.args.get('locale', '').strip(),
        g.user.get('locale') if g.user else None,
        request.accept_languages.best_match(app.config['LANGUAGES']),
        app.config['BABEL_DEFAULT_LOCALE']
    ]
    for locale in locale_options:
        if locale in app.config['LANGUAGES']:
            return locale
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone() -> str:
    """
    Determines the appropriate timezone for the user.

    Checks the following in order:
    1. 'timezone' parameter in the URL
    2. User's stored timezone preference (if logged in)
    3. Default timezone (UTC)

    Validates timezone using pytz specified.

    Returns:
        str: The chosen timezone.
    """
    timezone = request.args.get('timezone', '').strip() \
        or (g.user['timezone'] if g.user else None)
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.before_request
def before_request() -> None:
    """
    Sets the user information in Flask's `g` object for each request.
    """
    user_id = request.args.get('login_as', type=int)
    g.user = get_user(user_id) if user_id else None


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders the main page template.

    Returns:
        str: Rendered HTML content of the main page.
    """
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run()
