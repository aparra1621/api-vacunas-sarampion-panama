from app import app
import services


def test_get_vacuna_por_anio(monkeypatch):
    datos_falsos = [
        {"anio": 2000, "valor": 95.0, "pais": "Panamá", "indicador": "SH.IMM.MEAS"},
        {"anio": 2001, "valor": 96.0, "pais": "Panamá", "indicador": "SH.IMM.MEAS"},
    ]

    monkeypatch.setattr(services, "obtener_datos_banco_mundial", lambda: datos_falsos)

    client = app.test_client()
    response = client.get("/vacunas/2001")

    assert response.status_code == 200
    data = response.get_json()
    assert data["anio"] == 2001
    assert data["valor"] == 96.0
