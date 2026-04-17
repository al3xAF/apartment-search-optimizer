Apartment Tour Optimizer
========================

Searches a metro area for apartment buildings and filters them by quality and commute constraints. Outputs viable apartments with address, commute time, rating details, and website link.


How It Works
------------
1. Places API sweep  — Runs a 9x9 grid of nearby-search requests (81 sectors, up to 20 results each) and deduplicates by place id.
2. Rating filter     — Drops listings with rating below MIN_RATING when rating data exists, and also requires at least MIN_REVIEW_COUNT reviews for rated properties.
3. Website filter    — Drops listings that do not have a website value.
4. Commute filter    — Sends remaining locations to the Distance Matrix API in batches of 25 and drops any apartment with a driving commute longer than MAX_COMMUTE_MINS.
5. Results printout  — Prints name, rating, address, commute time, and website for each apartment that passed all filters.


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
       - MAX_COMMUTE_MINS   — Maximum acceptable commute in minutes (default: 30)
       - MIN_RATING         — Minimum rating to keep a rated listing (default: 4.0)
       - MIN_REVIEW_COUNT   — Minimum number of reviews for rated listings (default: 10)
       - TARGET_PRICE       — Target monthly rent (default: 1350)
       - PRICE_VARIANCE_PCT — Allowed variance around target price (default: 0.05)
       - SEARCH_RADIUS_METERS — Radius per grid sector (default: 16000)


Running
-------
    python main.py


Required Google APIs
--------------------
Enable both of these in your Google Cloud project:
  - Places API (New)
  - Distance Matrix API

Both require a billing-enabled project. The grid sweep makes 81 Places API calls;
the commute filter makes one Distance Matrix call per 25 apartments after the rating and website filters.

