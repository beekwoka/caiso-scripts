#!python

# Turning downloaded LMP data into a useful format for GIS capstone analysis 
# (2022.05)

# For each CSV file in the data directory:
# Use a function to read the first line. These are the field names. 
#
# Iterate through each row. 
# For rows where the value in the field LMP_TYPE == LMP, grab this data and stuff 
#   it in a new dictionary:
#       NODE_ID
#       NODE
#       MW (append to an array)
#
# Iterate through the next CSV file and do the same. 
#
# Post CSV file iteration, average the values of each array.
# Return a csv with NODE_ID, NODE, and the Average MW value for each Node
#
# The final output: A csv file with the average LMP price (over the course 
#   of a year) for each APnode.


import os
import csv
import statistics


# The 'data_accumulator' is a place to accumulate data from all csv files
# It's a dictionary that has keys that match the NODE_ID field in the csv 
#   files to facilitate fast lookup. 
# Each entry in this dictionary is itself a dictionary containing
#   NODE_ID, NODE, and an array of MW values for the corresponding Node
data_accumulator = {}

data_dir = "data_pnodes"

# ERIC EDIT: Sort list of files prior to iteration...
# Get a list of all files in the data directory, sorted alphabetically.
filenames = os.listdir(data_dir)
filenames.sort()

# Enumerate all data files
# Assume directory only contains csv files we want
for filename in filenames:

    # ERIC EDIT: Ignore non-csv files.
    # Ignore non-csv files
    if not filename.endswith(".csv"):
        continue

    # open the current file
    with open(f"{data_dir}/{filename}", 'r') as current_csv:
        print(f"Processing file {filename}...")
        #open the file as a csv
        reader = csv.DictReader(current_csv)
        # Iterate over all rows
        for row in reader:
            # Ignore APNodes
            if row['GRP_TYPE'] == "ALL_APNODES":
                continue

            # Checks for column similarity...
            # if row["NODE"] != row["NODE_ID"]:
            #     print("NODE and NODE_ID don't match!")
            #     print(row)
            # if row["NODE_ID"] != row["NODE_ID_XML"]:
            #     print("NODE_ID and NODE_ID_XML don't match!")
            #     print(row)
            # if row["NODE"] != row["PNODE_RESMRID"]:
            #     print("NODE_ID and PNODE_RESMRID don't match!")
            #     print(row)

            # Now for the rows we care about
            current_node_id = row['NODE_ID']

            # See if the node ID exists in the data_accumulator dictionary
            # If it does, add the MW value to the MW array
            try:
                node_data = data_accumulator[current_node_id]
                # ERIC EDIT: add float() to convert from str to float
                node_data['MW'].append(float(row['MW']))

            # 
            except KeyError:
                data_accumulator[current_node_id] = {
                    'NODE_ID': row['NODE_ID'],
                    # ERIC EDIT: add float() to convert from str to float
                    'MW': [float(row['MW'])],
                }

print("\nWriting Output CSV...")

with open("CAISO_LMP_pnodes_output.csv", 'w') as output_csv:
    # ERIC EDIT: Remove "MW" field...
    # fieldnames = ["NODE_ID", "NODE", "MW", "AVG_LMP"]
    fieldnames = ["NODE_ID", "AVG_LMP"]
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

    writer.writeheader()

    # Now to average the LMP prices (e.g. the numbers in the MW array)
    # Start by exploding the data_accumulator dictionary, separating the keys and associated values
    #   (This provides access to the keys and value pairs.)
    # In this case, the value is another dictionary (that contains the accumulated data for a given node)
    for key, value in data_accumulator.items():
        # Averaging the MW array and sticking it in a new field in the same dictionary
        value["AVG_LMP"] = statistics.fmean(value["MW"])

        # ERIC EDIT: Remove "MW" field...
        # Remove the original "MW" field.
        del value["MW"]

        # Write each dictionary to a row in the output_csv
        writer.writerow(value)

print("Process complete!")

# The end?
     



# Early explanations of code structure

# my_transformed_data = {
#     'BethanyNode-APND': {
#         'NODE_ID': "BethanyNode",
#         'NODE': "Bethany",
#         'MW': [4, 23],
#     },
# }

# row = {
#     'NODE_ID': "BethanyNode-APND",
#     'NODE': "Bethany-APND",
#     'MW': 42,
#     # ...
# }

# # BethanyNode
# current_node_id = row['NODE_ID']

# try:
#     node_data = my_transformed_data[current_node_id]
#     node_data['MW'].append(row['MW'])

# except KeyError:
#     my_transformed_data[current_node_id] = {
#         'NODE_ID': row['NODE_ID'],
#         'NODE': row['NODE'].removesuffix("-APND"),
#         'MW': [row['MW']],
#     }




