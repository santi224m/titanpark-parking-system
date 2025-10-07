from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from ParkingSpaces import ParkingSpaces
from DBHandler import DBHandler

app = FastAPI()

@app.get("/", include_in_schema=False)
async def docs_redirect():
    try:
        return RedirectResponse(url='/docs')
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error trying to redirect to API documentation page: {e}"
        )

@app.get("/parking_data/all")
def get_all_parking_data():
    """Get live parking data for all parking structures"""
    try:
        ps = ParkingSpaces()
        available_parking = ps.get_available_parking()
        return available_parking
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error trying to fetch parking data: {e}"
        )

@app.get("/parking_data/{struct_name}")
def get_parking_structure_data(struct_name: str):
    """Get live parking data for a specific parking structure"""
    try:
        ps = ParkingSpaces()
        available_parking = ps.get_available_parking()
        if struct_name not in available_parking:
            raise HTTPException(status_code=422, detail=f"Structure '{struct_name}' not in parking data")
        return available_parking[struct_name]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while fetching {struct_name} data: {e}"
        )

@app.post("/add_vehicle")
def add_vehicle(user_id: str, make: str, model: str, year: int, color: str, license_plate: str):
    """Add a user's vehicle to the database"""
    try:
        with DBHandler() as curr:
            curr.execute(
                """
                INSERT INTO vehicle (
                    user_id,
                    make,
                    model,
                    year,
                    color,
                    license_plate
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """, (
                    user_id,
                    make,
                    model,
                    year,
                    color,
                    license_plate
                )
            )
            res = curr.fetchone()
            if res is not None and len(res) > 0:
                vehicle_uuid = res[0]
            else:
                vehicle_uuid = None
        return {"vehicle_uuid": vehicle_uuid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting vehicle to database: {e}")

@app.get("/get_user_vehicles")
def get_user_vehicles(user_id: str):
    """Get a list of vehicles belonging to a user"""
    try:
        with DBHandler() as curr:
            curr.execute(
                """
                SELECT
                    id AS vehicle_id,
                    make,
                    model,
                    year,
                    color,
                    license_plate
                FROM vehicle
                WHERE user_id = %s;
                """, (user_id, )
            )
            res = curr.fetchall()
            vehicles_dict = {}
            for vehicle in res:
                vehicle_id, make, model, year, color, license_plate = vehicle
                vehicles_dict[vehicle_id] = {
                    'make': make,
                    'model': model,
                    'year': year,
                    'color': color,
                    'license_plate': license_plate
                }
            return vehicles_dict
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error trying to get user {user_id}'s vehicles: {e}"
        )

@app.post("/add_listing")
def add_listing(user_id: str, price: int, structure_id: int, floor: int, vehicle_id: str, comment: str):
    """Add a listing to the database"""
    try:
        # Insert listing to database
        with DBHandler() as curr:
            curr.execute(
                """
                INSERT INTO listing (
                    user_id,
                    price,
                    structure_id,
                    floor,
                    vehicle_id,
                    comment
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """, (
                    user_id,
                    price,
                    structure_id,
                    floor,
                    vehicle_id,
                    comment
                )
            )
            res = curr.fetchone()
            if res is not None and len(res) > 0:
                listing_uuid = res[0]
            else:
                listing_uuid = None
        return {"listing_uuid": listing_uuid}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inserting listing to database: {e}"
        )

@app.get("/get_listings")
def get_listings():
    """Get a list of all currently available listings"""
    try:
        with DBHandler() as curr:
            curr.execute(
                """
                SELECT
                    L.id AS listing_id,
                    L.user_id,
                    L.post_date,
                    L.price,
                    PS.name AS structure_name,
                    L.floor,
                    V.make,
                    V.model,
                    V.year,
                    V.color,
                    V.license_plate,
                    L.comment
                FROM listing AS L
                INNER JOIN parking_structure AS PS
                    ON PS.id = L.structure_id
                INNER JOIN vehicle AS V
                    ON v.id = L.vehicle_id;
                """
            )
            res = curr.fetchall()
            listings_dict = {}
            for listing in res:
                listing_id, user_id, post_date, price, structure_name, floor, make, model, year, color, license_plate, comment = listing
                listings_dict[listing_id] = {
                    'user_id': user_id,
                    'post_date': post_date,
                    'price': price,
                    'structure_name': structure_name,
                    'floor': floor,
                    'vehicle': {
                        'make': make,
                        'model': model,
                        'year': year,
                        'color': color,
                        'license_plate': license_plate
                    },
                    'comment': comment
                }
            return listings_dict
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error trying to get listings: {e}"
        )