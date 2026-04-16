import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
	
	# Origin Point dynamically loaded from .env
	SEARCH_CENTER_LAT = float(os.getenv("SEARCH_CENTER_LAT"))
	SEARCH_CENTER_LNG = float(os.getenv("SEARCH_CENTER_LNG"))
	
	SEARCH_RADIUS_METERS = 50000 
	
	TARGET_PRICE = 1500
	PRICE_VARIANCE_PCT = 0.05
	MAX_COMMUTE_MINS = 25
	
	# Target destination dynamically loaded from .env
	TARGET_DESTINATION_LAT = os.getenv("TARGET_LAT")
	TARGET_DESTINATION_LNG = os.getenv("TARGET_LNG")