import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
	SEARCH_RADIUS_METERS = 8000
	TARGET_PRICE = 1500
	PRICE_VARIANCE_PCT = 0.05
	MAX_COMMUTE_MINS = 25
	
	TARGET_DESTINATION_LAT = os.getenv("TARGET_LAT", "40.0992")
	TARGET_DESTINATION_LNG = os.getenv("TARGET_LNG", "-83.1141")