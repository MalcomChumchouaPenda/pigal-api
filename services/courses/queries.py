
import csv
from core.config import db
from .schemas import Course, Training, Unit, Domain, Diploma




def import_courses(csv_file):
    errors = []
    imported_count = 0
    session = db.session
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        diploma_id = row['code_diplome']
        diploma = Diploma.query.filter_by(id=diploma_id).first()
        if not diploma:
            error = {'type':'Diploma not found', 'obj':diploma_id}
            errors.append(error)
            continue
        
        domain_id = row['code_filiere']
        domain = Domain.query.filter_by(id=domain_id).first()
        if not domain:
            error = {'type':'Domain not found', 'obj':domain_id}
            errors.append(error)
            continue

        session.merge(Course(id=row['code'], 
                             name=row['nom'], 
                             level=row['niveau'],
                             domain_id=domain_id, 
                             diploma_id=diploma_id))
        imported_count += 1
    session.commit()
    return imported_count, errors


def import_domains(csv_file):
    errors = []
    imported_count = 0
    session = db.session
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:        
        unit_id = row['code_unite']
        unit = Unit.query.filter_by(id=unit_id).first()
        if not unit:
            error = {'type':'Unit not found', 'obj':unit_id}
            errors.append(error)
            continue
        
        training_id = row['code_formation']
        training = Training.query.filter_by(id=training_id).first()
        if not training:
            error = {'type':'Training not found', 'obj':training_id}
            errors.append(error)
            continue

        domain_id = row['code_filiere']
        domain = Domain.query.filter_by(id=domain_id).first()
        if not domain:
            session.add(Domain(id=domain_id, 
                               name=row['nom_filiere'],
                               training=training, 
                               unit=unit))
        else:
            domain.name = row['nom_filiere']
            domain.unit = unit

        imported_count += 1
        session.commit()
    return imported_count, errors


def import_units(csv_file):
    errors = []
    imported_count = 0
    session = db.session
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:        
        unit_id = row['code_unite']
        unit = Unit.query.filter_by(id=unit_id).first()
        if not unit:
            type = row['type_unite']
            unit = Unit(id=unit_id, name=row['nom_unite'], type=type)
            session.add(unit)
        else:
            unit.name = row['nom_unite']
            unit.type = row['type_unite']

        imported_count += 1
        session.commit()
    return imported_count, errors

