
from core.config import db


CASCADE = "all, delete-orphan"


class Domain(db.Model):
    __bind_key__ = 'courses'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
class Course(db.Model):
    __bind_key__ = 'courses'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    domain_id = db.Column(db.String(15), db.ForeignKey('domain.id'))    
    domain = db.relationship('Domain', backref=db.backref('courses', cascade=CASCADE))
    