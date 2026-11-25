from datetime import date


def trip_length_days(start_date: date, end_date: date) -> int:
    """Calculate the inclusive trip length."""
    if end_date < start_date:
        raise ValueError("End date must be on or after start date.")

    return (end_date - start_date).days + 1
