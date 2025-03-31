import io
from flask import request, jsonify
from core.utils import create_api, swag_from
from core.config import db
from .schemas import Course
from .queries import (
    get_courses, 
    get_domains,
    get_departments,
    get_labs,
    import_courses, 
    import_domains,
    import_units    
)


api = create_api('courses_api', __name__)


@api.route('/', methods=['GET'])
@api.docs('get_courses.yml')
def get_courses():
    training_id = request.args.get('training')
    unit_id = request.args.get('unit')
    courses = get_courses(training_id=training_id, unit_id=unit_id)    
    return jsonify([{"id": course.id, 
                     "name": course.name, 
                     "level": course.level, 
                     "training": course.domain.training.name,
                     "domain": course.domain.name, 
                     "diploma": course.diploma.name} 
                            for course in courses])

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
def list_domains():
    training_id = request.args.get('training')
    unit_id = request.args.get('unit')
    courses = get_domains(training_id=training_id, unit_id=unit_id)    
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
def list_departments():
    units = get_departments()    
    return jsonify([{"id": unit.id, 
                     "name": unit.name} 
                            for unit in units])

@api.route('/labs/', methods=['GET'])
def list_labs():
    units = get_labs()    
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
