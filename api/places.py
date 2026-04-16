import requests
import time
from typing import List
from models.schemas import Apartment
from config import Config

def fetch_nearby_apartments() -> List[Apartment]:
    """Sweeps a dense 5x5 grid across the city to return hundreds of results."""
    
    # Dynamically generate a 5x5 grid (25 search zones)
    # 0.075 degrees is roughly 5 miles of distance between each point
    step_sizes = [-0.15, -0.075, 0.0, 0.075, 0.15]
    grid_offsets = []
    
    for lat_offset in step_sizes:
        for lng_offset in step_sizes:
            grid_offsets.append((lat_offset, lng_offset))
    
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": Config.GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName.text,places.formattedAddress,places.location,places.websiteUri"
    }
    
    apartments = []
    seen_ids = set() # Tracks duplicates across overlapping circles
    
    print(f"Sweeping Columbus metro area across {len(grid_offsets)} grid sectors...")
    
    for i, (lat_offset, lng_offset) in enumerate(grid_offsets):
        search_lat = Config.SEARCH_CENTER_LAT + lat_offset
        search_lng = Config.SEARCH_CENTER_LNG + lng_offset
        
        payload = {
            "includedTypes": ["apartment_building", "apartment_complex"],
            "maxResultCount": 20, # Google's hard limit per individual request
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": search_lat, "longitude": search_lng},
                    "radius": 10000 # 10km radius ensures tight overlap between grid points
                }
            }
        }
        
        # Add a tiny delay so we don't trip Google's rate limit for free tiers
        time.sleep(0.2)
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"API Error on sector {i+1}: {response.status_code}")
            continue
            
        places_data = response.json().get("places", [])
        new_finds = 0
        
        for place in places_data:
            place_id = place.get("id", "")
            
            if place_id in seen_ids:
                continue
                
            seen_ids.add(place_id)
            new_finds += 1
            
            apt = Apartment(
                name=place.get("displayName", {}).get("text", "Unknown Name"),
                address=place.get("formattedAddress", "Unknown Address"),
                lat=place.get("location", {}).get("latitude", 0.0),
                lng=place.get("location", {}).get("longitude", 0.0),
                place_id=place_id,
                website=place.get("websiteUri")
            )
            apartments.append(apt)
            
        print(f"Sector {i+1}/25 complete: Found {new_finds} new apartments.")
            
    return apartments