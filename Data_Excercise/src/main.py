import json
import pandas as pd
import requests

if __name__ == "__main__":
    print("Starting...")
    components_df = pd.read_csv("https://github.com/qmetric/data-team-coding-exercise/blob/main/data/components.csv"
                                "?raw=true")

    components = json.loads(components_df.to_json(orient="records"))

    response = requests.get("https://github.com/qmetric/data-team-coding-exercise/blob/main/data/orders.json.txt"
                            "?raw=true")

    response_format = response.text.replace('}\n{', '},\n{')

    orders = json.loads("[%s]" % response_format)

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

    print("Finished!")
