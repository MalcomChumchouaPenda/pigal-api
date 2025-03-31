import io
import csv
from flask import request, jsonify, send_file
from core.utils import create_api
from core.config import db

from .models import Course, Domain
from .schemas import CourseSchema, DomainSchema
from .tasks import (
    import_courses, 
    import_domains, 
    export_courses
)


api = create_api('courses_api', __name__)


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

@api.route('/courses', methods=['GET'])
@api.docs('get_courses.yml')
def get_courses():
    query = Course.query
    domain_id = request.args.get('domain')
    if domain_id:
        query = query.join(Domain)
        query = query.filter(Domain.id == domain_id)

    keywords = request.args.get('keywords')
    if keywords:
        filters = keywords.replace(' ', '%')
        filters += '%'
        query = query.filter(Course.name.like(filters))
    courses = query.all()
    return courses_schema.dump(courses)   

@api.route("/courses/<course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    return course_schema.dump(course)

@api.route("/courses/<course_id>", methods=["PUT"])
def update_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return {"message": "Course not found"}, 404

    data = request.get_json()
    for key, value in data.items():
        setattr(course, key, value)

    db.session.commit()
    return {"message": "Course updated"}, 200

@api.route("/courses/<course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return {"message": "Course not found"}, 404

    db.session.delete(course)
    db.session.commit()
    return "", 204

@api.route("/courses/csv", methods=["POST"])
@api.docs('import_courses.yml', methods=["POST"])
def import_courses_from_csv():
    if "file" not in request.files:
        return {"message": "No file provided"}, 400

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return {"message": "Invalid file format"}, 400
    
    with io.TextIOWrapper(file) as csv_file:
        imported_count, errors = import_courses(csv_file)
    return {"imported": imported_count, "errors":errors}, 201

@api.route("/courses/csv", methods=["GET"])
@api.roles_accepted('admin', 'teacher')
def export_courses_from_csv():
    csv_data = export_courses()
    return send_file(
        io.BytesIO(csv_data.encode()),
        as_attachment=True,
        download_name="courses.csv",
        mimetype="text/csv"
    )


domain_schema = DomainSchema()
domains_schema = DomainSchema(many=True)

@api.route('/domains', methods=['GET'])
@api.docs('get_domains.yml', methods=["GET"])
def get_domains():
    domains = Domain.query.all() 
    return domains_schema.dump(domains)


@api.route("/domains/csv", methods=["POST"])
def import_domains_from_csv():
    if "file" not in request.files:
        return {"message": "No file provided"}, 400

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return {"message": "Invalid file format"}, 400
    
    with io.TextIOWrapper(file) as csv_file:
        imported_count, errors = import_domains(csv_file)
    return {"imported": imported_count, "errors":errors}, 201
