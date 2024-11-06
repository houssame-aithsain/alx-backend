#!/usr/bin/env python3
"""
A basic Flask application demonstrating.
"""
import pytz
import datetime
from typing import Dict, Union
from flask import Flask, g, request, render_template
from flask_babel import Babel, format_datetime


class Config:
    """
    Configuration class for the Flask app.
    """
    LANGUAGES = ['en', 'fr']  # Supported languages
    BABEL_DEFAULT_LOCALE = 'en'  # Default locale
    BABEL_DEFAULT_TIMEZONE = 'UTC'  # Default timezone


# Initialize the Flask application and configure it
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Babel for localization and timezone management
babel = Babel(app)

# Simulated user data with names, locales, and timezones
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id: int) -> Union[Dict[str, Union[str, None]], None]:
    """
    Retrieve user information based on the user ID.
    Args:
        user_id (int): The user's ID.
    Returns:
        dict: User data if found, otherwise None.
    """
    return users.get(user_id, None)


@babel.localeselector
def get_locale() -> str:
    """
    Select the appropriate locale based on the request.
    """
    locale_options = [
        request.args.get('locale', '').strip(),  # Locale from URL parameters
        g.user.get('locale') if g.user else None,  # Locale from user settings
        request.accept_languages.best_match(app.config['LANGUAGES']),
        Config.BABEL_DEFAULT_LOCALE  # Fallback to default locale
    ]

    for locale in locale_options:
        if locale and locale in Config.LANGUAGES:
            return locale
    return Config.BABEL_DEFAULT_LOCALE  # Default to the configured fallback


@babel.timezoneselector
def get_timezone() -> str:
    """
    Select the appropriate timezone based on the request.
    """
    timezone = request.args.get('timezone', '').strip()

    if not timezone and g.user:
        timezone = g.user['timezone']  # Timezone from user settings

    try:
        timezone = pytz.timezone(timezone).zone  # Validate the timezone
    except pytz.exceptions.UnknownTimeZoneError:
        timezone = app.config['BABEL_DEFAULT_TIMEZONE']

    return timezone


@app.before_request
def before_request() -> None:
    """
    Add the user and formatted time to the global.
    """
    user_id = request.args.get('login_as', 0)  # Retrieve the 'login_as'
    g.user = get_user(user_id)  # Set the user in the global object
    # Store the current time, formatted according to the user's locale
    g.time = format_datetime(datetime.datetime.now())


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Render the homepage with the current time and any necessary localization.
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
