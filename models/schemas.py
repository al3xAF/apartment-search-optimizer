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
	commute_time_mins: Optional[int] = None
	studio_price: Optional[int] = None
	one_bed_price: Optional[int] = None
	two_bed_price: Optional[int] = None