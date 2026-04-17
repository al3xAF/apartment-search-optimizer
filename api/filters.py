from typing import List
from models.schemas import Apartment
from config import Config

def apply_rating_filter(apartments: List[Apartment]) -> List[Apartment]:
	"""Filters out apartments with Google reviews below the configured threshold."""
	if not apartments:
		return []

	initial_count = len(apartments)
	highly_rated = []
	
	for apt in apartments:
		if apt.rating is not None and apt.user_rating_count is not None:
			# Check against your minimum thresholds
			if apt.rating >= Config.MIN_RATING and apt.user_rating_count >= Config.MIN_REVIEW_COUNT:
				highly_rated.append(apt)
		else:
			# Keep brand new properties that don't have reviews yet
			highly_rated.append(apt)
			
	dropped = initial_count - len(highly_rated)
	print(f"Dropped {dropped} locations for having a rating below {Config.MIN_RATING} stars.")
	
	return highly_rated


def apply_website_filter(apartments: List[Apartment]) -> List[Apartment]:
	"""Filters out apartments that do not have a website listed."""
	if not apartments:
		return []

	initial_count = len(apartments)
	with_website = []

	for apt in apartments:
		if apt.website and apt.website.strip():
			with_website.append(apt)

	dropped = initial_count - len(with_website)
	print(f"Dropped {dropped} locations for not having a website listed.")

	return with_website