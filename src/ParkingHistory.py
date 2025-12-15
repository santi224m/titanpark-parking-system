from pydantic import BaseModel
from datetime import datetime, date

class ParkingHistory(BaseModel):
  id: int
  struct_name: str
  available: int
  total: int
  perc_full: float | None
  datetime: datetime
  date: date

  model_config = {
    'json_schema_extra': {
      'examples': [
        {
          'id': 1,
          'struct_name': 'Nutwood Structure',
          'available': 1316,
          'total': 2504,
          'perc_full': 0.47,
          'datetime': '2025-12-15T11:38:54.518042'
        }
      ]
    }
  }