import requests
 
 
def lookupFood(ean):
  req = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{ean}.json")
  if req.status_code == 200:
    return req.json()
  else:
    raise Exception(f"Failed to get food for ean '{ean}'. HTTP status code {req.status_code}")
