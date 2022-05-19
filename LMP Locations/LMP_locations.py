# Grabbing the AP Node name and location from a JSON file

# Load the JSON file
# Point program to 3rd object in the "l" array
# Tell program to look in there for the "m" array
# --> everything we want is in there! So iterate over that array 
#   and grab the info we need. 
#       "c": [
#           46.390899999981457,
#           -116.98003473525635
#       ],
#       "n": "10TH_STW_1_1LNODE",
#       "p": "LOAD",
#       "a": ...

# asking for the values that correspond to particular keys
# in all the dictionaries in the "m" array
#
#

import json
import csv

with open("LMP_CAISO_PriceContourMap.json", "r") as json_file:

    all_json = json.load(json_file)

    lmp_nodes = all_json["l"][2]["m"]

    with open("LMP_Node_locations.csv", "w") as output_csv:
        fieldnames = ["NODE_ID", "Type", "Area", "CoordX", "CoordY"]

        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

        writer.writeheader()

        for node in lmp_nodes:
            writer.writerow({
                'NODE_ID': node['n'],
                'Type': node['p'],
                'Area': node['a'],
                'CoordX': node['c'][0],
                'CoordY': node['c'][1],
            })
