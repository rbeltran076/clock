import json
import csv
import os

def register_to_csv():
    # Check if the JSON file exists
    if not os.path.exists('clock/data/saves.json'):
        print("No 'saves.json' file found.")
        return

    # Load data from JSON file
    with open('clock/data/saves.json', 'r') as file:
        data = json.load(file)

    # Check if the CSV file exists, if not create it and write the header
    if not os.path.exists('clock/data/workHours.csv'):
        with open('clock/data/workHours.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Hourly Rate', 'Time', 'Pay'])

    # Write data to CSV file
    with open('clock/data/workHours.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for date, entries in data.items():
            for entry in entries:
                writer.writerow([date, entry['hourly_rate'], entry['time'], entry['pay']])
