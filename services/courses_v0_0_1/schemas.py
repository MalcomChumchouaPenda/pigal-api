
from core.config import ma
from .models import Course, Domain


class DomainSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Domain
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()

domain_schema = DomainSchema()
domains_schema = DomainSchema(many=True)


class CourseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Course
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    level = ma.auto_field()
    domain = ma.Function(lambda obj:obj.domain.name)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
