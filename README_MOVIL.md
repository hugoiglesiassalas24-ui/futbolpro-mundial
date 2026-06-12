# FutbolPro Mundial Móvil

App web móvil para analizar partidos, pensada para abrirse desde el teléfono durante el Mundial.

## Qué incluye

- Modo manual/demo sin API.
- Modo Mundial 2026 con API-Football si añades una clave.
- Probabilidades 1X2.
- Goles esperados.
- Marcadores más probables.
- Over/Under 2.5.
- Ambos marcan.
- Córners, tarjetas y tiros a puerta estimados.
- Comparador de cuotas y posible valor.
- Diseño más cómodo para móvil.

## Cómo usarla desde el móvil

La app debe estar subida a internet. Lo más fácil es Streamlit Community Cloud.

### 1. Crear repositorio en GitHub

Sube estos archivos al repositorio:

- `streamlit_app.py`
- `requirements.txt`
- carpeta `.streamlit/config.toml`

### 2. Desplegar en Streamlit Cloud

1. Entra en Streamlit Community Cloud.
2. Conecta tu GitHub.
3. Elige el repositorio.
4. En "Main file path" pon:

```text
streamlit_app.py
```

5. Deploy.

### 3. Añadir API key opcional

Si quieres datos reales del Mundial con API-Football, añade en Streamlit Secrets:

```toml
APIFOOTBALL_KEY = "TU_CLAVE_AQUI"
```

También vale:

```toml
[api_football]
key = "TU_CLAVE_AQUI"
```

La app usa `league=1` y `season=2026` para el Mundial 2026 en API-Football.

### 4. Guardarla como app en el móvil

#### iPhone

Safari → abrir enlace de la app → botón compartir → Añadir a pantalla de inicio.

#### Android

Chrome → abrir enlace de la app → menú de tres puntos → Añadir a pantalla de inicio.

## Importante

Esta herramienta es de análisis estadístico. No garantiza resultados ni beneficios. Apostar implica riesgo de pérdida económica.
