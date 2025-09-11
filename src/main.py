from fastapi import FastAPI

from ParkingSpaces import ParkingSpaces

app = FastAPI()

@app.get("/")
def get_parking_data():
    ps = ParkingSpaces()
    available_parking = ps.get_available_parking()
    return available_parking