import logging
import os
import time
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from repositories.estudiante_repository import inicializar
from routes.estudiantes import router

# ---------------------------------------------------------------------------
# Configuración de logging
# ---------------------------------------------------------------------------
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("observabilidad")


# ---------------------------------------------------------------------------
# Lifespan: inicialización y cierre de la aplicación
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.info("Iniciando aplicación — creando tablas en base de datos...")
    inicializar()
    logger.info("Base de datos inicializada correctamente.")
    yield
    # --- Shutdown ---
    logger.info("Aplicación detenida.")


# ---------------------------------------------------------------------------
# Aplicación FastAPI
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Sistema Académico - Taller de Observabilidad",
    lifespan=lifespan,
)
app.include_router(router)


# ---------------------------------------------------------------------------
# Middleware de observabilidad
# ---------------------------------------------------------------------------
@app.middleware("http")
async def middleware_observabilidad(request: Request, call_next):
    inicio = time.time()
    metodo = request.method
    endpoint = request.url.path

    try:
        response = await call_next(request)
        duracion = round(time.time() - inicio, 4)
        codigo = response.status_code

        resultado = "Operación exitosa" if codigo < 400 else "Error"

        logger.info(
            "%s %s | código=%d | tiempo=%.4fs | resultado=%s",
            metodo, endpoint, codigo, duracion, resultado,
        )
        return response

    except Exception as exc:
        duracion = round(time.time() - inicio, 4)

        logger.error(
            "%s %s | código=500 | tiempo=%.4fs | resultado=Error | "
            "excepción=%s | traza=%s",
            metodo, endpoint, duracion,
            str(exc), traceback.format_exc(),
        )
        raise


# ---------------------------------------------------------------------------
# Manejador global de errores no controlados
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def manejador_global_errores(request: Request, exc: Exception):
    logger.error(
        "ERROR NO CONTROLADO | %s %s | error=%s | tipo=%s | traza=%s",
        request.method,
        request.url.path,
        str(exc),
        type(exc).__name__,
        traceback.format_exc(),
    )
    return JSONResponse(
        status_code=500,
        content={
            "detalle": "Error interno del servidor",
            "error": str(exc),
            "tipo": type(exc).__name__,
        },
    )


# ---------------------------------------------------------------------------
# Endpoint raíz (health check)
# ---------------------------------------------------------------------------
@app.get("/")
def inicio():
    return {"mensaje": "Sistema académico activo"}
