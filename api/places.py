import requests
from typing import List
from models.schemas import Apartment
from config import Config

def fetch_nearby_apartments(lat: float, lng: float) -> List[Apartment]:
	url = "https://places.googleapis.com/v1/places:searchNearby"
	
	headers = {
		"Content-Type": "application/json",
		"X-Goog-Api-Key": Config.GOOGLE_API_KEY,
		"X-Goog-FieldMask": "places.id,places.displayName.text,places.formattedAddress,places.location,places.websiteUri"
	}
	
	payload = {
		"includedTypes": ["apartment_building", "apartment_complex"],
		"maxResultCount": 20,
		"locationRestriction": {
			"circle": {
				"center": {"latitude": lat, "longitude": lng},
				"radius": Config.SEARCH_RADIUS_METERS
			}
		}
	}
	
	print("Fetching apartments from Google Places...")
	response = requests.post(url, headers=headers, json=payload)
	
	if response.status_code != 200:
		print(f"API Error: {response.status_code} - {response.text}")
		return []
		
	places_data = response.json().get("places", [])
	apartments = []
	
	for place in places_data:
		apt = Apartment(
			name=place.get("displayName", {}).get("text", "Unknown Name"),
			address=place.get("formattedAddress", "Unknown Address"),
			lat=place.get("location", {}).get("latitude", 0.0),
			lng=place.get("location", {}).get("longitude", 0.0),
			place_id=place.get("id", ""),
			website=place.get("websiteUri")
		)
		apartments.append(apt)
		
	return apartments