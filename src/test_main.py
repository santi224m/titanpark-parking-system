from fastapi.testclient import TestClient

from main import app
from helpers import TestHelper
from datetime import datetime, timedelta

client = TestClient(app)

expected_structs = [
    'Nutwood_Structure',
    'State_College_Structure',
    'Eastside_North',
    'Eastside_South'
]

def test_root_to_docs_redirect():
    """
    Users should be redirected to the API documentation when the visit the
    root path.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.url == 'http://testserver/docs'

def test_TC_LPD1():
    """
    Live parking data API at path “/parking_data/all” should return information
    regarding how full a parking structure is for Nutwood Structure, State College
    Structure, Eastside North, and Eastside South.
    """
    response = client.get("/parking_data/all")
    assert response.status_code == 200
    res = response.json()

    # Test that all structures are present
    for struct in expected_structs:
        assert struct in res

    for struct in expected_structs:
        curr_struct = res[struct]

        # Test data types
        assert type(curr_struct['available']) == int
        assert type(curr_struct['total']) == int
        assert type(curr_struct['perc_full']) == float
        assert type(curr_struct['price_in_cents']) == int

        # Test that name is correct
        assert curr_struct['name'] == struct.replace('_', ' ')

def test_TC_LPD2():
    """
    Live parking data API at path “/parking_data/{struct_name}” should return
    information regarding how full a parking structure is for the specified
    parking structure.
    """
    for struct in expected_structs:
      response = client.get(f"/parking_data/{struct}")
      assert response.status_code == 200
      res = response.json()

      # Test data types
      assert type(res['available']) == int
      assert type(res['total']) == int
      assert type(res['perc_full']) == float
      assert type(res['price_in_cents']) == int

      # Test that name is correct
      assert res['name'] == struct.replace('_', ' ')

def test_TC_LPD3():
    """
    Users should get an error if they make a call to ”/parking_data/{struct_name}" with a structure that isn’t in our list of supported parking structures.
    """
    response = client.get("/parking_data/Fake_Structure")
    assert response.status_code == 200
    res_json = response.json()
    assert "Error" in res_json
    assert res_json['Error'] == "Structure 'Fake_Structure' not in parking data"

def test_TC_PMS1():
    """
    Test that “/add_vehicle” path inserts a user's vehicle to the database.
    """
    user_id = 'testuser123'
    make = 'Volkswagen'
    model = 'Jetta'
    year = 2014
    color = 'red'
    license_plate = 'LI12345'
    params = {
        'user_id': user_id,
        'make': make,
        'model': model,
        'year': str(year),
        'color': color,
        'license_plate': license_plate
    }
    res = client.post("/add_vehicle", params=params)
    assert res.status_code == 200
    res_json = res.json()
    assert 'status' in res_json and res_json['status'] == 'success'
    assert 'vehicle_uuid' in res_json
    # Get uuid assigned to vehicle to check it and delete it after
    vehicle_uuid = res_json['vehicle_uuid']
    res = TestHelper.get_db_vehicle(vehicle_uuid)
    db_id, db_user_id, db_make, db_model, db_year, db_color, db_license_plate = res
    # Check that all values were inserted correctly
    assert user_id == db_user_id
    assert make == db_make
    assert model == db_model
    assert year == db_year
    assert color == db_color
    assert license_plate == db_license_plate
    TestHelper.delete_db_vehicle(vehicle_uuid)

def test_TC_PMS2():
    """
    Test that “/get_user_vehicles” path returns a list of vehicles belonging to the specified user.
    """
    # Insert multiple vehicles to database before calling api
    testuser = 'testuser123'
    vehicles = [
        [testuser, 'Lexus', 'LS', 2023, 'Gray', 'JGLAJG91'],
        [testuser, 'Porsche', '718 Cayman GT4 RS', 2020, 'Blue', 'LSADGJL'],
        [testuser, 'Audi', 'A7', 2025, 'White', 'QIKGBUSL'],
    ]

    vehicle_uuid_list = []
    for idx, v in enumerate(vehicles):
        uuid = TestHelper.insert_db_vehicle(v[0], v[1], v[2], v[3], v[4], v[5])
        vehicle_uuid_list.append(uuid)
        vehicles[idx].append(uuid)

    # Get user vehicles using API
    res = client.get("/get_user_vehicles", params={'user_id': testuser})
    assert res.status_code == 200
    res_json = res.json()
    # Check that all 3 vehicles were inserted
    assert len(res_json) == 3

    # Check that data is the same
    for v in vehicles:
        uuid = v[-1]
        v_json = res_json[uuid]
        assert v[1] == v_json['make']
        assert v[2] == v_json['model']
        assert v[3] == v_json['year']
        assert v[4] == v_json['color']
        assert v[5] == v_json['license_plate']

    # Delete test vehicles from database
    for uuid in vehicle_uuid_list:
        TestHelper.delete_db_vehicle(uuid)

def test_TC_PMS3():
    """
    Test that “/add_listing” path inserts a parking listing in the database.
    """
    # User must have at least one vehicle before creating a listing
    user_id = 'testuser123'
    nutwood_struct_id = 1
    price = 100
    floor = 3
    comment = 'This is a comment'
    vehicle_uuid = TestHelper.insert_db_vehicle(user_id, 'Volkswagen', 'Jetta', 2014, 'red', 'SAFJLK212')
    params = {
        'user_id': user_id,
        'price': price,
        'structure_id': nutwood_struct_id,
        'floor': floor,
        'vehicle_id': vehicle_uuid,
        'comment': comment
    }
    res = client.post("/add_listing", params=params)
    assert res.status_code == 200
    res_json = res.json()
    assert 'status' in res_json and res_json['status'] == 'success'
    assert 'listing_uuid' in res_json
    listing_uuid = res_json['listing_uuid']
    try:
        res = TestHelper.get_db_listing(listing_uuid)
        assert res is not None and len(res) == 8
        db_id, db_user_id, db_post_date, db_price, db_structure_id, db_floor, db_vehicle_id, db_comment = res
        assert user_id == db_user_id
        assert price == db_price
        assert nutwood_struct_id == db_structure_id
        assert floor == db_floor
        assert vehicle_uuid == db_vehicle_id
        assert comment == db_comment

        # Check that post date was auto set to right now
        assert datetime.now() - db_post_date < timedelta(seconds=5)

    # Clean up database
    finally:
        TestHelper.delete_db_listing(listing_uuid)
        TestHelper.delete_db_vehicle(vehicle_uuid)