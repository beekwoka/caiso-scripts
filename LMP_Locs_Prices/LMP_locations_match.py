# #!python

# Matching the LMP nodes from OASIS with geospatial data from a CAISO map
# (2022.05)

# Match the node name from the LMP_Node_Locations csv file to rows (node names/IDs/avg LMP)
#   in the CAISO_LMP_pnodes_output csv file.
# For any matches, write all the information from the LMP_Node_Locations file and the 
#   avg LMP from the CAISO_LMP_pnodes_output file. 


import csv

all_data_dict = {} # where our collected lmp data goes

with open('../LMP Locations/LMP_Node_locations.csv', 'r') as node_locations: #need to add directory name
    locations_reader = csv.DictReader(node_locations)
    
    for row_dict in locations_reader:
        node_name = row_dict['NODE_ID']
        all_data_dict[node_name] = row_dict

with open('../CAISO_LMP/CAISO_LMP_pnodes_output.csv', 'r') as node_lmps:
    lmp_reader = csv.DictReader(node_lmps)

    for row_dict in lmp_reader:
        if row_dict['NODE_ID'] in all_data_dict:
            # The "|=" operator takes the key-value pairs from the
            #   dictionary on the right-hand-side and adds them to
            #   the dictionary on the left-hand-side. If the
            #   dictionary on the left-hand-side already has an
            #   entry for a key-value-pair, it will be overwritten.
            all_data_dict[row_dict['NODE_ID']] |= row_dict

            # The following two lines simply add a specific
            #   key-value pair to the node_dict dictionary.
            # node_dict = all_data_dict['NODE_ID']
            # node_dict['AVG_LMP'] = row_dict['AVG_LMP']
        else:
            # Add the row_dict to the all_data_dict using the
            #   row_dict's NODE_ID value as the key.
            all_data_dict[row_dict['NODE_ID']] = row_dict



with open('avg_LMP_node_locations.csv', 'w') as LMP_locations_csv:
    fieldnames = ["NODE_ID", "AVG_LMP", "Type", "Area", "CoordX", "CoordY"]
    writer = csv.DictWriter(LMP_locations_csv, fieldnames=fieldnames)

    writer.writeheader()

    for value in all_data_dict.values():
        writer.writerow(value)
