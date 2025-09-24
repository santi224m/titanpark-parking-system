from fastapi.testclient import TestClient

from main import app

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