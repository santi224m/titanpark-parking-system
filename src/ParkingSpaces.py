from bs4 import BeautifulSoup
import requests

class ParkingSpaces:
  def __init__(self):
    self.url = 'https://parking.fullerton.edu/ParkingLotCounts/mobile.aspx'
  
  def get_available_parking(self):
    # Get data from CSUF parking services website
    res = requests.get(self.url)
    data = res.text
    soup = BeautifulSoup(data, features="html.parser")

    # Parse data
    table = soup.find_all('table', {"class": "AvailabilityTable"})[0]
    all_tr = table.find_all('tr')

    # We don't want to fetch prices for all parking spots
    exclude_locs = set(['Fullerton Free Church'])

    parking_dict = {}
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
      parking_dict[struct_name] = avail_count
    
    return parking_dict

if __name__ == "__main__":
  ps = ParkingSpaces()
  print(ps.get_available_parking())