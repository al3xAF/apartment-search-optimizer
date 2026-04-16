from config import Config
from api.places import fetch_nearby_apartments
from api.commute import filter_by_commute

def main():
    print("Starting Apartment Tour Optimizer...\n")
    
    # We still need these for the commute filter later
    search_lat = float(Config.TARGET_DESTINATION_LAT)
    search_lng = float(Config.TARGET_DESTINATION_LNG)
    
    # Step 1: Fetch Locations using the 5x5 grid sweep (No arguments needed!)
    apartments = fetch_nearby_apartments()
    
    print(f"\nFound {len(apartments)} unique apartments across the metro area!")
    print("-" * 40)
    
    # Step 2: Filter by Commute (Pass the target destination in here)
    viable_apartments = filter_by_commute(apartments, search_lat, search_lng)
    
    print(f"\nFound {len(viable_apartments)} apartments within a {Config.MAX_COMMUTE_MINS}-minute drive!")
    print("-" * 40)
    
    for apt in viable_apartments:
        website_display = apt.website if apt.website else "No website listed"
        print(f"{apt.name}")
        print(f"Location: {apt.address}")
        print(f"Commute: {apt.commute_time_mins} mins")
        print(f"Link: {website_display}\n")

if __name__ == "__main__":
    main()