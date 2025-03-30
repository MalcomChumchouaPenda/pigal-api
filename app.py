
import os
import click
from flask import request, redirect, session, url_for, send_file
from core import create_app, read_markdown, is_file, SERVICES_DIR, PAGES_DIR
# from services import register_services, init_data


# APP CREATION

env_name = os.getenv('FLASK_ENV', 'dev')
app = create_app(__name__, env_name=env_name)
# register_services(app)
# init_data(app)


# APP CLASSIC ROUTES

@app.route('/change_lang')
def change_lang():
    next = request.referrer
    if not next:
        next = url_for('home.index')
    lang = request.args.get('lang', 'fr')
    session['lang'] = lang
    return redirect(next)

@app.route('/pages/<path:fname>')
def page_static_file(fname):
    pdir = os.path.join(PAGES_DIR, os.path.normpath(fname))
    return send_file(pdir)

@app.route('/services/<path:fname>')
def service_static_file(fname):
    sdir = os.path.join(SERVICES_DIR, os.path.normpath(fname))
    return send_file(sdir)


# CLI COMMANDS

@app.cli.group()
def translate():
    """Translation and localization commands."""

@translate.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')

@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d translations'):
        raise RuntimeError('compile command failed')

@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@app.cli.group()
def demo():
    """Demo management."""

@demo.command()
def clear():
    """Clear all demo databases"""


# CUSTOM FILTERS

@app.template_filter('safe_md')
def convert_to_safe(filename, default=None):
    safe = app.jinja_env.filters['safe']
    try:
        return safe(read_markdown(filename))
    except FileNotFoundError:
        if default is not None:
            return safe(default)
        raise

@app.template_filter('safe_img')
def check_image(filename, default=None):
    if is_file(filename):
        return filename
    return default


if __name__=='__main__':
    app.run(debug=True)
    