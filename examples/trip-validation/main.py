from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rules import trip_length_days

app = FastAPI()


class TripDates(BaseModel):
    start_date: date
    end_date: date


class TripDuration(BaseModel):
    days: int = Field(ge=1)


@app.post("/api/v1/trip-duration", response_model=TripDuration)
def validate_trip_dates(trip: TripDates) -> TripDuration:
    try:
        days = trip_length_days(trip.start_date, trip.end_date)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return TripDuration(days=days)
