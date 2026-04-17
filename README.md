Apartment Tour Optimizer
========================

Searches a metro area for apartment buildings and filters them by driving commute time to a target destination. Outputs a ranked list of viable apartments with addresses, commute times, and website links.


How It Works
------------
1. Places API sweep  — Runs a 9x9 grid of nearby-search requests spanning ~40 miles in each direction from the origin (81 sectors, up to 20 results each) to collect apartment buildings/complexes.
2. Commute filter    — Sends the collected locations to the Distance Matrix API in batches of 25 and drops any apartment with a driving commute longer than MAX_COMMUTE_MINS.
3. Results printout  — Prints the name, address, commute time, and website for every apartment that passed the filter.


Setup
-----
1. Create and activate a virtual environment:

       python -m venv venv
       source venv/bin/activate

2. Install dependencies:

       pip install -r requirements.txt

3. Create a .env file in the project root with the following keys:

       GOOGLE_API_KEY=your_google_api_key

       # Center of the search grid (the middle of the metro area you want to scan)
       SEARCH_CENTER_LAT=your_center_latitude
       SEARCH_CENTER_LNG=your_center_longitude

       # Your workplace or commute destination
       TARGET_LAT=your_destination_latitude
       TARGET_LNG=your_destination_longitude

4. (Optional) Adjust thresholds in config.py:
   - MAX_COMMUTE_MINS  — Maximum acceptable commute in minutes (default: 25)
   - TARGET_PRICE      — Target monthly rent (default: 1500)
   - SEARCH_RADIUS_METERS — Radius per grid sector (default: 50000)


Running
-------
    python main.py


Required Google APIs
--------------------
Enable both of these in your Google Cloud project:
  - Places API (New)
  - Distance Matrix API

Both require a billing-enabled project. The grid sweep makes 81 Places API calls;
the commute filter makes one Distance Matrix call per 25 apartments found.

