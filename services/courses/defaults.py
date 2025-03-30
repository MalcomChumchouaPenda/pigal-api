
from core.config import db
from core.utils import get_path
from .schemas import Course, Training, Diploma
from .queries import import_courses, import_domains, import_units


def init_data():
    session = db.session
    _init_diplomas(session)
    _init_trainings(session)
    _init_courses()

def _init_diplomas(session):
    if not Diploma.query.first():
        data = [('DIPET1', 'DIPET I'), 
                ('DIPET2', 'DIPET II'), 
                ('LPRO', 'Licence Professionnelle'), 
                ('MPRO', 'Master Professionnel'), 
                ('M2R', 'Master II Recherche')]
        diplomas = [Diploma(id=i, name=n) for i, n in data]
        session.add_all(diplomas)
        session.commit()

def _init_trainings(session):
    if not Training.query.first():
        data = [('FI', 'Formation Initiale'), 
                ('CPS', 'Formation Continue'), 
                ('M2R', 'Master II Recherche')]
        trainings = [Training(id=i, name=n) for i, n in data]
        session.add_all(trainings)
        session.commit()

def _init_courses():
    if not Course.query.first():
        store_dir = '/services/courses/store'
        with open(get_path(store_dir + '/initial_units.csv')) as f:
            import_units(f)
        with open(get_path(store_dir + '/initial_domains.csv')) as f:
            import_domains(f)
        with open(get_path(store_dir + '/initial_courses.csv')) as f:
            import_courses(f)
        