import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Déposez votre code à partir d'ici :

@app.route("/contact")
def MaPremiereAPI():
    return render_template("contact.html")

@app.get("/paris")
def api_paris():
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)

@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

@app.route("/rapport2")
def mongraphique2():
    return render_template("graphique2.html")

@app.route("/atelier")
def atelier():
    return render_template("atelier.html")

# API DATA POUR L'ATELIER (Marseille - vent + indicateur)
@app.get("/atelier_data")
def atelier_data():
    # Marseille
    lat, lon = 43.2965, 5.3698

    # On récupère du "current" (instantané)
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=windspeed_10m"
        "&timezone=Europe/Paris"
    )

    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    current = data.get("current", {})
    wind = float(current.get("windspeed_10m", 0.0))  # km/h (souvent)
    time = current.get("time")

    # Indicateur perso : confort du vent (0–100)
    comfort = 100 - 5 * wind
    comfort = max(0, min(100, comfort))

    return jsonify({
        "city": "Marseille",
        "time": time,
        "wind_kmh": wind,
        "comfort_index": comfort
    })

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
