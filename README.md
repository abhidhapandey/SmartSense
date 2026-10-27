# SmartSense 🏭

Hi! This is SmartSense, a project I'm building while learning Python and exploring industrial IoT.

The idea is to simulate machine sensor readings and check whether everything is working within some demo limits. It generates temperature, vibration, and electrical current readings, detects warnings, and saves the data so I can analyse it later.

I'm using this project to practise Python, data handling, visualisation, testing, and building an interactive dashboard.

## What it does

- Generates simulated temperature, vibration, and current readings.
- Shows a warning when temperature goes above 70°C.
- Shows a warning when vibration goes above 5 mm/s.
- Saves sensor readings in a CSV file.
- Analyses data and plots sensor trends.
- Displays readings and machine status in a Streamlit dashboard.
- Shows recent alerts and lets users filter, search, and download recorded data.
- Includes tests for the alert logic.

## Dashboard

The dashboard includes:

- **Overview:** latest readings, charts, and machine status.
- **Sensor Analytics:** sensor trends and summary statistics.
- **Alert Center:** a view of readings that cross the demo thresholds.
- **Data Explorer:** a searchable table with CSV export.

I'll add a screenshot here once the dashboard design is finalised.

## Tech stack

- Python
- Pandas
- Streamlit
- Plotly
- CSV
- pytest

## How to run it

Install the required libraries:

```bash
python -m pip install -r requirements.txt
```

Generate sensor readings:

```bash
python main.py
```

Launch the dashboard:

```bash
python -m streamlit run dashboard.py
```

Run the tests:

```bash
python -m pytest -v
```

## What I'm learning

Through SmartSense, I'm practising how to work with sensor-like data, write monitoring logic, analyse readings, build interactive charts, and test my code.

Next, I'd like to explore configurable alert thresholds and predictive maintenance using a suitable dataset.

**Note:** All sensor readings are simulated. The thresholds are only for demonstrating the code and are not certified industrial safety limits. This project is a work in progress, and I'll keep improving it as I learn.

Thanks for checking out SmartSense!
