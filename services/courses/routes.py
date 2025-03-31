import io
from flask import request, jsonify
from core.utils import create_api
from core.config import db

from .schemas import (
    Course, 
    Training, 
    Unit, 
    Domain, 
    Diploma
)

from .queries import (
    import_courses, 
    import_domains,
    import_units    
)


api = create_api('courses_api', __name__)


@api.route('/', methods=['GET'])
@api.docs('get_courses.yml')
def get_courses():
    query = Course.query.join(Domain)
    training_id = request.args.get('training')
    if training_id:
        query = query.join(Training)
        query = query.filter(Training.id == training_id)

    unit_id = request.args.get('unit')
    if unit_id:
        query = query.join(Unit)
        query = query.filter(Unit.id == unit_id)

    keywords = request.args.get('keywords')
    if keywords:
        filters = keywords.replace(' ', '%')
        filters += '%'
        query = query.filter(Course.name.like(filters))
    courses = query.all()   
    return jsonify([{"id": course.id, 
                     "name": course.name, 
                     "level": course.level, 
                     "training": course.domain.training.name,
                     "domain": course.domain.name, 
                     "diploma": course.diploma.name} 
                            for course in courses])

@api.route("/<course_id>/", methods=["GET"])
def get_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    return jsonify({"id": course.id, 
                     "name": course.name, 
                     "level": course.level, 
                     "training": course.domain.training.name,
                     "domain": course.domain.name, 
                     "diploma": course.diploma.name})

@api.route("/<course_id>/", methods=["PUT"])
def update_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return {"message": "Course not found"}, 404

    data = request.get_json()
    for key, value in data.items():
        setattr(course, key, value)

    db.session.commit()
    return {"message": "Course updated"}, 200

@api.route("/<course_id>/", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return {"message": "Course not found"}, 404

    db.session.delete(course)
    db.session.commit()
    return "", 204

@api.route("/import", methods=["POST"])
@api.docs('import_courses_from_csv.yml', methods=["POST"])
def import_courses_from_csv():
    if "file" not in request.files:
        return {"message": "No file provided"}, 400

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return {"message": "Invalid file format"}, 400
    
    with io.TextIOWrapper(file) as csv_file:
        imported_count, errors = import_courses(csv_file)
    return {"imported": imported_count, "errors":errors}, 201


@api.route('/domains/', methods=['GET'])
def get_domains():
    query = Domain.query
    training_id = request.args.get('training')
    if training_id:
        query = query.join(Training)
        query = query.filter(Training.id == training_id)

    unit_id = request.args.get('unit')
    if unit_id:
        query = query.join(Unit)
        query = query.filter(Unit.id == unit_id)
    courses = query.all()   
    return jsonify([{"id": domain.id, 
                     "name": domain.name,
                     "training": domain.training.name} 
                            for domain in courses])


@api.route("/domains/import", methods=["POST"])
def import_domains_from_csv():
    if "file" not in request.files:
        return {"message": "No file provided"}, 400

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return {"message": "Invalid file format"}, 400
    
    with io.TextIOWrapper(file) as csv_file:
        imported_count, errors = import_domains(csv_file)
    return {"imported": imported_count, "errors":errors}, 201


@api.route('/departments/', methods=['GET'])
def get_departments():
    units = Unit.query.filter_by(type='D').all()  
    return jsonify([{"id": unit.id, 
                     "name": unit.name} 
                            for unit in units])

@api.route('/labs/', methods=['GET'])
def get_labs():
    units = Unit.query.filter_by(type='L').all()    
    return jsonify([{"id": unit.id, 
                     "name": unit.name} 
                            for unit in units])

@api.route("/units/import", methods=["POST"])
def import_units_from_csv():
    if "file" not in request.files:
        return {"message": "No file provided"}, 400

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return {"message": "Invalid file format"}, 400
    
    with io.TextIOWrapper(file) as csv_file:
        imported_count, errors = import_units(csv_file)
    return {"imported": imported_count, "errors":errors}, 201
