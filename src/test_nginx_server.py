import requests

class TestNginxHTTPS:
  PARKING_DOMAIN = "parking.titanpark.online"  # Replace with your actual domain
  HTTPS_URL = f"https://{PARKING_DOMAIN}/docs"
  HTTP_URL = f"http://{PARKING_DOMAIN}/docs"

  def test_TC_NS1(self):
      """
      Flutter requires an API to be hosted using HTTPS so we need to test that
      our parking microservice API is using HTTPS or our flutter app won't be
      able to make API requests to it.
      """
      try:
        res = requests.get(self.HTTPS_URL, verify=True)
        assert res.status_code == 200
      except Exception as e:
         raise AssertionError("Unable to connect to server using HTTPS.") from None

  def test_TC_NS2(self):
    """
    Requests made to the server using HTTP should be redirected to use HTTPS.
    """
    res = requests.get(
      self.HTTP_URL,
      allow_redirects=False
    )

    # Check that server tried to redirect request
    assert res.status_code in [301, 302, 307, 308], \
      "Did not redirect from HTTP to HTTPS"

    # Check that redirect location is using https
    location = res.headers.get('Location', '')
    assert 'https://' in location
