"""
This script should be run every 30 minutes by a cron job
in order to store parking data in the database.

Enter the following in crontab:
*/30 * * * * cd /path/to/repo && /path/to/venv/bin/python /path/to/parking_data_history.py
"""

from ParkingSpaces import ParkingSpaces
from datetime import datetime

from DBHandler import DBHandler

if __name__ == "__main__":
  # Get live parking data
  PS = ParkingSpaces()
  parking_data = PS.get_available_parking()
  dt = datetime.now()

  # Insert parking data into database
  for parking in parking_data.values():
    with DBHandler () as curr:
      # Check that parking structure exists in database
      curr.execute(
        """
        SELECT id
        FROM parking_structure
        WHERE name = %s;
        """, (parking['name'], )
      )
      struct_id = curr.fetchone()

      # Insert structure if it doesn't exist
      if struct_id is None:
        curr.execute(
          """
          INSERT INTO parking_structure
          (name) VALUES (%s)
          RETURNING id;
          """, (parking['name'], )
        )
        struct_id = curr.fetchone()

      # Insert parking data
      curr.execute(
        """
        INSERT INTO parking_data_history
        (
          structure_id,
          available,
          total,
          perc_full,
          datetime
        )
        VALUES (%s, %s, %s, %s, %s);
        """, (
          struct_id,
          parking['available'],
          parking['total'],
          parking['perc_full'],
          dt
        )
      )