from flask import Flask, jsonify
from services import (
    obtener_todos_los_registros,
    obtener_registro_por_anio,
    obtener_datos_provincia_simulados,
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "API GET-only de vacunación contra el sarampión en Panamá",
        "indicador": "SH.IMM.MEAS",
        "endpoints": [
            "/vacunas",
            "/vacunas/<anio>",
            "/vacunas/provincia/<nombre>"
        ]
    }), 200


@app.route("/vacunas", methods=["GET"])
def get_vacunas():
    try:
        data = obtener_todos_los_registros()
        return jsonify({
            "pais": "Panamá",
            "indicador": "SH.IMM.MEAS",
            "descripcion": "Cobertura de vacunación contra el sarampión (% de niños de 12 a 23 meses)",
            "total_registros": len(data),
            "datos": data
        }), 200
    except Exception as e:
        return jsonify({"error": f"No se pudieron obtener los datos: {str(e)}"}), 500


@app.route("/vacunas/<int:anio>", methods=["GET"])
def get_vacuna_por_anio(anio):
    try:
        registro = obtener_registro_por_anio(anio)
        if registro is None:
            return jsonify({"error": "No se encontró información para ese año."}), 404
        return jsonify(registro), 200
    except Exception as e:
        return jsonify({"error": f"No se pudo procesar la solicitud: {str(e)}"}), 500


@app.route("/vacunas/provincia/<nombre>", methods=["GET"])
def get_vacunas_provincia(nombre):
    try:
        data = obtener_datos_provincia_simulados(nombre)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"No se pudo procesar la solicitud: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
