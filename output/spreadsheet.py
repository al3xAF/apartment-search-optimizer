from pathlib import Path
from typing import List

from openpyxl import Workbook
from openpyxl.styles import Font

from models.schemas import Apartment


def export_apartments_to_spreadsheet(apartments: List[Apartment], output_path: str) -> str:
    """Write apartment results to a simple Excel workbook and return the file path."""
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Apartments"

    headers = [
        "Name",
        "Address",
        "Commute (mins)",
        "Rating",
        "Review Count",
        "Website",
        "Latitude",
        "Longitude",
        "Studio Price",
        "1 Bed Price",
        "2 Bed Price",
        "Place ID",
    ]

    worksheet.append(headers)
    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    for apartment in apartments:
        worksheet.append(
            [
                apartment.name,
                apartment.address,
                apartment.commute_time_mins,
                apartment.rating,
                apartment.user_rating_count,
                apartment.website,
                apartment.lat,
                apartment.lng,
                apartment.studio_price,
                apartment.one_bed_price,
                apartment.two_bed_price,
                apartment.place_id,
            ]
        )

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions

    column_widths = {
        "A": 28,
        "B": 48,
        "C": 16,
        "D": 10,
        "E": 14,
        "F": 42,
        "G": 12,
        "H": 12,
        "I": 14,
        "J": 14,
        "K": 14,
        "L": 32,
    }
    for column, width in column_widths.items():
        worksheet.column_dimensions[column].width = width

    export_file = Path(output_path)
    export_file.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(export_file)

    return str(export_file)