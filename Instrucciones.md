# Instrucciones para Clasificación y Visualización de Artículos de Biociencia

## 4. Backend API
- Leer una base de datos alojada en google cloud
  - table category
    - nombre del la categoria
  - Tabla en base llamada articles
    - Categorias
    - Titulo del articulo
    - Url del articulo
    - categoria a la que pertenece
    - description del articulo
- Reetorno de datos de la base de datos
  - Categorias del articulo
  - Titulo del articulo
  - Url del articulo
  - descripcion

## 5. Frontend
- Consume la API para obtener los datos y llenar las categorias
- Mostrar las temáticas (las categorias) como tarjetas (cards) en la página principal.
- Al seleccionar una temática, hacer una petición a la API para obtener los artículos y sus resúmenes.
- Mostrar la descipcion y detalles de los artículos en tarjetas individuales.
- Crea datos dummy con el archivo de ejemplo
---

## Plan de Acción
1. Desarollar en la API para popular la base de datos con los datos de este CSV C:\Users\RYZEN 5\OneDrive\Escritorio\Jobs\NASA-Challenge\SB_publication_categorizado_NASA_temas.csv
1. **Desarrollar una API backend para exponer los datos y resúmenes.**
2. **Integrar servicios de resumen automático usando IA de Google Cloud.**
3. **Desarrollar el frontend para mostrar temáticas y artículos clasificados.**
4. **Implementar autenticación y seguridad en la API y frontend.**
5. **Realizar pruebas de extremo a extremo y documentar el flujo.**

---

¿Te gustaría que te ayude a iniciar con algún paso específico (por ejemplo, el script de clasificación o la estructura de la API)?
