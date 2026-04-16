import requests
import time
from typing import List
from models.schemas import Apartment
from config import Config

def filter_by_commute(apartments: List[Apartment], dest_lat: float, dest_lng: float) -> List[Apartment]:
    """Filters a list of apartments based on driving commute time using the Distance Matrix API."""
    if not apartments:
        return []

    print(f"\nCalculating commute times for {len(apartments)} locations...")
    
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    destination = f"{dest_lat},{dest_lng}"
    
    filtered_apartments = []
    
    # Batch apartments into chunks of 25 to respect Google's API limits
    batch_size = 25
    
    for i in range(0, len(apartments), batch_size):
        batch = apartments[i:i + batch_size]
        
        # Format origins as a pipe-separated string: "lat1,lng1|lat2,lng2"
        origins = "|".join([f"{apt.lat},{apt.lng}" for apt in batch])
        
        params = {
            "origins": origins,
            "destinations": destination,
            "key": Config.GOOGLE_API_KEY,
            "units": "imperial",
            "departure_time": "now" # In a production app, set to a future Tuesday 8AM Unix Timestamp
        }
        
        # Add a half-second delay between batches so we don't hit rate limits
        if i > 0:
            time.sleep(0.5)
            
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Distance Matrix API Error on batch: {response.status_code}")
            continue

        data = response.json()
        
        # The API returns rows in the exact order we sent them in the string
        for j, row in enumerate(data.get("rows", [])):
            elements = row.get("elements", [])
            if not elements or elements[0].get("status") != "OK":
                continue
                
            # Extract duration in minutes (preferring duration_in_traffic if available)
            duration_data = elements[0].get("duration_in_traffic", elements[0].get("duration", {}))
            duration_seconds = duration_data.get("value", 0)
            commute_mins = duration_seconds // 60
            
            # Update the dataclass with the newly found time
            batch[j].commute_time_mins = commute_mins
            
            # Filter based on the threshold in your config.py
            if commute_mins <= Config.MAX_COMMUTE_MINS:
                filtered_apartments.append(batch[j])
                
        print(f"Processed commute batch {(i // batch_size) + 1}...")

    return filtered_apartments