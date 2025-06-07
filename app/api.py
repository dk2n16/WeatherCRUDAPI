from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from .data_types import WeatherReport
from .data_access import (
    db_add_weather_report,
    db_get_weather_report,
    db_delete_weather_report,
    db_update_weather_report,
    db_get_all_weather_reports,
)
from .errors import CityNotFoundError


api_bp = Blueprint("api", __name__)


@api_bp.route("/weather/<city>", methods=["POST"])
def create_weather_report(city: str):
    timestamp = datetime.now(timezone.utc)
    data = request.get_json()
    data["timestamp"] = timestamp.isoformat()
    try:
        report = WeatherReport(**data)
    except ValidationError as e:
        return jsonify({"error": "Invalid data", "details": str(e)}), 400
    db_add_weather_report(city, report)
    return jsonify({"message": "Weather report created", "city": city, "report": report.model_dump(mode="json")}), 201

@api_bp.route("/weather/<city>", methods=["GET"])
def get_weather_report(city: str):
    try:
        report = db_get_weather_report(city)
    except CityNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify({"city": city, "report": report.model_dump(mode="json")}), 200


@api_bp.route("/weather", methods=["GET"])
def get_all_weather_reports():
    reports = db_get_all_weather_reports()
    summary = [
        {
            "city": report.city,
            "condition": report.condition.value,
            "temperature": report.temperature,
            "timestamp": report.timestamp.isoformat(),
        }
        for report in reports
    ]
    return jsonify({"weather_reports": summary}), 200


@api_bp.route("/weather/<city>", methods=["DELETE"])
def delete_weather_report(city: str):
    try:
        db_delete_weather_report(city)
    except CityNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify({"message": "Weather report deleted", "city": city}), 200


@api_bp.route("/weather/<city>", methods=["PUT"])
def update_weather_report(city: str):
    data = request.get_json()
    data["city"] = city
    data["timestamp"] = datetime.now(timezone.utc).isoformat()
    try:
        report = WeatherReport(**data)
    except ValidationError as e:
        return jsonify({"error": "Invalid data", "details": str(e)}), 400
    try:
        updated_report = db_update_weather_report(city, report)
    except CityNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify({"message": "Weather report updated", "city": city, "report": updated_report.model_dump(mode="json")}), 200
