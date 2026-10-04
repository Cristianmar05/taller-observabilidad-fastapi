# GUÍA DEL TALLER

## Objetivo

Analizar la aplicación, implementar observabilidad, realizar pruebas controladas, identificar mínimo cinco puntos débiles y proponer mejoras técnicas.

## 1. Reconocimiento

Identifique endpoints, métodos HTTP, modelos, rutas, servicios, repositorios, base de datos y servicio externo.

Construya:
Cliente → FastAPI → Service → Repository / API externa → Respuesta

## 2. Ejecución

Instale dependencias:

python -m pip install -r requirements.txt

Ejecute:

python -m uvicorn main:app --reload

Abra /docs.

## 3. Observabilidad

Incorpore registros con:
- fecha y hora;
- método HTTP;
- endpoint;
- código de respuesta;
- tiempo de respuesta;
- resultado;
- información del error.

## 4. Pruebas

Pruebe:
- datos válidos;
- datos inválidos;
- campos faltantes;
- valores fuera de rango;
- identificadores existentes;
- identificadores inexistentes;
- comportamiento del servicio externo;
- diferentes cantidades de solicitudes.

## 5. Rendimiento

Seleccione mínimo tres endpoints o escenarios y mida:
- número de pruebas;
- tiempo mínimo;
- tiempo máximo;
- tiempo promedio;
- código HTTP.

No invente los datos: deben salir de las pruebas.

## 6. Hallazgos

Identifique mínimo cinco puntos débiles. Para cada uno registre:

1. Problema.
2. Componente afectado.
3. Evidencia.
4. Causa probable.
5. Impacto.
6. Prioridad: Crítico, Alto, Medio o Bajo.
7. Solución propuesta.

## 7. Mejoras

Seleccione los tres hallazgos más importantes y explique:

Problema → Causa → Impacto → Solución técnica → Resultado esperado

## 8. Pruebas finales

Amplíe los tests para cubrir operaciones exitosas, validaciones, recursos inexistentes, errores y servicios externos.

## 9. Preguntas

1. ¿Por qué la observabilidad es importante aunque una aplicación aparentemente funcione?
2. ¿Qué diferencia existe entre detectar un error y encontrar su causa?
3. ¿Por qué "Error" es insuficiente como registro?
4. ¿Qué información debe tener un log útil?
5. ¿Qué puede ocurrir si una API externa no tiene timeout?
6. ¿Cómo ayudan los códigos HTTP al diagnóstico?
7. ¿Cómo ayuda el tiempo de respuesta a encontrar puntos débiles?
8. ¿Qué relación existe entre observabilidad y calidad?
9. ¿Por qué una prueba manual puede comportarse diferente ante muchas solicitudes?
10. ¿Cuál hallazgo encontrado tiene mayor impacto y qué evidencia lo demuestra?

## 10. Entrega

proyecto/
├── main.py
├── routes/
├── services/
├── repositories/
├── models/
├── tests/
├── logs/
├── requirements.txt
└── README.md

El informe debe utilizar APA 7.ª edición y contener evidencias relacionadas con cada prueba.

No incluir contraseñas, tokens, API Keys, credenciales ni secretos.

## Regla del taller

No basta con decir "hay un error".

Deben demostrar:

OBSERVAR → PROBAR → MEDIR → ENCONTRAR → DEMOSTRAR → EXPLICAR → MEJORAR
