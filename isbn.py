#isbn.py
import requests
 
def lookupIsbn(isbn):
  req = requests.get(f"https://openlibrary.org/isbn/{isbn}.json")
  if req.status_code == 200:
    return req.json()
  else:
    raise Exception(f"Failed to get book by isbn '{isbn}'. HTTP status {req.status_code}") 
 
 