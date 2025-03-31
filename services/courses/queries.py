
import csv
from core.config import db
from .schemas import Course, Domain


def import_courses(csv_file):
    errors = []
    imported_count = 0
    session = db.session
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        domain_id = row['code_filiere']
        domain = Domain.query.filter_by(id=domain_id).first()
        if not domain:
            error = {'type':'Domain not found', 'obj':domain_id}
            errors.append(error)
            continue

        session.merge(Course(id=row['code'], 
                             name=row['nom'], 
                             level=row['niveau'],
                             domain_id=domain_id))
        imported_count += 1
    session.commit()
    return imported_count, errors


def import_domains(csv_file):
    errors = []
    imported_count = 0
    session = db.session
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:        
        domain_id = row['code_filiere']
        domain = Domain.query.filter_by(id=domain_id).first()
        if not domain:
            domain = Domain(id=domain_id, name=row['nom_filiere'])
            session.add(domain)
        else:
            domain.name = row['nom_filiere']
        imported_count += 1
        session.commit()
    return imported_count, errors
