
from main import check_status, TEMP_LIMIT, VIBRATION_LIMIT


def test_normal_readings():
    reading = {
        "temperature": 50,
        "vibration": 2,
        "current": 5,
        "timestamp": "2026-10-27 10:00:00",
    }

    status = check_status(reading)

    assert status == ["WITHIN DEMO LIMITS"]


def test_high_temperature():
    reading = {
        "temperature": TEMP_LIMIT + 5,
        "vibration": 2,
        "current": 5,
        "timestamp": "2026-10-27 10:00:00",
    }

    status = check_status(reading)

    assert "HIGH TEMPERATURE" in status
    assert "HIGH VIBRATION" not in status


def test_high_vibration():
    reading = {
        "temperature": 50,
        "vibration": VIBRATION_LIMIT + 1,
        "current": 5,
        "timestamp": "2026-10-27 10:00:00",
    }

    status = check_status(reading)

    assert "HIGH VIBRATION" in status
    assert "HIGH TEMPERATURE" not in status


def test_both_warnings():
    reading = {
        "temperature": TEMP_LIMIT + 5,
        "vibration": VIBRATION_LIMIT + 1,
        "current": 5,
        "timestamp": "2026-10-27 10:00:00",
    }

    status = check_status(reading)

    assert "HIGH TEMPERATURE" in status
    assert "HIGH VIBRATION" in status
