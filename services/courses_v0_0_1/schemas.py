
from core.config import ma
from .models import Course, Domain


class DomainSchema(ma.Schema):
    class Meta:
        model = Domain

    id = ma.Str()
    name = ma.Str()


class CourseSchema(ma.Schema):
    class Meta:
        model = Course

    id = ma.Str()
    name = ma.Str()
    level = ma.Int()
    domain = ma.Function(lambda obj:obj.domain.name)


