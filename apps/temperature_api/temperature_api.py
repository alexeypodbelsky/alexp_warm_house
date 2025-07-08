from flask import Flask, request, jsonify
import random
import datetime

app = Flask(__name__)


def generateTemperature():
    return round(random.uniform(-20, 40), 1)


def getLocationBySensorId(sensor_id):
    if sensor_id == "1":
        return "Living Room"
    elif sensor_id == "2":
        return "Bedroom"
    elif sensor_id == "3":
        return "Kitchen"
    else:
        return "Unknown"


def getSensorIdByLocation(location):
    if location == "Living Room":
        return "1"
    elif location == "Bedroom":
        return "2"
    elif location == "Kitchen":
        return "3"
    else:
        return "0"


@app.route("/temperature")
def getTemperature():
    location = request.args.get("location", default="")
    sensor_id = location

    if getLocationBySensorId(sensor_id) != "Unknown":
        location = getLocationBySensorId(sensor_id)
    else:
        sensor_id = getSensorIdByLocation(location)

    temperature = generateTemperature()

    # Форматируем текущее время в RFC3339 (ISO8601)
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    response = {
        "location": location,
        "sensor_id": sensor_id,
        "value": temperature,
        "unit": "°C",
        "status": "active",
        "timestamp": timestamp,
        "sensor_type": "temperature",
        "description": "temperature sensor data",
    }

    return jsonify(response)


@app.route("/temperature/<sensor_id>")
def getTemperatureById(sensor_id):

    location = getLocationBySensorId(sensor_id)

    if location == "Unknown":
        return jsonify({"error": "Sensor ID not found"}), 404

    temperature = generateTemperature()
    # Форматируем текущее время в RFC3339 (ISO8601)
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    response = {
        "location": location,
        "sensor_id": sensor_id,
        "value": temperature,
        "unit": "°C",
        "status": "active",
        "timestamp": timestamp,
        "sensor_type": "temperature",
        "description": "temperature sensor data",
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)
