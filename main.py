
import csv
import os
import random
from datetime import datetime

# Demonstration thresholds, not real equipment safety limits.
TEMP_LIMIT = 70
VIBRATION_LIMIT = 5

CSV_FILE = "sensor_readings.csv"


def generate_reading():
    """Generate one set of simulated sensor measurements."""
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": round(random.uniform(35, 85), 2),
        "vibration": round(random.uniform(0.1, 8.0), 2),
        "current": round(random.uniform(2, 15), 2),
    }


def check_status(reading):
    """Return warnings for a set of sensor readings."""
    warnings = []

    if reading["temperature"] > TEMP_LIMIT:
        warnings.append("HIGH TEMPERATURE")

    if reading["vibration"] > VIBRATION_LIMIT:
        warnings.append("HIGH VIBRATION")

    if not warnings:
        warnings.append("WITHIN DEMO LIMITS")

    return warnings


def save_reading(reading, status):
    """Append a reading and its status to the CSV history."""
    file_exists = (
        os.path.isfile(CSV_FILE)
        and os.path.getsize(CSV_FILE) > 0
    )

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Timestamp",
                "Temperature_C",
                "Vibration_mm_s",
                "Current_A",
                "Status",
            ])

        writer.writerow([
            reading["timestamp"],
            reading["temperature"],
            reading["vibration"],
            reading["current"],
            " | ".join(status),
        ])


def main():
    print("SMARTSENSE - INDUSTRIAL MONITORING")
    print("=" * 40)

    number_of_readings = 10

    for number in range(1, number_of_readings + 1):
        reading = generate_reading()
        status = check_status(reading)

        print(f"\nReading {number}")
        print("-" * 30)
        print("Time:", reading["timestamp"])
        print("Temperature:", reading["temperature"], "°C")
        print("Vibration:", reading["vibration"], "mm/s")
        print("Current:", reading["current"], "A")
        print("Status:", ", ".join(status))

        save_reading(reading, status)

    print(f"\nCompleted {number_of_readings} readings.")
    print("Sensor history saved to:", CSV_FILE)


if __name__ == "__main__":
    main()
