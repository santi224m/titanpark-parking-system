from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from ParkingSpaces import ParkingSpaces

app = FastAPI()

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')

@app.get("/parking_data/all")
def get_all_parking_data():
    """Get live parking data for all parking structures"""
    ps = ParkingSpaces()
    available_parking = ps.get_available_parking()
    return available_parking

@app.get("/parking_data/{struct_name}")
def get_parking_structure_data(struct_name: str):
    """Get live parking data for a specific parking structure"""
    ps = ParkingSpaces()
    available_parking = ps.get_available_parking()
    if struct_name not in available_parking:
        return {"Error": f"Structure '{struct_name}' not in parking data"}
    return available_parking[struct_name]
    