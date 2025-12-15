"""
This class contains database methdods
that are used in more than one place within
the application.
"""
from DBHandler import DBHandler
from ParkingHistory import ParkingHistory

class DBMethods:
  @staticmethod
  def get_parking_history(*, date=None):
    query = """
          SELECT
              PDH.id,
              PS.name,
              PDH.available,
              PDH.total,
              PDH.perc_full,
              PDH.datetime,
              PDH.datetime::timestamp::date AS date
          FROM
              parking_data_history AS PDH
              INNER JOIN
                  parking_structure AS PS ON PS.id = structure_id
    """
    if date is not None:
       query += " WHERE PDH.datetime::timestamp::date = %s"
    with DBHandler() as curr:
      if date is None:
        curr.execute(query)
      else:
        curr.execute(query, (date, ))
      res = curr.fetchall()
      history = {'history': []}
      for data in res:
          PH = ParkingHistory(
              id=data[0],
              struct_name=data[1],
              available=data[2],
              total=data[3],
              perc_full=data[4],
              datetime=data[5],
              date=data[6]
          )
          history['history'].append(PH)
      return history