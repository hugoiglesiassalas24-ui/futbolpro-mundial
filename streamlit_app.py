import math
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import requests
import streamlit as st


# ==========================================================
# FUTBOLPRO MUNDIAL MÓVIL
# App web móvil para análisis estadístico de partidos
# ==========================================================

st.set_page_config(
    page_title="FutbolPro Mundial",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# -----------------------------
# CSS móvil
# -----------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-left: 0.75rem;
        padding-right: 0.75rem;
        max-width: 780px;
    }
    div[data-testid="stMetric"] {
        background: #f7f7f9;
        border: 1px solid #ececf1;
        padding: 10px;
        border-radius: 14px;
    }
    .big-card {
        background: #ffffff;
        border: 1px solid #ececf1;
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,.04);
    }
    .risk {
        background: #fff7e6;
        border: 1px solid #ffd591;
        border-radius: 14px;
        padding: 12px;
        font-size: 0.94rem;
    }
    .ok-card {
        background: #f6ffed;
        border: 1px solid #b7eb8f;
        border-radius: 14px;
        padding: 12px;
    }
    .bad-card {
        background: #fff1f0;
        border: 1px solid #ffa39e;
        border-radius: 14px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Datos demo internacionales
# -----------------------------

DEMO_TEAMS = pd.DataFrame([
    {"Equipo": "España", "Partidos": 20, "Goles_Favor": 42, "Goles_Contra": 17, "xG_Favor": 40.8, "xG_Contra": 18.9, "Corners_Favor": 126, "Corners_Contra": 79, "Tarjetas_Favor": 36, "Tarjetas_Contra": 47, "Tiros_Puerta_Favor": 133, "Tiros_Puerta_Contra": 71, "Forma_5": 12, "Elo": 1905},
    {"Equipo": "Francia", "Partidos": 20, "Goles_Favor": 44, "Goles_Contra": 19, "xG_Favor": 42.1, "xG_Contra": 20.5, "Corners_Favor": 121, "Corners_Contra": 83, "Tarjetas_Favor": 39, "Tarjetas_Contra": 50, "Tiros_Puerta_Favor": 136, "Tiros_Puerta_Contra": 76, "Forma_5": 11, "Elo": 1920},
    {"Equipo": "Brasil", "Partidos": 20, "Goles_Favor": 41, "Goles_Contra": 20, "xG_Favor": 39.5, "xG_Contra": 22.1, "Corners_Favor": 117, "Corners_Contra": 88, "Tarjetas_Favor": 45, "Tarjetas_Contra": 48, "Tiros_Puerta_Favor": 128, "Tiros_Puerta_Contra": 82, "Forma_5": 10, "Elo": 1888},
    {"Equipo": "Argentina", "Partidos": 20, "Goles_Favor": 38, "Goles_Contra": 18, "xG_Favor": 37.6, "xG_Contra": 19.7, "Corners_Favor": 112, "Corners_Contra": 80, "Tarjetas_Favor": 47, "Tarjetas_Contra": 45, "Tiros_Puerta_Favor": 121, "Tiros_Puerta_Contra": 74, "Forma_5": 12, "Elo": 1898},
    {"Equipo": "Inglaterra", "Partidos": 20, "Goles_Favor": 40, "Goles_Contra": 21, "xG_Favor": 38.9, "xG_Contra": 22.8, "Corners_Favor": 119, "Corners_Contra": 86, "Tarjetas_Favor": 33, "Tarjetas_Contra": 52, "Tiros_Puerta_Favor": 127, "Tiros_Puerta_Contra": 80, "Forma_5": 10, "Elo": 1880},
    {"Equipo": "Alemania", "Partidos": 20, "Goles_Favor": 36, "Goles_Contra": 24, "xG_Favor": 36.3, "xG_Contra": 25.1, "Corners_Favor": 115, "Corners_Contra": 94, "Tarjetas_Favor": 41, "Tarjetas_Contra": 46, "Tiros_Puerta_Favor": 118, "Tiros_Puerta_Contra": 89, "Forma_5": 9, "Elo": 1835},
    {"Equipo": "Portugal", "Partidos": 20, "Goles_Favor": 39, "Goles_Contra": 22, "xG_Favor": 37.9, "xG_Contra": 23.5, "Corners_Favor": 116, "Corners_Contra": 90, "Tarjetas_Favor": 43, "Tarjetas_Contra": 47, "Tiros_Puerta_Favor": 123, "Tiros_Puerta_Contra": 84, "Forma_5": 10, "Elo": 1855},
    {"Equipo": "Países Bajos", "Partidos": 20, "Goles_Favor": 35, "Goles_Contra": 22, "xG_Favor": 34.2, "xG_Contra": 23.4, "Corners_Favor": 106, "Corners_Contra": 87, "Tarjetas_Favor": 40, "Tarjetas_Contra": 49, "Tiros_Puerta_Favor": 108, "Tiros_Puerta_Contra": 83, "Forma_5": 9, "Elo": 1815},
    {"Equipo": "Uruguay", "Partidos": 20, "Goles_Favor": 31, "Goles_Contra": 21, "xG_Favor": 30.8, "xG_Contra": 22.9, "Corners_Favor": 99, "Corners_Contra": 86, "Tarjetas_Favor": 54, "Tarjetas_Contra": 44, "Tiros_Puerta_Favor": 103, "Tiros_Puerta_Contra": 82, "Forma_5": 9, "Elo": 1785},
    {"Equipo": "Marruecos", "Partidos": 20, "Goles_Favor": 29, "Goles_Contra": 19, "xG_Favor": 28.7, "xG_Contra": 20.4, "Corners_Favor": 94, "Corners_Contra": 82, "Tarjetas_Favor": 49, "Tarjetas_Contra": 45, "Tiros_Puerta_Favor": 96, "Tiros_Puerta_Contra": 76, "Forma_5": 10, "Elo": 1765},
    {"Equipo": "México", "Partidos": 20, "Goles_Favor": 27, "Goles_Contra": 24, "xG_Favor": 27.4, "xG_Contra": 25.3, "Corners_Favor": 93, "Corners_Contra": 91, "Tarjetas_Favor": 51, "Tarjetas_Contra": 43, "Tiros_Puerta_Favor": 91, "Tiros_Puerta_Contra": 87, "Forma_5": 8, "Elo": 1715},
    {"Equipo": "Estados Unidos", "Partidos": 20, "Goles_Favor": 30, "Goles_Contra": 25, "xG_Favor": 30.2, "xG_Contra": 26.1, "Corners_Favor": 102, "Corners_Contra": 93, "Tarjetas_Favor": 44, "Tarjetas_Contra": 46, "Tiros_Puerta_Favor": 101, "Tiros_Puerta_Contra": 88, "Forma_5": 8, "Elo": 1730},
])


# -----------------------------
# Estadística básica
# -----------------------------

def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def poisson_pmf(k: int, lam: float) -> float:
    lam = max(float(lam), 0.01)
    return (math.exp(-lam) * lam ** k) / math.factorial(k)


def fair_odds(probability: float) -> float:
    return float("inf") if probability <= 0 else 1 / probability


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def per_match(row: pd.Series, col: str) -> float:
    return float(row[col]) / max(float(row["Partidos"]), 1)


def league_avg(df: pd.DataFrame, col: str) -> float:
    return float(df[col].sum()) / max(float(df["Partidos"].sum()), 1)


def poisson_matrix(lambda_home: float, lambda_away: float, max_goals: int = 8) -> pd.DataFrame:
    data = []
    for h in range(max_goals + 1):
        data.append([poisson_pmf(h, lambda_home) * poisson_pmf(a, lambda_away) for a in range(max_goals + 1)])
    return pd.DataFrame(data, index=list(range(max_goals + 1)), columns=list(range(max_goals + 1)))


def outcome_probs(matrix: pd.DataFrame) -> Dict[str, float]:
    out = {"Local": 0.0, "Empate": 0.0, "Visitante": 0.0}
    for h in matrix.index:
        for a in matrix.columns:
            p = float(matrix.loc[h, a])
            if h > a:
                out["Local"] += p
            elif h == a:
                out["Empate"] += p
            else:
                out["Visitante"] += p
    s = sum(out.values())
    return {k: v / s for k, v in out.items()}


def market_probs(matrix: pd.DataFrame) -> Dict[str, float]:
    out = {
        "Over 1.5": 0.0,
        "Over 2.5": 0.0,
        "Over 3.5": 0.0,
        "Under 2.5": 0.0,
        "BTTS Sí": 0.0,
        "BTTS No": 0.0,
    }
    for h in matrix.index:
        for a in matrix.columns:
            p = float(matrix.loc[h, a])
            total = int(h) + int(a)
            if total >= 2:
                out["Over 1.5"] += p
            if total >= 3:
                out["Over 2.5"] += p
            if total >= 4:
                out["Over 3.5"] += p
            if total <= 2:
                out["Under 2.5"] += p
            if int(h) > 0 and int(a) > 0:
                out["BTTS Sí"] += p
            else:
                out["BTTS No"] += p
    return out


def score_table(matrix: pd.DataFrame, n: int = 8) -> pd.DataFrame:
    rows = []
    for h in matrix.index:
        for a in matrix.columns:
            rows.append({"Marcador": f"{h}-{a}", "Probabilidad": float(matrix.loc[h, a])})
    df = pd.DataFrame(rows).sort_values("Probabilidad", ascending=False).head(n)
    df["Probabilidad"] = df["Probabilidad"].map(lambda x: f"{100*x:.2f}%")
    return df.reset_index(drop=True)


def model_match(
    teams_df: pd.DataFrame,
    home_team: str,
    away_team: str,
    use_xg: bool = True,
    home_advantage: float = 1.10,
    form_weight: float = 0.12,
    elo_weight: float = 0.20,
) -> Dict[str, object]:

    home = teams_df[teams_df["Equipo"] == home_team].iloc[0]
    away = teams_df[teams_df["Equipo"] == away_team].iloc[0]

    base_col_for = "xG_Favor" if use_xg else "Goles_Favor"
    base_col_against = "xG_Contra" if use_xg else "Goles_Contra"
    base = league_avg(teams_df, base_col_for)

    h_attack = per_match(home, base_col_for) / max(base, 0.01)
    a_attack = per_match(away, base_col_for) / max(base, 0.01)
    h_def_allowed = per_match(home, base_col_against) / max(base, 0.01)
    a_def_allowed = per_match(away, base_col_against) / max(base, 0.01)

    h_form = 1 + form_weight * ((float(home["Forma_5"]) - 7.5) / 7.5)
    a_form = 1 + form_weight * ((float(away["Forma_5"]) - 7.5) / 7.5)

    elo_diff = float(home["Elo"]) - float(away["Elo"])
    elo_adj = clamp(elo_diff / 400, -0.35, 0.35)

    h_elo = 1 + elo_weight * elo_adj
    a_elo = 1 - elo_weight * elo_adj

    lambda_home = base * h_attack * a_def_allowed * home_advantage * h_form * h_elo
    lambda_away = base * a_attack * h_def_allowed * (2 - home_advantage) * a_form * a_elo

    lambda_home = clamp(lambda_home, 0.15, 4.5)
    lambda_away = clamp(lambda_away, 0.15, 4.5)

    matrix = poisson_matrix(lambda_home, lambda_away, 8)
    op = outcome_probs(matrix)
    mp = market_probs(matrix)

    h_corners = (per_match(home, "Corners_Favor") + per_match(away, "Corners_Contra")) / 2
    a_corners = (per_match(away, "Corners_Favor") + per_match(home, "Corners_Contra")) / 2
    h_cards = (per_match(home, "Tarjetas_Favor") + per_match(away, "Tarjetas_Contra")) / 2
    a_cards = (per_match(away, "Tarjetas_Favor") + per_match(home, "Tarjetas_Contra")) / 2
    h_sot = (per_match(home, "Tiros_Puerta_Favor") + per_match(away, "Tiros_Puerta_Contra")) / 2
    a_sot = (per_match(away, "Tiros_Puerta_Favor") + per_match(home, "Tiros_Puerta_Contra")) / 2

    top = max(op, key=op.get)
    top_prob = op[top]
    confidence = "Alta" if top_prob >= 0.58 else "Media" if top_prob >= 0.48 else "Baja"

    return {
        "lambda_home": lambda_home,
        "lambda_away": lambda_away,
        "matrix": matrix,
        "outcome_probs": op,
        "market_probs": mp,
        "scores": score_table(matrix),
        "corners": {"Local": h_corners, "Visitante": a_corners, "Total": h_corners + a_corners},
        "cards": {"Local": h_cards, "Visitante": a_cards, "Total": h_cards + a_cards},
        "sot": {"Local": h_sot, "Visitante": a_sot, "Total": h_sot + a_sot},
        "pick": top,
        "pick_prob": top_prob,
        "confidence": confidence,
    }


def implied_prob(odds: float) -> float:
    if odds <= 1:
        return np.nan
    return 1 / odds


def value_row(name: str, probability: float, odds: float, min_edge: float) -> Dict[str, object]:
    ip = implied_prob(odds)
    edge = probability - ip if not np.isnan(ip) else np.nan
    if np.isnan(edge):
        label = "Sin cuota"
    elif edge >= min_edge:
        label = "Posible valor"
    elif edge >= 0:
        label = "Muy justo"
    else:
        label = "Sin valor"
    return {
        "Mercado": name,
        "Cuota": odds,
        "Prob. modelo": probability,
        "Cuota justa": fair_odds(probability),
        "Prob. cuota": ip,
        "Edge": edge,
        "Lectura": label,
    }


# -----------------------------
# API-Football opcional
# -----------------------------

def get_api_key() -> Optional[str]:
    # Streamlit Secrets:
    # APIFOOTBALL_KEY = "..."
    # o bien:
    # [api_football]
    # key = "..."
    try:
        if "APIFOOTBALL_KEY" in st.secrets:
            return st.secrets["APIFOOTBALL_KEY"]
    except Exception:
        pass
    try:
        if "api_football" in st.secrets and "key" in st.secrets["api_football"]:
            return st.secrets["api_football"]["key"]
    except Exception:
        pass
    return None


@st.cache_data(ttl=600, show_spinner=False)
def api_get(endpoint: str, api_key: str, params: Dict[str, object]) -> Dict[str, object]:
    url = f"https://v3.football.api-sports.io/{endpoint.lstrip('/')}"
    headers = {"x-apisports-key": api_key}
    r = requests.get(url, headers=headers, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def load_worldcup_fixtures(api_key: str) -> pd.DataFrame:
    data = api_get(
        "fixtures",
        api_key,
        {"league": 1, "season": 2026, "timezone": "Europe/Madrid"}
    )
    rows = []
    for item in data.get("response", []):
        fixture = item.get("fixture", {})
        teams = item.get("teams", {})
        goals = item.get("goals", {})
        league = item.get("league", {})
        rows.append({
            "fixture_id": fixture.get("id"),
            "fecha": fixture.get("date"),
            "estado": fixture.get("status", {}).get("short"),
            "ronda": league.get("round"),
            "local": teams.get("home", {}).get("name"),
            "visitante": teams.get("away", {}).get("name"),
            "home_id": teams.get("home", {}).get("id"),
            "away_id": teams.get("away", {}).get("id"),
            "goles_local": goals.get("home"),
            "goles_visitante": goals.get("away"),
            "venue": fixture.get("venue", {}).get("name"),
            "city": fixture.get("venue", {}).get("city"),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["fecha_dt"] = pd.to_datetime(df["fecha"], errors="coerce")
        df = df.sort_values("fecha_dt")
    return df


def load_api_prediction(api_key: str, fixture_id: int) -> Optional[Dict[str, object]]:
    try:
        data = api_get("predictions", api_key, {"fixture": fixture_id})
        resp = data.get("response", [])
        return resp[0] if resp else None
    except Exception:
        return None


def load_fixture_stats(api_key: str, fixture_id: int) -> Optional[pd.DataFrame]:
    try:
        data = api_get("fixtures/statistics", api_key, {"fixture": fixture_id})
        rows = []
        for team_block in data.get("response", []):
            team_name = team_block.get("team", {}).get("name", "")
            for stat in team_block.get("statistics", []):
                rows.append({
                    "Equipo": team_name,
                    "Estadística": stat.get("type"),
                    "Valor": stat.get("value")
                })
        return pd.DataFrame(rows)
    except Exception:
        return None


# -----------------------------
# Cabecera
# -----------------------------

st.title("⚽ FutbolPro Mundial")
st.caption("Análisis rápido de partidos desde el móvil. Versión web/PWA.")

api_key = get_api_key()

with st.expander("📱 Cómo usarla como app en el móvil", expanded=False):
    st.markdown(
        """
        **iPhone:** abre el enlace en Safari → botón compartir → **Añadir a pantalla de inicio**.  
        **Android:** abre el enlace en Chrome → menú ⋮ → **Añadir a pantalla de inicio**.

        Así la tendrás como icono, aunque por dentro sea una app web.
        """
    )

st.markdown(
    """
    <div class="risk">
    <b>Aviso:</b> esto es análisis estadístico. No garantiza aciertos ni beneficios. 
    Si se usa para apostar, debe hacerse con responsabilidad y sabiendo que se puede perder dinero.
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Entrada de partido
# -----------------------------

mode = st.radio(
    "Modo",
    ["Mundial 2026 con API", "Manual/demo"],
    horizontal=True,
    index=0 if api_key else 1,
)

teams_df = DEMO_TEAMS.copy()

selected_home = None
selected_away = None
selected_fixture_id = None
fixture_label = None
fixture_stats_df = None
api_prediction = None

if mode == "Mundial 2026 con API":
    if not api_key:
        st.error("No hay clave API configurada. Usa el modo Manual/demo o añade tu API key en Streamlit Secrets.")
    else:
        try:
            fixtures_df = load_worldcup_fixtures(api_key)
            if fixtures_df.empty:
                st.warning("La API no ha devuelto partidos. Prueba en modo manual.")
            else:
                today = pd.Timestamp.now(tz="Europe/Madrid")
                upcoming = fixtures_df[fixtures_df["fecha_dt"] >= today].copy()
                base_df = upcoming if not upcoming.empty else fixtures_df

                labels = []
                for _, r in base_df.iterrows():
                    date_txt = r["fecha_dt"].strftime("%d/%m %H:%M") if pd.notnull(r["fecha_dt"]) else "Fecha desconocida"
                    labels.append(f"{date_txt} · {r['local']} vs {r['visitante']} · {r.get('ronda', '')}")

                picked_label = st.selectbox("Partido del Mundial", labels)
                idx = labels.index(picked_label)
                picked = base_df.iloc[idx]

                selected_home = picked["local"]
                selected_away = picked["visitante"]
                selected_fixture_id = int(picked["fixture_id"]) if pd.notnull(picked["fixture_id"]) else None
                fixture_label = picked_label

                st.markdown(
                    f"""
                    <div class="big-card">
                    <b>{selected_home} vs {selected_away}</b><br>
                    {picked.get('ronda', '')}<br>
                    {picked.get('venue', '')} · {picked.get('city', '')}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if selected_fixture_id:
                    api_prediction = load_api_prediction(api_key, selected_fixture_id)
                    fixture_stats_df = load_fixture_stats(api_key, selected_fixture_id)

                if selected_home not in teams_df["Equipo"].values:
                    st.info("Ese equipo no está en la tabla demo. Puedes analizarlo en manual introduciendo nombres similares o ampliar el CSV base.")
        except Exception as e:
            st.error(f"No se pudo cargar la API: {e}")

if mode == "Manual/demo" or selected_home not in teams_df["Equipo"].values or selected_away not in teams_df["Equipo"].values:
    teams = sorted(teams_df["Equipo"].tolist())
    c1, c2 = st.columns(2)
    with c1:
        selected_home = st.selectbox("Local", teams, index=0)
    with c2:
        away_options = [t for t in teams if t != selected_home]
        selected_away = st.selectbox("Visitante", away_options, index=0)


with st.expander("⚙️ Ajustes del modelo", expanded=False):
    use_xg = st.toggle("Usar xG si está disponible", value=True)
    home_advantage = st.slider("Ventaja local", 1.00, 1.30, 1.10, 0.01)
    form_weight = st.slider("Peso de forma reciente", 0.00, 0.30, 0.12, 0.01)
    elo_weight = st.slider("Peso Elo/ranking", 0.00, 0.50, 0.20, 0.01)
    min_edge = st.slider("Edge mínimo para posible valor", 0.00, 0.15, 0.05, 0.01)


# -----------------------------
# Resultado modelo
# -----------------------------

if not selected_home or not selected_away or selected_home == selected_away:
    st.stop()

result = model_match(
    teams_df,
    selected_home,
    selected_away,
    use_xg=use_xg,
    home_advantage=home_advantage,
    form_weight=form_weight,
    elo_weight=elo_weight,
)

st.subheader(f"{selected_home} vs {selected_away}")

m1, m2 = st.columns(2)
m1.metric("Predicción", result["pick"], pct(result["pick_prob"]))
m2.metric("Confianza", result["confidence"])

m3, m4 = st.columns(2)
m3.metric("Goles esperados", f"{result['lambda_home'] + result['lambda_away']:.2f}",
          f"{selected_home} {result['lambda_home']:.2f} - {selected_away} {result['lambda_away']:.2f}")
m4.metric("Córners esperados", f"{result['corners']['Total']:.1f}",
          f"{result['corners']['Local']:.1f} - {result['corners']['Visitante']:.1f}")


# -----------------------------
# Tabs
# -----------------------------

tab1, tab2, tab3, tab4 = st.tabs(["Pronóstico", "Cuotas", "Stats", "API"])

with tab1:
    st.markdown("### Probabilidades principales")

    probs = result["outcome_probs"]
    markets = result["market_probs"]

    prob_df = pd.DataFrame([
        {"Mercado": "Gana local", "Probabilidad": probs["Local"], "Cuota justa": fair_odds(probs["Local"])},
        {"Mercado": "Empate", "Probabilidad": probs["Empate"], "Cuota justa": fair_odds(probs["Empate"])},
        {"Mercado": "Gana visitante", "Probabilidad": probs["Visitante"], "Cuota justa": fair_odds(probs["Visitante"])},
        {"Mercado": "Over 2.5", "Probabilidad": markets["Over 2.5"], "Cuota justa": fair_odds(markets["Over 2.5"])},
        {"Mercado": "Under 2.5", "Probabilidad": markets["Under 2.5"], "Cuota justa": fair_odds(markets["Under 2.5"])},
        {"Mercado": "Ambos marcan Sí", "Probabilidad": markets["BTTS Sí"], "Cuota justa": fair_odds(markets["BTTS Sí"])},
        {"Mercado": "Ambos marcan No", "Probabilidad": markets["BTTS No"], "Cuota justa": fair_odds(markets["BTTS No"])},
    ])
    show = prob_df.copy()
    show["Probabilidad"] = show["Probabilidad"].map(lambda x: f"{100*x:.1f}%")
    show["Cuota justa"] = show["Cuota justa"].map(lambda x: f"{x:.2f}")
    st.dataframe(show, hide_index=True, use_container_width=True)

    st.markdown("### Marcadores más probables")
    st.dataframe(result["scores"], hide_index=True, use_container_width=True)

    st.markdown("### Lectura rápida")
    explanation = (
        f"El modelo da como opción más probable: **{result['pick']}**. "
        f"Los goles esperados son {result['lambda_home']:.2f} para {selected_home} "
        f"y {result['lambda_away']:.2f} para {selected_away}. "
        f"Para córners, la línea orientativa total es **{result['corners']['Total']:.1f}**."
    )
    st.info(explanation)

with tab2:
    st.markdown("### Comparar con cuotas")

    c1, c2 = st.columns(2)
    with c1:
        odds_home = st.number_input("Cuota local", min_value=1.01, max_value=80.0, value=2.00, step=0.01)
        odds_away = st.number_input("Cuota visitante", min_value=1.01, max_value=80.0, value=3.40, step=0.01)
        odds_btts_yes = st.number_input("Cuota ambos marcan Sí", min_value=1.01, max_value=80.0, value=1.90, step=0.01)
    with c2:
        odds_draw = st.number_input("Cuota empate", min_value=1.01, max_value=80.0, value=3.20, step=0.01)
        odds_o25 = st.number_input("Cuota Over 2.5", min_value=1.01, max_value=80.0, value=1.95, step=0.01)
        odds_u25 = st.number_input("Cuota Under 2.5", min_value=1.01, max_value=80.0, value=1.85, step=0.01)

    value_df = pd.DataFrame([
        value_row("Gana local", probs["Local"], odds_home, min_edge),
        value_row("Empate", probs["Empate"], odds_draw, min_edge),
        value_row("Gana visitante", probs["Visitante"], odds_away, min_edge),
        value_row("Over 2.5", markets["Over 2.5"], odds_o25, min_edge),
        value_row("Under 2.5", markets["Under 2.5"], odds_u25, min_edge),
        value_row("Ambos marcan Sí", markets["BTTS Sí"], odds_btts_yes, min_edge),
    ])

    show_value = value_df.copy()
    for col in ["Prob. modelo", "Prob. cuota", "Edge"]:
        show_value[col] = show_value[col].map(lambda x: "" if pd.isna(x) else f"{100*x:.1f}%")
    show_value["Cuota justa"] = show_value["Cuota justa"].map(lambda x: f"{x:.2f}")
    show_value["Cuota"] = show_value["Cuota"].map(lambda x: f"{x:.2f}")

    st.dataframe(show_value, hide_index=True, use_container_width=True)

    picks = value_df[value_df["Lectura"] == "Posible valor"].sort_values("Edge", ascending=False)
    if not picks.empty:
        best = picks.iloc[0]
        st.markdown(
            f"""
            <div class="ok-card">
            <b>Mayor posible valor:</b> {best['Mercado']}<br>
            Probabilidad modelo: {100*best['Prob. modelo']:.1f}% · Cuota justa: {best['Cuota justa']:.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="bad-card">
            No aparece valor claro con estas cuotas. Mejor no forzar lectura.
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab3:
    st.markdown("### Estimaciones extra")

    extra_df = pd.DataFrame([
        {"Métrica": "Córners local", "Estimación": result["corners"]["Local"]},
        {"Métrica": "Córners visitante", "Estimación": result["corners"]["Visitante"]},
        {"Métrica": "Córners totales", "Estimación": result["corners"]["Total"]},
        {"Métrica": "Tarjetas local", "Estimación": result["cards"]["Local"]},
        {"Métrica": "Tarjetas visitante", "Estimación": result["cards"]["Visitante"]},
        {"Métrica": "Tarjetas totales", "Estimación": result["cards"]["Total"]},
        {"Métrica": "Tiros puerta local", "Estimación": result["sot"]["Local"]},
        {"Métrica": "Tiros puerta visitante", "Estimación": result["sot"]["Visitante"]},
        {"Métrica": "Tiros puerta totales", "Estimación": result["sot"]["Total"]},
    ])
    extra_df["Estimación"] = extra_df["Estimación"].map(lambda x: round(float(x), 2))
    st.dataframe(extra_df, hide_index=True, use_container_width=True)

    st.markdown("### Datos base")
    st.dataframe(teams_df, hide_index=True, use_container_width=True)

with tab4:
    st.markdown("### Estado de conexión")
    if api_key:
        st.success("API key detectada.")
    else:
        st.warning("Sin API key. La app funciona en modo manual/demo.")

    if api_prediction:
        st.markdown("### Predicción devuelta por API-Football")
        pred = api_prediction.get("predictions", {})
        percent = pred.get("percent", {})
        winner = pred.get("winner", {})
        goals = pred.get("goals", {})

        api_rows = []
        if percent:
            api_rows.extend([
                {"Dato": "Local", "Valor": percent.get("home")},
                {"Dato": "Empate", "Valor": percent.get("draw")},
                {"Dato": "Visitante", "Valor": percent.get("away")},
            ])
        if winner:
            api_rows.append({"Dato": "Ganador API", "Valor": winner.get("name")})
        if goals:
            api_rows.extend([
                {"Dato": "Goles over/under API", "Valor": goals.get("under_over")},
            ])
        if api_rows:
            st.dataframe(pd.DataFrame(api_rows), hide_index=True, use_container_width=True)
        else:
            st.json(pred)
    else:
        st.info("No hay predicción API para este partido o tu plan no la permite.")

    if fixture_stats_df is not None and not fixture_stats_df.empty:
        st.markdown("### Estadísticas oficiales del fixture")
        st.dataframe(fixture_stats_df, hide_index=True, use_container_width=True)
    else:
        st.info("No hay estadísticas de fixture todavía. Suelen aparecer durante o después del partido.")
