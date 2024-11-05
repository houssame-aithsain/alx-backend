#!/usr/bin/env python3
"""
Basic Flask app with a single route and template
"""
from flask import Flask, request, render_template
from flask_babel import Babel, _


class Config(object):
    """
    Config class for the application
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determines the best match for the supported languages
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Route to render the template
    """
    return render_template('3-index.html', home_title=_('home_title'),
                           home_header=_('home_header'))


if __name__ == '__main__':
    app.run()
