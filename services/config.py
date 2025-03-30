
# from .auth.routes import auth_api
# from .courses.routes import courses_api

# from .auth.queries import init_users
# from .courses.queries import init_courses


def register_services(app):
    # Enregistre les Blueprints des services API dans l'application."""    
    app.register_blueprint(auth_api, url_prefix='/auth')
    app.register_blueprint(courses_api, url_prefix='/api/courses')

def init_data(app):
    # Initialise les bases de données des microservices
    with app.app_context():
        init_users()
        init_courses()
