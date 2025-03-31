
import io
import json
import pytest
from core.config import db
from services.courses.schemas import Course, Domain


@pytest.fixture
def courses1(app):
    domain1 = Domain(id="ECO", name="Economie")
    domain2 = Domain(id="INFO", name="Informatique")
    db.session.add_all([domain1, domain2])
    
    course1 = Course(id="ECO3", name="Economie 3", domain=domain1, level=3)
    course2 = Course(id="ECO4", name="Economie 4", domain=domain1, level=4)
    course3 = Course(id="INFO5", name="Informatique 5", domain=domain2, level=5)    
    db.session.add_all([course1, course2, course3])
    db.session.commit()


def test_get_courses(client, courses1):
    response = client.get("/courses-api/")
    assert response.status_code == 200
    assert len(response.json) == 3

def test_get_courses_by_domain(client, courses1):
    response = client.get("/courses-api/?domain=ECO")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_courses_by_keywords(client, courses1):
    response = client.get("/courses-api/?keywords=Econom+4")
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_course_by_id(client, courses1):
    response = client.get("/courses-api/ECO3/")
    assert response.status_code == 200
    course = response.json
    assert course['id'] == 'ECO3'

def test_get_domains(client, courses1):
    response = client.get("/courses-api/domains/")
    assert response.status_code == 200
    assert len(response.json) == 2


@pytest.fixture
def domain1(app):   
    domain = Domain(id="ECO", name="Economie")
    db.session.add(domain)
    db.session.commit()
    return domain

@pytest.fixture
def courses2(app, domain1):
    course = Course(id="ECO3", name="Economie 3", level=3, domain=domain1)
    db.session.add(course)
    db.session.commit()


def test_update_course(client, courses2):
    data = {"name": "Economie Appliquée 3"}
    response = client.put("/courses-api/ECO3/", 
                          data=json.dumps(data), 
                          content_type="application/json")
    
    assert response.status_code == 200
    assert "Course updated" in response.json["message"]
    course = Course.query.filter_by(id='ECO3').one()
    assert course.name == "Economie Appliquée 3"

def test_delete_course(client, courses2):
    response = client.delete("/courses-api/ECO3/")
    assert response.status_code == 204


def test_import_csv_to_create_courses(client, domain1):
    csv_data = "code,nom,niveau,code_filiere\n"
    csv_data += "ECO3,Economie Monetaire 3,3,ECO\n"
    csv_data += "ECO5,Economie Politique 5,5,ECO"
    data = {"file": (io.BytesIO(csv_data.encode()), "courses.csv")}
    response = client.post("/courses-api/import", data=data, 
                           content_type="multipart/form-data")
    
    assert response.status_code == 201
    assert response.json["errors"] == []
    assert response.json["imported"] == 2
    courses = Course.query.all()
    assert len(courses) == 2
    
def test_import_csv_to_update_courses(client, courses2):
    csv_data = "code,nom,niveau,code_filiere\n"
    csv_data += "ECO3,Economie Monetaire 3,3,ECO\n"
    csv_data += "ECO5,Economie Politique 5,5,ECO"
    data = {"file": (io.BytesIO(csv_data.encode()), "courses.csv")}
    response = client.post("/courses-api/import", data=data, 
                           content_type="multipart/form-data")
    
    assert response.status_code == 201
    assert response.json["errors"] == []
    assert response.json["imported"] == 2
    courses = Course.query.all()
    assert len(courses) == 2

def test_import_csv_to_create_domains(client):
    csv_data = "code_filiere,nom_filiere\n"
    csv_data += "CFA,Comptabilite et Finance\n"
    csv_data += "ECO,Economie Monetaire"
    data = {"file": (io.BytesIO(csv_data.encode()), "domains.csv")}
    response = client.post("/courses-api/domains/import", data=data, 
                           content_type="multipart/form-data")
    
    assert response.status_code == 201
    assert response.json["errors"] == []
    assert response.json["imported"] == 2
    domains = Domain.query.all()
    assert len(domains) == 2
    
def test_import_csv_to_update_domains(client, domain1):
    csv_data = "code_filiere,nom_filiere\n"
    csv_data += "CFA,Comptabilite et Finance\n"
    csv_data += "ECO,Economie Monetaire"
    data = {"file": (io.BytesIO(csv_data.encode()), "domains.csv")}
    response = client.post("/courses-api/domains/import", data=data, 
                           content_type="multipart/form-data")
    
    assert response.status_code == 201
    assert response.json["errors"] == []
    assert response.json["imported"] == 2
    domains = Domain.query.all()
    assert len(domains) == 2
