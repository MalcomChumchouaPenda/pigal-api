
from core.utils import get_path
from .schemas import Course
from .queries import import_courses, import_domains
from .routes import api


def init_data():
    if not Course.query.first():
        with open(get_path(api.store_folder + '/default_domains.csv')) as f:
            import_domains(f)
        with open(get_path(api.store_folder + '/default_courses.csv')) as f:
            import_courses(f)

        