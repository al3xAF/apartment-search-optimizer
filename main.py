from config import Config
from api.places import fetch_nearby_apartments

def main():
	print("Starting Apartment Tour Optimizer...")
	
	search_lat = float(Config.TARGET_DESTINATION_LAT)
	search_lng = float(Config.TARGET_DESTINATION_LNG)
	
	apartments = fetch_nearby_apartments(search_lat, search_lng)
	
	print(f"\nFound {len(apartments)} apartments!")
	print("-" * 40)
	
	for apt in apartments:
		website_display = apt.website if apt.website else "No website listed"
		print(f"{apt.name}")
		print(f"Location: {apt.address}")
		print(f"Link: {website_display}\n")

if __name__ == "__main__":
	main()