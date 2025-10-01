"""Helper functions used in testing"""
from DBHandler import DBHandler


class TestHelper():
  @staticmethod
  def get_db_vehicle(vehicle_uuid: str):
    """Return row for a specific vehicle in 'vehicle' table using uuid"""
    with DBHandler() as curr:
      curr.execute(
        """
        SELECT *
        FROM vehicle
        WHERE id = %s;
        """, (vehicle_uuid, )
      )
      res = curr.fetchone()
      assert res is not None and len(res) == 7
      return res
  
  @staticmethod
  def delete_db_vehicle(vehicle_uuid: str):
    """Delete a vehicle from the database using its id"""
    with DBHandler() as curr:
      # Delete test vehicle from database
      curr.execute(
        """
        DELETE FROM vehicle
        WHERE id = %s;
        """, (vehicle_uuid, )
      )
  
  @staticmethod
  def insert_db_vehicle(user_id: str, make: str, model: str, year: int, color: str, license_plate: str):
    """Insert a vehicle to the database and return its uuid"""
    with DBHandler() as curr:
      curr.execute(
        """
        INSERT INTO vehicle
        (
          user_id,
          make,
          model,
          year,
          color,
          license_plate
        ) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """, (user_id, make, model, year, color, license_plate)
      )
      res = curr.fetchone()
      assert res is not None and len(res) == 1
      vehicle_uuid = res[0]
      return vehicle_uuid
  
  @staticmethod
  def delete_db_listing(listing_uuid: str):
    """Delete a listing from the database"""
    with DBHandler() as curr:
      curr.execute(
        """
        DELETE FROM listing
        WHERE id = %s;
        """, (listing_uuid, )
      )

  @staticmethod
  def get_db_listing(listing_uuid: str):
    """Return a listing row"""
    with DBHandler() as curr:
      curr.execute(
        """
        SELECT *
        FROM listing
        WHERE id = %s;
        """, (listing_uuid, )
      )
      res = curr.fetchone()
      if res is None or len(res) == 0:
        return None
      return res

  @staticmethod
  def insert_db_listing(user_id: str, price: int, structure_id: int, floor: int, vehicle_uuid: str, comment: str):
    """Insert a listing into the database"""
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
          vehicle_uuid,
          comment
        )
      )
      res = curr.fetchone()
      assert res is not None and len(res) == 1
      # Return listing uuid
      return res[0]