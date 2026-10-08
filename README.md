# 🐾 HuellaSegura

Proyecto universitario para registrar y gestionar reportes de maltrato, abandono o peligro animal. **Corte I:** CRUD de reportes conectado a SQLite. La integración con WhatsApp y la notificación a fundaciones son objetivos futuros, **no están implementados**.

## Tecnologías
Python 3, Flask, SQLite, HTML, CSS y Jinja2.

## Cómo ejecutarlo
1. Instala Python 3.10 o superior.
2. Abre una terminal dentro de esta carpeta.
3. (Opcional) Crea un entorno virtual: `python -m venv .venv` y actívalo.
4. Instala dependencias: `python -m pip install -r requirements.txt`.
5. Ejecuta: `python app.py`.
6. Abre `http://127.0.0.1:5000`.

En Windows también puedes utilizar `py -m pip install -r requirements.txt` y `py app.py`.

La base de datos `huellasegura.db` se crea automáticamente en el primer arranque y no se sube a GitHub.

## Funcionalidades
- Crear reporte con validación de tipo, ubicación y descripción.
- Listar reportes y consultar detalles.
- Editar reporte y cambiar estado.
- Eliminar reporte mediante POST con confirmación.

## Modelo de datos
Cuatro tablas: `ciudadanos`, `reportes`, `fundaciones` y `asignaciones`. En este corte, el CRUD se aplica únicamente a `reportes`. Las otras tablas preparan el modelo para futuras fases.

## Pruebas manuales para el equipo
1. Registrar un caso y comprobar que aparece en el listado.
2. Editar la ubicación y comprobar el cambio.
3. Reiniciar Flask y comprobar que el caso permanece.
4. Intentar guardar una descripción de menos de 10 caracteres.
5. Eliminar el caso, confirmar que desaparece y comprobar que una petición GET a `/reportes/1/eliminar` no elimina registros.

## Seguridad y alcance
Es un prototipo académico local, sin inicio de sesión ni integración real con entidades de protección. No debe desplegarse públicamente con `debug=True` o la clave de desarrollo. Para un despliegue real se requieren autenticación, CSRF, protección de datos personales y configuración segura.

## Integrantes
Sandra Johana Cartagena Agudelo 
Kelly Johana Ramírez Vanegas 
Luis Romero Cantillo 
Luis Miguel Floriano Ortegon

## Uso de IA
Se utilizó ChatGPT como asistente para el diseño y generación de una primera versión. El equipo debe revisar, probar, comprender y documentar sus cambios en la bitácora de IA antes de entregar.
