import pytest
from core.config import db
from services.courses.queries import get_courses, get_domains, get_labs, get_departments
from services.courses.schemas import Course, Training, Unit, Domain, Diploma


@pytest.fixture
def courses_setup(app):
    training1 = Training(id="A", name="Type A")
    training2 = Training(id="B", name="Type B")
    db.session.add_all([training1, training2])
    
    unit1 = Unit(id="X", name="Département X", type="D")
    unit2 = Unit(id="Y", name="Laboratoire Y", type="L")
    db.session.add_all([unit1, unit2])
    
    domain1 = Domain(id="Xn", name="Domain Xn", unit=unit1, training=training1)
    domain2 = Domain(id="Ym", name="Domain Ym", unit=unit2, training=training2)
    db.session.add_all([domain1, domain2])
    
    diploma1 = Diploma(id="LIC", name="Licence")
    diploma2 = Diploma(id="M2R", name="Master")
    db.session.add_all([diploma1, diploma2])
    
    course1 = Course(id="Xn3", name="Course Xn", domain=domain1, diploma=diploma1, level=3)
    course2 = Course(id="Ym5", name="Course Ym", domain=domain2, diploma=diploma2, level=5)    
    db.session.add_all([course1, course2])
    db.session.commit()


def test_get_courses(courses_setup):
    courses = get_courses()
    assert len(courses) == 2

def test_get_courses_by_training(courses_setup):
    courses = get_courses(training_id="B")
    assert len(courses) == 1
    assert courses[0].name == "Course Ym"

def test_get_courses_by_unit(courses_setup):
    courses = get_courses(unit_id="X")
    assert len(courses) == 1
    assert courses[0].name == "Course Xn"


def test_get_domains_by_training(courses_setup):
    domains = get_domains(training_id="B")
    assert len(domains) == 1
    assert domains[0].name == "Domain Ym"

def test_get_domains_by_unit(courses_setup):
    domains = get_domains(unit_id="X")
    assert len(domains) == 1
    assert domains[0].name == "Domain Xn"


def test_get_labs(courses_setup):
    labs = get_labs()
    assert len(labs) == 1
    assert labs[0].name == "Laboratoire Y"
    
def test_get_departments(courses_setup):
    departments = get_departments()
    assert len(departments) == 1
    assert departments[0].name == "Département X"

