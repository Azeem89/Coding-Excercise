import json
import os
import pandas as pd
import requests
import validators


def main():
    csv_location = "https://github.com/qmetric/data-team-coding-exercise/blob/main/data/components.csv?raw=true"
    json_location = "https://github.com/qmetric/data-team-coding-exercise/blob/main/data/orders.json.txt?raw=true"

    #csv_location = "../data/components.csv"
    #json_location = "../data/orders.json.txt"

    csv_valid_url = validators.url(csv_location)
    csv_valid_file  = os.path.isfile(csv_location)

    json_valid_url = validators.url(json_location)
    json_valid_file = os.path.isfile(json_location)

    components = []

    if csv_valid_url or csv_valid_file:
        components_df = pd.read_csv(csv_location)

        components = json.loads(components_df.to_json(orient="records"))

    data = ""

    if json_valid_url:
        data = requests.get(json_location).text
    elif json_valid_file:
        data = open(json_location).read()

    data_format = data.replace('}\n{', '},\n{')

    orders = json.loads("[%s]" % data_format)

    totals = {}

    for order in orders:
        if order['timestamp'].startswith("2021-06-03"):
            for key, value in order['units'].items():
                totals[key] = (0 if key not in totals.keys() else totals[key]) + value

    for component in components:
        if component['componentId'] in totals.keys():
            print(component['colour'] + ": " + str(totals[component['componentId']]))
        else:
            print(component['colour'] + ": 0")


if __name__ == "__main__":
    print("Starting...")

    main()

    print("Finished!")
