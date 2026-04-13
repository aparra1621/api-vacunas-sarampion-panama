import requests

WORLD_BANK_URL = (
    "https://api.worldbank.org/v2/country/PAN/indicator/SH.IMM.MEAS"
    "?format=json&per_page=20000"
)

PROVINCIAS_VALIDAS = [
    "bocas-del-toro",
    "cocle",
    "colon",
    "chiriqui",
    "darien",
    "herrera",
    "los-santos",
    "panama",
    "panama-oeste",
    "veraguas"
]


def obtener_datos_banco_mundial():
    """
    Consulta la API del Banco Mundial y transforma la respuesta.
    """
    response = requests.get(WORLD_BANK_URL, timeout=20)
    response.raise_for_status()

    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError("Respuesta inválida del Banco Mundial.")

    registros = payload[1]
    datos_limpios = []

    for item in registros:
        if item.get("value") is None:
            continue

        datos_limpios.append({
            "anio": int(item["date"]),
            "valor": float(item["value"]),
            "pais": item["country"]["value"],
            "indicador": item["indicator"]["id"]
        })

    datos_limpios.sort(key=lambda x: x["anio"])
    return datos_limpios


def obtener_todos_los_registros():
    return obtener_datos_banco_mundial()


def obtener_registro_por_anio(anio):
    datos = obtener_datos_banco_mundial()
    for registro in datos:
        if registro["anio"] == anio:
            return registro
    return None


def obtener_datos_provincia_simulados(nombre):
    """
    Genera datos simulados por provincia usando la serie nacional
    como base, solo con fines académicos.
    """
    provincia = nombre.strip().lower()

    base = obtener_datos_banco_mundial()

    if provincia not in PROVINCIAS_VALIDAS:
        return {
            "provincia": provincia,
            "simulado": True,
            "mensaje": "Provincia no reconocida. Usa por ejemplo: panama, chiriqui, colon o veraguas.",
            "datos": []
        }

    ajustes = {
        "bocas-del-toro": -2.0,
        "cocle": -0.8,
        "colon": -1.5,
        "chiriqui": 0.6,
        "darien": -2.3,
        "herrera": 0.9,
        "los-santos": 1.2,
        "panama": 0.4,
        "panama-oeste": -0.4,
        "veraguas": -0.9
    }

    ajuste = ajustes[provincia]
    datos_simulados = []

    for registro in base:
        valor = max(0.0, min(100.0, round(registro["valor"] + ajuste, 1)))
        datos_simulados.append({
            "anio": registro["anio"],
            "valor": valor
        })

    return {
        "provincia": provincia,
        "simulado": True,
        "base": "Serie nacional del Banco Mundial ajustada con fines académicos",
        "datos": datos_simulados
    }
