from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = Path(os.getenv("PORRA_CSV_PATH", BASE_DIR / "data" / "porra_mundial_muestra_40.csv"))
ASSETS_DIR = BASE_DIR / "assets"
FLAG_DIR = ASSETS_DIR / "flags"
LOGO_PATH = ASSETS_DIR / "logo" / "logo.webp"

GROUP_COLORS = {
    "A": "#6BBF78",
    "B": "#EC1522",
    "C": "#EAEA7E",
    "D": "#0C66B6",
    "E": "#F48020",
    "F": "#006858",
    "G": "#B0A8D9",
    "H": "#55BCBB",
    "I": "#4E3AA2",
    "J": "#FEA999",
    "K": "#F0417A",
    "L": "#82001C",
}

GROUPS = {
    "A": ["Mexico", "Sudafrica", "Corea", "Irlanda"],
    "B": ["Canada", "Italia", "Qatar", "Suiza"],
    "C": ["Brasil", "Marruecos", "Haiti", "Escocia"],
    "D": ["USA", "Paraguay", "Australia", "Turquia"],
    "E": ["Alemania", "Curazao", "CostaMarfil", "Ecuador"],
    "F": ["Holanda", "Japon", "Suecia", "Tunez"],
    "G": ["Belgica", "Egipto", "Iran", "NuevaZelanda"],
    "H": ["Espana", "CaboVerde", "ArabiaSaudi", "Uruguay"],
    "I": ["Francia", "Senegal", "Bolivia", "Noruega"],
    "J": ["Argentina", "Argelia", "Austria", "Jordania"],
    "K": ["Portugal", "Jamaica", "Uzbekistan", "Colombia"],
    "L": ["Inglaterra", "Croacia", "Ghana", "Panama"],
}

TEAM_DISPLAY = {
    "Alemania": "Alemania",
    "ArabiaSaudi": "Arabia Saudí",
    "Argelia": "Argelia",
    "Argentina": "Argentina",
    "Australia": "Australia",
    "Austria": "Austria",
    "Belgica": "Bélgica",
    "Bolivia": "Bolivia",
    "Brasil": "Brasil",
    "CaboVerde": "Cabo Verde",
    "Canada": "Canadá",
    "Colombia": "Colombia",
    "Corea": "Corea",
    "CostaMarfil": "Costa Marfil",
    "Croacia": "Croacia",
    "Curazao": "Curazao",
    "Ecuador": "Ecuador",
    "Egipto": "Egipto",
    "Escocia": "Escocia",
    "Espana": "España",
    "Francia": "Francia",
    "Ghana": "Ghana",
    "Haiti": "Haiti",
    "Holanda": "Holanda",
    "Inglaterra": "Inglaterra",
    "Iran": "Irán",
    "Irlanda": "Irlanda",
    "Italia": "Italia",
    "Jamaica": "Jamaica",
    "Japon": "Japón",
    "Jordania": "Jordania",
    "Marruecos": "Marruecos",
    "Mexico": "México",
    "Noruega": "Noruega",
    "NuevaZelanda": "Nueva Zelanda",
    "Panama": "Panamá",
    "Paraguay": "Paraguay",
    "Portugal": "Portugal",
    "Qatar": "Qatar",
    "Senegal": "Senegal",
    "Sudafrica": "Sudáfrica",
    "Suecia": "Suecia",
    "Suiza": "Suiza",
    "Tunez": "Túnez",
    "Turquia": "Turquia",
    "USA": "USA",
    "Uruguay": "Uruguay",
    "Uzbekistan": "Uzbekistán",
}

FLAG_FILES = {team: FLAG_DIR / f"{team}.png" for team in TEAM_DISPLAY}

SPECIAL_FIELDS = [
    ("MejorJugador", "Mejor Jugador"),
    ("MejorJugadorJoven", "Mejor Jugador Joven"),
    ("MejorPortero", "Mejor Portero"),
    ("MaximoGoleador", "Máximo Goleador"),
    ("MaximoAsistente", "Máximo Asistente"),
    ("MaximoGoleadorESP", "Máximo Goleador Español"),
    ("SeleccionRevelacion", "Selección Revelación"),
    ("SeleccionDecepcion", "Selección Decepción"),
    ("MinutoPrimerGol", "Minuto Primer Gol del Mundial"),
    ("PrimerGolESP", "Primer Goleador Español"),
]

TEAM_SPECIAL_FIELDS = {"SeleccionRevelacion", "SeleccionDecepcion"}

STAGE_CONFIGS = [
    ("Equipos más elegidos para pasar a dieciseisavos", "EquipoR32", 32),
    ("Equipos más elegidos para octavos", "EquipoOctavos", 16),
    ("Equipos más elegidos para cuartos", "EquipoCuartos", 8),
    ("Equipos más elegidos para semifinales", "EquipoSemis", 4),
    ("Equipos más elegidos para la final", "EquipoFinal", 2),
]

FINAL_TABLE_COLUMNS = [
    ("Posición", "Posicion"),
    ("Participante", "Participante"),
    ("Puntos totales", "TOTAL_PUNTOS"),
    ("Puntos fase de grupos", "PUNTOS_FASE_DE_GRUPOS"),
    ("Puntos fase final", "PUNTOS_FASE_FINAL"),
    ("Puntos especiales", "PUNTOS_ESPECIALES"),
    ("Campeón", "Campeon"),
    ("Subcampeón", "Subcampeon"),
    ("Tercer Puesto", "TercerPuesto"),
    ("Mejor Jugador", "MejorJugador"),
    ("Mejor Jugador Joven", "MejorJugadorJoven"),
    ("Mejor Portero", "MejorPortero"),
    ("Máximo Goleador", "MaximoGoleador"),
    ("Máximo Asistente", "MaximoAsistente"),
    ("Máximo Goleador Español", "MaximoGoleadorESP"),
    ("Minuto Primer Gol del Mundial", "MinutoPrimerGol"),
    ("Primer Goleador Español", "PrimerGolESP"),
]

EXACT_RESULT_POINTS = {3, 6}
MATCH_SIGN_POINTS = {2, 4}
RANK_NUMERIC_COLUMNS = [
    "TOTAL_PUNTOS",
    "PUNTOS_FASE_DE_GRUPOS",
    "PUNTOS_FASE_FINAL",
    "PUNTOS_ESPECIALES",
]

NEGATIVE_METRIC_LABELS = {
    "worst_streak": "Participante con peor racha de aciertos de resultados",
    "least_hits": "Participante con menos resultados acertados",
}

POSITIVE_METRIC_LABELS = {
    "best_streak": "Participante con mayor racha de aciertos de resultados",
    "most_hits": "Participante con más resultados acertados",
}
