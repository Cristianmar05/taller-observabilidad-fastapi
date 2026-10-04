# Sistema Académico — Taller de Observabilidad con FastAPI

API REST construida con **FastAPI** para la gestión de estudiantes de un sistema académico. Proyecto diseñado como ejercicio práctico de **observabilidad, pruebas y calidad de software**.

---

## Estructura del Proyecto

```
proyecto/
├── main.py                  # Aplicación FastAPI, middleware y manejador de errores
├── routes/
│   └── estudiantes.py       # Endpoints REST de estudiantes
├── services/
│   └── estudiante_service.py # Lógica de negocio y consumo de API externa
├── repositories/
│   └── estudiante_repository.py # Acceso a datos (SQLite)
├── models/
│   └── estudiante.py        # Modelo Pydantic de validación
├── tests/
│   └── test_estudiantes.py  # Pruebas automatizadas con pytest
├── logs/
│   └── app.log              # Registro de observabilidad (se crea automáticamente)
├── benchmark.py             # Script de benchmarking de rendimiento
├── requirements.txt         # Dependencias con versiones fijas
└── README.md                # Este archivo
```

---

## Requisitos Previos

- Python 3.10 o superior

---

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd taller_observabilidad_fastapi_con_errores
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python -m uvicorn main:app --reload
```

La aplicación estará disponible en: **http://127.0.0.1:8000**

### 5. Documentación interactiva (Swagger)

Abrir en el navegador: **http://127.0.0.1:8000/docs**

---

## Endpoints Disponibles

| Método | Ruta                       | Descripción                          |
|--------|----------------------------|--------------------------------------|
| GET    | `/`                        | Health check                         |
| GET    | `/estudiantes/`            | Listar todos los estudiantes         |
| GET    | `/estudiantes/{id}`        | Consultar un estudiante por ID       |
| POST   | `/estudiantes/`            | Registrar un nuevo estudiante        |

### Ejemplo de cuerpo para POST `/estudiantes/`

```json
{
  "nombre": "Ana García",
  "programa": "Ingeniería de Sistemas",
  "semestre": 5,
  "promedio": 4.2
}
```

---

## Pruebas

### Ejecutar pruebas automatizadas

```bash
python -m pytest tests/ -v
```

### Ejecutar benchmark de rendimiento

Con la aplicación corriendo en otra terminal:

```bash
python benchmark.py
```

---

## Observabilidad

Todos los registros se almacenan en `logs/app.log` con el siguiente formato:

```
2026-10-03 15:30:00 | INFO | POST /estudiantes/ | código=200 | tiempo=0.3421s | resultado=Operación exitosa
2026-10-03 15:30:01 | ERROR | GET /estudiantes/999 | código=500 | tiempo=0.0012s | resultado=Error | excepción=...
```

Cada entrada incluye: fecha/hora, método HTTP, endpoint, código de respuesta, tiempo en segundos y resultado.

---

## Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) — Framework web async
- [Uvicorn](https://www.uvicorn.org/) — Servidor ASGI
- [Pydantic](https://docs.pydantic.dev/) — Validación de datos
- [SQLite](https://www.sqlite.org/) — Base de datos embebida
- [pytest](https://docs.pytest.org/) — Framework de testing
- [httpx](https://www.python-httpx.org/) — Cliente HTTP para benchmarks
