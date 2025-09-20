from bs4 import BeautifulSoup
import requests

class ParkingSpaces:
  def __init__(self):
    self.url = 'https://parking.fullerton.edu/ParkingLotCounts/mobile.aspx'
    self.base_price = 100  # Price in cents
  
  def get_available_parking(self):
    # Get data from CSUF parking services website
    res = requests.get(self.url)
    data = res.text
    soup = BeautifulSoup(data, features="html.parser")

    # Parse data
    table = soup.find_all('table', {"class": "AvailabilityTable"})[0]
    all_tr = table.find_all('tr')

    # We don't want to fetch prices for all parking structures
    exclude_locs = set(['Fullerton Free Church', 'S8 and S10'])

    parking_dict = {
      'Nutwood_Structure': {'available': None, 'total': 2504, 'perc_full': None},
      'State_College_Structure': {'available': None, 'total': 1373, 'perc_full': None},
      'Eastside_North': {'available': None, 'total': 1880, 'perc_full': None},
      'Eastside_South': {'available': None, 'total': 1242, 'perc_full': None},
    }
    # Iterate through rows in table
    for tr in all_tr:
      # Get parking structure name
      name_el = tr.css.select('.LocationName a')
      if len(name_el) == 0:
        name_el = tr.css.select('.LocationName span')
      # Skip if no name
      if len(name_el) == 0: continue
      struct_name = name_el[0].text
      # Skip if this parking structure is in excluded list
      if struct_name in exclude_locs: continue
      # Get available parkings spots
      avail_count_el = tr.css.select('.AvailableCountYellow span')
      # Skip if parking spots not available
      if len(avail_count_el) == 0: continue
      avail_count = avail_count_el[0].text
      # Skip if available parking spots is not a numerical value
      # Sometimes is returns "Open" instead of a number
      if not avail_count.isdigit(): continue
      avail_count = int(avail_count)

      # Valid parking spot if this point is reached
      struct_key = struct_name.replace(' ', '_')  # Remove spaces from name so we can use key in url
      parking_dict[struct_key]['name'] = struct_name
      parking_dict[struct_key]['available'] = avail_count
      parking_dict[struct_key]['perc_full'] = round(1 - (avail_count / parking_dict[struct_key]['total']), 2)
      parking_dict[struct_key]['price_in_cents`'] = self.get_dynamic_price(parking_dict[struct_key]['perc_full'])

    return parking_dict

  def get_dynamic_price(self, perc_full):
    """Set a price based on how full the structure is"""
    if perc_full <= 0.4:
      return self.base_price
    elif perc_full <= 0.6:
      return self.base_price * 1.5
    elif perc_full <= 0.8:
      return self.base_price * 2.0
    else:
      return self.base_price * 2.5

if __name__ == "__main__":
  ps = ParkingSpaces()
  print(ps.get_available_parking())