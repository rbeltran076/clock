import json
import csv
import os

# From saves.json to clockdata.csv
def register_from_json():
    # Check if the JSON file exists
    if not os.path.exists('data/saves.json'):
        print("No 'saves.json' file found.")
        return

    # Load data from JSON file
    with open('data/saves.json', 'r') as file:
        data = json.load(file)

    # Check if the CSV file exists, if not create it and write the header
    if not os.path.exists('data/clockdata.csv'):
        with open('data/clockdata.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Title', 'Hourly Rate', 'Time', 'Pay'])

    # Write data to CSV file
    with open('data/clockdata.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for date, titles in data.items():
            for title, entries in titles.items():
                for entry in entries:
                    writer.writerow([date, title, entry['hourly_rate'], entry['time'], entry['pay']])

# Call the function
register_from_json()