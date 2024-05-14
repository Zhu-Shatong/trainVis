import json
import csv

# Function to convert JSON data to CSV format


def json_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Write CSV header
        writer.writerow(
            ["origin_station", "destination_station", "code"])

        # Iterate through each entry in the JSON data
        for entry in data:
            key = entry.get("key", [])
            code = entry.get("code", "")
            # Iterate through pairs of stations in 'key' list
            for i in range(len(key) - 1):
                origin_station = key[i]
                destination_station = key[i+1]
                # Skip empty strings as destinations
                if origin_station != "" and destination_station != "":
                    writer.writerow(
                        [origin_station, destination_station, code])


# Usage example
input_json_file = "static/data/TrainInfo.json"
output_csv_file = "real_all_train_info.csv"
json_to_csv(input_json_file, output_csv_file)
