#!python

# Reference: https://www.caiso.com/Documents/OASIS-InterfaceSpecification_v5_1_1Clean_Fall2017Release.pdf
# FAQ: https://www.caiso.com/Documents/OASISFrequentlyAskedQuestions.pdf

import io
import pandas as pd
import urllib.request
import zipfile


# The first date to retrieve.
start_date = "20210501"
# The last date to retrieve.
end_date = "20220430"

print("Beginning data retrieval...\n")

# Iterate over the date range.
for date in pd.date_range(start_date, end_date):
    # Transform the date into YYYYMMDD format.
    date_str = date.strftime("%Y%m%d")

    # Create URL.
    data_url = f"http://oasis.caiso.com/oasisapi/SingleZip?queryname=PRC_LMP&market_run_id=DAM&version=1&grp_type=ALL_APNODES&resultformat=6&startdatetime={date_str}T00:00-0000&enddatetime=23000101T00:00-0000"

    print(f"Downloading data for date \"{date_str}\"...")
    print(f"\tURL: {data_url}")

    # Download the file.
    with urllib.request.urlopen(data_url) as dl_data:
        # Read data fromthe response object.
        data = dl_data.read()

        print(f"Download complete. Extracting...")

        with zipfile.ZipFile(io.BytesIO(data)) as zip_data:
            # Extract all the data.
            zip_data.extractall("data")
            print(f"Extraction complete.\n")

print("Done!")
