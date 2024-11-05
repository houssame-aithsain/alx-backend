#!/usr/bin/env python3
"""
A simple Flask application with internationalization (i18n) support.
"""
from flask import Flask, request, render_template
from flask_babel import Babel


class Config:
    """
    Configuration class for the Flask application.

    This class defines the supported languages and sets the default locale
    and timezone for the application.
    """
    LANGUAGES = ['en', 'fr']  # Supported languages
    BABEL_DEFAULT_LOCALE = 'en'  # Default language
    BABEL_DEFAULT_TIMEZONE = 'UTC'  # Default timezone


# Create an instance of the Flask application
app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from the Config class

# Initialize Babel for language translations
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determines the best match for the user's.

    This function checks the request's accept_languages and returns the
    best match based on the configured supported languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders the index page with an HTML template.

    The index page displays a simple welcome message.
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run()  # Run the Flask application
