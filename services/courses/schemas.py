
from core.config import db


CASCADE = "all, delete-orphan"


class Training(db.Model):
    __bind_key__ = 'courses'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True) 


class Unit(db.Model):
    __bind_key__ = 'courses'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(1), nullable=False, default='D')  # D = departement, L = laboratoire


class Domain(db.Model):
    __bind_key__ = 'courses'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    unit_id = db.Column(db.String(15), db.ForeignKey('unit.id'))
    training_id = db.Column(db.String(15), db.ForeignKey('training.id'))

    unit = db.relationship('Unit', backref=db.backref('domains', cascade=CASCADE))
    training = db.relationship('Training', backref=db.backref('domains', cascade=CASCADE))


class Diploma(db.Model):
    __bind_key__ = 'courses'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


class Course(db.Model):
    __bind_key__ = 'courses'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    domain_id = db.Column(db.String(15), db.ForeignKey('domain.id'))
    diploma_id = db.Column(db.String(15), db.ForeignKey('diploma.id'))
    
    domain = db.relationship('Domain', backref=db.backref('courses', cascade=CASCADE))
    diploma = db.relationship('Diploma', backref=db.backref('courses', cascade=CASCADE))
