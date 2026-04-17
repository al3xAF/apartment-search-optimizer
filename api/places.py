import requests
import time
from typing import List
from models.schemas import Apartment
from config import Config

def fetch_nearby_apartments() -> List[Apartment]:
    """Sweeps a dense 9x9 grid across the city to return hundreds of results."""
    
    # Dynamically generate a 9x9 grid (81 search zones)
    # 0.15 degrees is roughly 10 miles of distance between each point
    step_sizes = [-0.60, -0.45, -0.30, -0.15, 0.0, 0.15, 0.30, 0.45, 0.60]
    grid_offsets = []
    
    for lat_offset in step_sizes:
        for lng_offset in step_sizes:
            grid_offsets.append((lat_offset, lng_offset))
    
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
		"Content-Type": "application/json",
		"X-Goog-Api-Key": Config.GOOGLE_API_KEY,
		"X-Goog-FieldMask": "places.id,places.displayName.text,places.formattedAddress,places.location,places.websiteUri,places.rating,places.userRatingCount"
	}
    
    apartments = []
    seen_ids = set() # Tracks duplicates across overlapping circles
    
    print(f"Sweeping metro area across {len(grid_offsets)} grid sectors...")
    
    for i, (lat_offset, lng_offset) in enumerate(grid_offsets):
        search_lat = Config.SEARCH_CENTER_LAT + lat_offset
        search_lng = Config.SEARCH_CENTER_LNG + lng_offset
        
        payload = {
            "includedTypes": ["apartment_building", "apartment_complex"],
            "maxResultCount": 20, # Google's hard limit per individual request
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": search_lat, "longitude": search_lng},
                    "radius": Config.SEARCH_RADIUS_METERS
                }
            }
        }
        
        # Add a tiny delay so we don't trip Google's rate limit for free tiers
        time.sleep(0.2)
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
        except requests.RequestException as exc:
            print(f"Places API request failed on sector {i+1}: {exc}")
            continue
        
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
                website=place.get("websiteUri"),
                rating=place.get("rating"),
                user_rating_count=place.get("userRatingCount")
            )
            apartments.append(apt)
            
        print(f"Sector {i+1}/{len(grid_offsets)} complete: Found {new_finds} new apartments.")
            
    return apartments