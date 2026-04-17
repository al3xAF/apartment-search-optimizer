from config import Config
from api.places import fetch_nearby_apartments
from api.filters import apply_rating_filter, apply_website_filter
from api.commute import filter_by_commute

def main():
	print("Starting Apartment Tour Optimizer...\n")
	
	search_lat = float(Config.TARGET_DESTINATION_LAT)
	search_lng = float(Config.TARGET_DESTINATION_LNG)
	
	# Step 1: Grid Sweep
	apartments = fetch_nearby_apartments()
	print(f"\nFound {len(apartments)} unique apartments across the metro area!")
	print("-" * 40)
	
	# Step 2: Rating Filter (Runs before the commute check!)
	good_apartments = apply_rating_filter(apartments)
	
	# Step 3: Website Filter
	good_apartments = apply_website_filter(good_apartments)
	print("-" * 40)
	
	# Step 4: Commute Filter
	viable_apartments = filter_by_commute(good_apartments, search_lat, search_lng)
	print(f"\nFound {len(viable_apartments)} apartments within a {Config.MAX_COMMUTE_MINS}-minute drive!")
	print("-" * 40)
	
	# Output
	for apt in viable_apartments:
		rating_display = f"{apt.rating}★ ({apt.user_rating_count} reviews)" if apt.rating is not None else "No reviews"
		
		print(f"{apt.name} | {rating_display}")
		print(f"Location: {apt.address}")
		print(f"Commute: {apt.commute_time_mins} mins")
		print(f"Link: {apt.website}\n")

if __name__ == "__main__":
	main()
