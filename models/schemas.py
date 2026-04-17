from dataclasses import dataclass
from typing import Optional

@dataclass
class Apartment:
	name: str
	address: str
	lat: float
	lng: float
	place_id: str
	website: Optional[str] = None
	rating: Optional[float] = None
	user_rating_count: Optional[int] = None
	commute_time_mins: Optional[int] = None
	studio_price: Optional[int] = None
	one_bed_price: Optional[int] = None
	two_bed_price: Optional[int] = None