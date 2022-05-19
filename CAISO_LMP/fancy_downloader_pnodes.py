#!python

# Reference: https://www.caiso.com/Documents/OASIS-InterfaceSpecification_v5_1_1Clean_Fall2017Release.pdf
# FAQ: https://www.caiso.com/Documents/OASISFrequentlyAskedQuestions.pdf

from datetime import date, timedelta
import io
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile


# The first date to retrieve.
start_date = date(2021, 5, 1)
# The last date to retrieve.
end_date = date(2022, 4, 30)

# Used to increment a date by one day.
one_day = timedelta(days = 1)

# Configuration for the request to OASIS.
request_config = {
    # System
    'version': 1,
    'resultformat': 6,      # Request CSV format.

    # Query
    'queryname': "PRC_LMP",
    'market_run_id': "DAM",
    'grp_type': "ALL",
    # PRC_LMP requests retrieve data one day at a time. The enddatetime
    # value is ignored, provided that the value provided is:
    #   1. a date in the expected format
    #   2. follows the 'startdatettime' value chronologically
    # As such, we simply set this once to the "day after the final
    # request date."
    'enddatetime': f"{(end_date + one_day).strftime('%Y%m%d')}T00:00-0000",
    # Left empty as it is dynamically adjusted in the request loop.
    'startdatetime': "",
}

# The base URL for the request to OASIS.
url_base = "http://oasis.caiso.com/oasisapi/SingleZip"

print("Beginning data retrieval...\n")

day = start_date
throttle_delay = 3  # in seconds...

# Iterate over the date range.
while day <= end_date:
    # Set the startdatetime parameter to the current date.
    request_config['startdatetime'] = f"{day.strftime('%Y%m%d')}T00:00-0000"

    # Build the specified parameters.
    params = urllib.parse.urlencode(request_config)

    # Create the request URL.
    data_url = f"{url_base}?{params}"

    print(f"Downloading data for date \"{day.strftime('%Y%m%d')}\"...")
    print(f"\tURL: {data_url}")

    try:
        # Download the file
        with urllib.request.urlopen(data_url) as dl_data:
            # Read data fromthe response object.
            data = dl_data.read()

            print(f"Download complete. Extracting...")

            with zipfile.ZipFile(io.BytesIO(data)) as zip_data:
                # Extract all the data.
                for info in zip_data.infolist():
                    if info.filename.endswith("LMP_v1.csv"):
                        zip_data.extract(info, "data_pnodes")
                        break

                print(f"Extraction complete.\n")
            
            # Sleep to avoid HTTP Request throttling.
            time.sleep(throttle_delay)

    except urllib.error.HTTPError as err:
        print(f"Failed to download with status {err.status}. Reason: {err.reason}")
        raise

    day += one_day

print("Done!")
