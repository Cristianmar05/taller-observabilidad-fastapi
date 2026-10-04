"""
benchmark.py — Script de benchmarking para el Sistema Académico.

Ejecuta 20 peticiones a cada uno de los 3 endpoints principales y genera
una tabla resumen con: endpoint, método, total de pruebas, tiempos mín/máx/prom
y códigos HTTP obtenidos.

Uso:
    1. Levantar la app:  python -m uvicorn main:app --reload
    2. En otra terminal:  python benchmark.py
"""

import time
import statistics

import httpx

BASE_URL = "http://127.0.0.1:8000"
NUM_PETICIONES = 20


# ── Definición de escenarios ────────────────────────────────────────────────

ESCENARIOS = [
    {
        "nombre": "Listar estudiantes",
        "metodo": "GET",
        "endpoint": "/estudiantes/",
    },
    {
        "nombre": "Consultar estudiante por ID",
        "metodo": "GET",
        "endpoint": "/estudiantes/1",
    },
    {
        "nombre": "Crear estudiante (llama API externa)",
        "metodo": "POST",
        "endpoint": "/estudiantes/",
        "json": {
            "nombre": "Benchmark Test",
            "programa": "Ingeniería de Sistemas",
            "semestre": 5,
            "promedio": 4.0,
        },
    },
]


# ── Funciones auxiliares ────────────────────────────────────────────────────

def ejecutar_peticiones(client: httpx.Client, escenario: dict) -> dict:
    """Ejecuta NUM_PETICIONES al endpoint indicado y recopila métricas."""
    tiempos = []
    codigos = []

    for _ in range(NUM_PETICIONES):
        inicio = time.perf_counter()

        if escenario["metodo"] == "GET":
            resp = client.get(escenario["endpoint"])
        else:
            resp = client.post(
                escenario["endpoint"],
                json=escenario.get("json", {}),
            )

        duracion = time.perf_counter() - inicio
        tiempos.append(duracion)
        codigos.append(resp.status_code)

    codigos_unicos = sorted(set(codigos))

    return {
        "nombre": escenario["nombre"],
        "metodo": escenario["metodo"],
        "endpoint": escenario["endpoint"],
        "total": NUM_PETICIONES,
        "t_min": min(tiempos),
        "t_max": max(tiempos),
        "t_prom": statistics.mean(tiempos),
        "codigos": codigos_unicos,
    }


def imprimir_tabla(resultados: list[dict]) -> None:
    """Imprime los resultados en formato de tabla legible."""

    # Anchos de columna
    ancho = {
        "endpoint": 50,
        "metodo": 8,
        "total": 8,
        "t_min": 12,
        "t_max": 12,
        "t_prom": 12,
        "codigos": 18,
    }

    separador = "+" + "+".join("-" * (v + 2) for v in ancho.values()) + "+"
    encabezado = (
        f"| {'Endpoint':<{ancho['endpoint']}} "
        f"| {'Método':<{ancho['metodo']}} "
        f"| {'Total':<{ancho['total']}} "
        f"| {'T. Mínimo':<{ancho['t_min']}} "
        f"| {'T. Máximo':<{ancho['t_max']}} "
        f"| {'T. Promedio':<{ancho['t_prom']}} "
        f"| {'Códigos HTTP':<{ancho['codigos']}} |"
    )

    print()
    print("=" * 80)
    print("  RESULTADOS DEL BENCHMARK DE RENDIMIENTO")
    print(f"  {NUM_PETICIONES} peticiones por endpoint")
    print("=" * 80)
    print()
    print(separador)
    print(encabezado)
    print(separador)

    for r in resultados:
        codigos_str = ", ".join(str(c) for c in r["codigos"])
        fila = (
            f"| {r['metodo'] + ' ' + r['endpoint']:<{ancho['endpoint']}} "
            f"| {r['metodo']:<{ancho['metodo']}} "
            f"| {r['total']:<{ancho['total']}} "
            f"| {r['t_min']:<{ancho['t_min']}.4f} "
            f"| {r['t_max']:<{ancho['t_max']}.4f} "
            f"| {r['t_prom']:<{ancho['t_prom']}.4f} "
            f"| {codigos_str:<{ancho['codigos']}} |"
        )
        print(fila)

    print(separador)
    print()

    # Identificar el endpoint más lento
    mas_lento = max(resultados, key=lambda r: r["t_prom"])
    print(
        f"⚠  Endpoint más lento: {mas_lento['metodo']} {mas_lento['endpoint']} "
        f"(promedio: {mas_lento['t_prom']:.4f}s)"
    )
    print()


# ── Ejecución principal ────────────────────────────────────────────────────

def main():
    print(f"\nConectando a {BASE_URL} ...")

    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        # Verificar que la API está disponible
        try:
            health = client.get("/")
            health.raise_for_status()
            print("Conexión exitosa. Iniciando benchmark...\n")
        except httpx.ConnectError:
            print(
                "ERROR: No se pudo conectar a la API. "
                "Asegúrate de que esté corriendo con:\n"
                "  python -m uvicorn main:app --reload\n"
            )
            return

        resultados = []
        for i, escenario in enumerate(ESCENARIOS, 1):
            print(
                f"  [{i}/{len(ESCENARIOS)}] "
                f"{escenario['metodo']} {escenario['endpoint']} "
                f"— {NUM_PETICIONES} peticiones ..."
            )
            resultado = ejecutar_peticiones(client, escenario)
            resultados.append(resultado)

        imprimir_tabla(resultados)


if __name__ == "__main__":
    main()
