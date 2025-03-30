
import io
import json
import pytest
from core.config import db
from services.courses.schemas import Course, Training, Unit, Domain, Diploma


@pytest.fixture
def courses1(app):
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


def test_get_courses(client, courses1):
    response = client.get("/api/courses/")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_courses_by_training(client, courses1):
    response = client.get("/api/courses/?training=A")
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_courses_by_unit(client, courses1):
    response = client.get("/api/courses/?unit=X")
    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_domains(client, courses1):
    response = client.get("/api/courses/domains/")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_domains_by_training(client, courses1):
    response = client.get("/api/courses/domains/?training=A")
    assert response.status_code == 200
    assert len(response.json) == 1
    
def test_get_domains_by_unit(client, courses1):
    response = client.get("/api/courses/domains/?unit=X")
    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_labs(client, courses1):
    response = client.get("/api/courses/labs/")
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_departments(client, courses1):
    response = client.get("/api/courses/departments/")
    assert response.status_code == 200
    assert len(response.json) == 1


@pytest.fixture
def training1(app): 
    training = Training(id='FI', name="Initiale")
    db.session.add(training)
    db.session.commit()
    return training

@pytest.fixture
def unit1(app): 
    unit = Unit(id='STEG', name="Sciences Gestion", type="D")
    db.session.add(unit)
    db.session.commit()
    return unit

@pytest.fixture
def domain1(app, training1, unit1):   
    domain = Domain(id="ECO", name="Economie", unit=unit1, training=training1)
    db.session.add(domain)
    db.session.commit()
    return domain

@pytest.fixture
def diplomas1(app):
    diploma1 = Diploma(id="L3", name="Licence")   
    diploma2 = Diploma(id="M2", name="Master")   
    db.session.add_all([diploma1, diploma2])
    db.session.commit()
    return diploma1, diploma2

@pytest.fixture
def courses2(app, diplomas1, domain1):
    course = Course(id="ECO3", name="Economie 3", level=3,
                    domain=domain1, diploma=diplomas1[0])
    db.session.add(course)
    db.session.commit()

def test_update_course(client, courses2):
    data = {"name": "Economie Appliquée 3"}
    response = client.put("/api/courses/ECO3", 
                          data=json.dumps(data), 
                          content_type="application/json")
    
    assert response.status_code == 200
    assert "Course updated" in response.json["message"]
    course = Course.query.filter_by(id='ECO3').one()
    assert course.name == "Economie Appliquée 3"

def test_delete_course(client, courses2):
    response = client.delete("/api/courses/ECO3")
    assert response.status_code == 204


def test_import_csv_to_create_courses(client, diplomas1, domain1):
    csv_data = "code,nom,niveau,code_filiere,code_diplome\n"
    csv_data += "ECO3,Economie Monetaire 3,3,ECO,L3\n"
    csv_data += "ECO5,Economie Politique 5,5,ECO,M2"
    data = {"file": (io.BytesIO(csv_data.encode()), "courses.csv")}
    response = client.post("/api/courses/import", data=data, 
                           content_type="multipart/form-data")
    
    assert response.status_code == 201
    assert response.json["errors"] == []
    assert response.json["imported"] == 2
    courses = Course.query.all()
    assert len(courses) == 2
    
def test_import_csv_to_update_courses(client, courses2):
    csv_data = "code,nom,niveau,code_filiere,code_diplome\n"
    csv_data += "ECO3,Economie Monetaire 3,3,ECO,L3\n"
    csv_data += "ECO5,Economie Politique 5,5,ECO,M2"
    data = {"file": (io.BytesIO(csv_data.encode()), "courses.csv")}
    response = client.post("/api/courses/import", data=data, 
                           content_type="multipart/form-data")
    
    assert response.status_code == 201
    assert response.json["errors"] == []
    assert response.json["imported"] == 2
    courses = Course.query.all()
    assert len(courses) == 2


def test_import_csv_to_create_domains(client, training1, unit1):
    csv_data = "code_filiere,nom_filiere,code_formation,code_unite\n"
    csv_data += "CFA,Comptabilite et Finance,FI,STEG\n"
    csv_data += "ECO,Economie Monetaire,FI,STEG"
    data = {"file": (io.BytesIO(csv_data.encode()), "domains.csv")}
    response = client.post("/api/courses/domains/import", data=data, 
                           content_type="multipart/form-data")
    
    assert response.status_code == 201
    assert response.json["errors"] == []
    assert response.json["imported"] == 2
    domains = Domain.query.all()
    assert len(domains) == 2
    
def test_import_csv_to_update_domains(client, domain1):
    csv_data = "code_filiere,nom_filiere,code_formation,code_unite\n"
    csv_data += "CFA,Comptabilite et Finance,FI,STEG\n"
    csv_data += "ECO,Economie Monetaire,FI,STEG"
    data = {"file": (io.BytesIO(csv_data.encode()), "domains.csv")}
    response = client.post("/api/courses/domains/import", data=data, 
                           content_type="multipart/form-data")
    
    assert response.status_code == 201
    assert response.json["errors"] == []
    assert response.json["imported"] == 2
    domains = Domain.query.all()
    assert len(domains) == 2


def test_import_csv_to_create_units(client):
    csv_data = "code_unite,nom_unite,type_unite\n"
    csv_data += "STEG,Sciences de Gestion,D\n"
    csv_data += "GINFO,Génie Informatique,L"
    data = {"file": (io.BytesIO(csv_data.encode()), "units.csv")}
    response = client.post("/api/courses/units/import", data=data, 
                           content_type="multipart/form-data")
    
    assert response.status_code == 201
    assert response.json["errors"] == []
    assert response.json["imported"] == 2
    units = Unit.query.all()
    assert len(units) == 2
    
def test_import_csv_to_update_units(client, unit1):
    csv_data = "code_unite,nom_unite,type_unite\n"
    csv_data += "STEG,Sciences de Gestion,D\n"
    csv_data += "GINFO,Génie Informatique,L"
    data = {"file": (io.BytesIO(csv_data.encode()), "units.csv")}
    response = client.post("/api/courses/units/import", data=data, 
                           content_type="multipart/form-data")
    
    assert response.status_code == 201
    assert response.json["errors"] == []
    assert response.json["imported"] == 2
    units = Unit.query.all()
    assert len(units) == 2

