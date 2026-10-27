
import csv
import matplotlib.pyplot as plt

CSV_FILE = "sensor_readings.csv"


def load_readings():
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        readings = list(reader)

    if not readings:
        print("No sensor readings found.")
        return []

    return readings


def analyze_readings(readings):
    temperatures = [
        float(row["Temperature_C"])
        for row in readings
        if row.get("Temperature_C")
    ]

    vibrations = [
        float(row["Vibration_mm_s"])
        for row in readings
        if row.get("Vibration_mm_s")
    ]

    # Handle old CSV files without a Status column.
    warning_count = sum(
        1
        for row in readings
        if "HIGH" in (row.get("Status") or "")
    )

    print("\nSMARTSENSE - SENSOR REPORT")
    print("=" * 35)
    print("Total readings:", len(readings))

    if temperatures:
        print(
            f"Average temperature: "
            f"{sum(temperatures) / len(temperatures):.2f} °C"
        )
        print(f"Maximum temperature: {max(temperatures):.2f} °C")

    if vibrations:
        print(
            f"Average vibration: "
            f"{sum(vibrations) / len(vibrations):.2f} mm/s"
        )
        print(f"Maximum vibration: {max(vibrations):.2f} mm/s")

    print("Recorded readings with warnings:", warning_count)
    print("Note: Older rows without Status are not counted as warnings.")

    return temperatures, vibrations


def plot_readings(temperatures, vibrations):
    if not temperatures and not vibrations:
        print("No numeric sensor data available to plot.")
        return

    if temperatures:
        plt.figure(figsize=(9, 4))
        plt.plot(
            range(1, len(temperatures) + 1),
            temperatures,
            marker="o",
            label="Temperature (°C)",
        )
        plt.axhline(
            y=70,
            linestyle="--",
            label="Demo temperature threshold",
        )
        plt.xlabel("Reading Number")
        plt.ylabel("Temperature (°C)")
        plt.title("SmartSense - Temperature History")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

    if vibrations:
        plt.figure(figsize=(9, 4))
        plt.plot(
            range(1, len(vibrations) + 1),
            vibrations,
            marker="o",
            label="Vibration (mm/s)",
        )
        plt.axhline(
            y=5,
            linestyle="--",
            label="Demo vibration threshold",
        )
        plt.xlabel("Reading Number")
        plt.ylabel("Vibration (mm/s)")
        plt.title("SmartSense - Vibration History")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

    plt.show()


def main():
    try:
        readings = load_readings()
    except FileNotFoundError:
        print(f"CSV file not found: {CSV_FILE}")
        print("Run main.py first to generate sensor readings.")
        return

    if not readings:
        return

    temperatures, vibrations = analyze_readings(readings)
    plot_readings(temperatures, vibrations)


if __name__ == "__main__":
    main()
