from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_listar_estudiantes():
    respuesta = client.get("/estudiantes/")
    assert respuesta.status_code == 200

def test_crear_estudiante():
    respuesta = client.post("/estudiantes/", json={
        "nombre": "Ana",
        "programa": "Ingeniería de Sistemas",
        "semestre": 5,
        "promedio": 4.2
    })
    assert respuesta.status_code == 200

def test_estudiante_inexistente():
    respuesta = client.get("/estudiantes/99999")
    assert respuesta.status_code == 404
