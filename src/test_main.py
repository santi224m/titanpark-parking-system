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
    Users should get an error if they make a call to ”/parking_data/{struct_name}"
    with a structure that isn't in our list of supported parking structures.
    """
    response = client.get("/parking_data/Fake_Structure")
    assert response.status_code == 422


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
    vehicle_uuid = TestHelper.insert_db_vehicle(
        user_id, 'Volkswagen', 'Jetta', 2014, 'red', 'SAFJLK212')
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


def test_TC_PMS4():
    """
    Test that “/get_listings” path returns a list of all parking listings,
    which will be displayed to users who are trying to purchase a parking spot.
    """
    # Create 3 listings before checking for list
    listing_1 = {
        'user_id': 'testuser123',
        'price': 100,
        'structure_id': 1,
        'structure_name': 'Nutwood Structure',
        'floor':  2,
        'vehicle_id': None,
        'comment': 'This is a comment for listing 1',
        'make': 'Volkswagen',
        'model': 'Jetta',
        'year': 2014,
        'color': 'Red',
        'license_plate': 'SAFJLK212',
    }
    listing_1['vehicle_id'] = TestHelper.insert_db_vehicle(
        listing_1['user_id'],
        listing_1['make'],
        listing_1['model'],
        listing_1['year'],
        listing_1['color'],
        listing_1['license_plate'],
    )
    listing_1_uuid = TestHelper.insert_db_listing(
        listing_1['user_id'],
        listing_1['price'],
        listing_1['structure_id'],
        listing_1['floor'],
        listing_1['vehicle_id'],
        listing_1['comment'],
    )

    listing_2 = {
        'user_id': 'testuser456',
        'price': 150,
        'structure_id': 2,
        'structure_name': 'State College Structure',
        'floor': 1,
        'vehicle_id': None,
        'comment': 'This is a comment for listing 2',
        'make': 'Ford',
        'model': 'Mustang',
        'year': 2020,
        'color': 'Black',
        'license_plate': 'LKSJFD193'
    }
    listing_2['vehicle_id'] = TestHelper.insert_db_vehicle(
        listing_2['user_id'],
        listing_2['make'],
        listing_2['model'],
        listing_2['year'],
        listing_2['color'],
        listing_2['license_plate'],
    )
    listing_2_uuid = TestHelper.insert_db_listing(
        listing_2['user_id'],
        listing_2['price'],
        listing_2['structure_id'],
        listing_2['floor'],
        listing_2['vehicle_id'],
        listing_2['comment']
    )

    listing_3 = {
        'user_id': 'testuser789',
        'price': 223,
        'structure_id': 3,
        'structure_name': 'Eastside North',
        'floor': 4,
        'vehicle_id': None,
        'comment': 'This is a comment for listing 3',
        'make': 'CFMoto',
        'model': '300ss',
        'year': 2023,
        'color': 'Gray',
        'license_plate': 'KLAJGJ1738'
    }
    listing_3['vehicle_id'] = TestHelper.insert_db_vehicle(
        listing_3['user_id'],
        listing_3['make'],
        listing_3['model'],
        listing_3['year'],
        listing_3['color'],
        listing_3['license_plate'],
    )
    listing_3_uuid = TestHelper.insert_db_listing(
        listing_3['user_id'],
        listing_3['price'],
        listing_3['structure_id'],
        listing_3['floor'],
        listing_3['vehicle_id'],
        listing_3['comment']
    )

    # Now call api to get all listings
    try:
        res = client.get("/get_listings")
        assert res.status_code == 200
        res_json = res.json()

        # Test that all listings are in database
        assert listing_1_uuid in res_json
        assert listing_2_uuid in res_json
        assert listing_3_uuid in res_json

        # Test that inserted data matches data in database
        listing_1_db = res_json[listing_1_uuid]
        listing_2_db = res_json[listing_2_uuid]
        listing_3_db = res_json[listing_3_uuid]

        listing_pairs = [
            (listing_1, listing_1_db),
            (listing_2, listing_2_db),
            (listing_3, listing_3_db),
        ]

        for inserted_listing, db_listing in listing_pairs:
            assert inserted_listing['user_id'] == db_listing['user_id']
            assert inserted_listing['price'] == db_listing['price']
            assert inserted_listing['structure_name'] == db_listing['structure_name']
            assert inserted_listing['floor'] == db_listing['floor']
            assert inserted_listing['comment'] == db_listing['comment']
            assert inserted_listing['make'] == db_listing['vehicle']['make']
            assert inserted_listing['model'] == db_listing['vehicle']['model']
            assert inserted_listing['year'] == db_listing['vehicle']['year']
            assert inserted_listing['color'] == db_listing['vehicle']['color']
            assert inserted_listing['license_plate'] == db_listing['vehicle']['license_plate']
    finally:
        TestHelper.delete_db_listing(listing_1_uuid)
        TestHelper.delete_db_vehicle(listing_1['vehicle_id'])

        TestHelper.delete_db_listing(listing_2_uuid)
        TestHelper.delete_db_vehicle(listing_2['vehicle_id'])

        TestHelper.delete_db_listing(listing_3_uuid)
        TestHelper.delete_db_vehicle(listing_3['vehicle_id'])


def test_TC_PMS5():
    """
    Test that “/delete_vehicle” path correctly deletes a vehicle from the database.
    """
    # Insert test vehicle into database
    vehicle = {
        'user_id': 'testuser123',
        'vehicle_id': None,
        'make': 'Volkswagen',
        'model': 'Jetta',
        'year': 2014,
        'color': 'Red',
        'license_plate': 'SAFJLK212',
    }

    try:
        vehicle['vehicle_id'] = TestHelper.insert_db_vehicle(
            vehicle['user_id'],
            vehicle['make'],
            vehicle['model'],
            vehicle['year'],
            vehicle['color'],
            vehicle['license_plate'],
        )

        # Delete vehicle using API
        params = {'vehicle_id': vehicle['vehicle_id']}
        res = client.post("/delete_vehicle", params=params)
        assert res.status_code == 200

        # Check that vehicle is no longer in database
        db_vehicle = TestHelper.get_db_vehicle(vehicle['vehicle_id'])
        assert db_vehicle is None
    finally:
        # Delete vehicle using helper in case test fails
        TestHelper.delete_db_vehicle(vehicle['vehicle_id'])
