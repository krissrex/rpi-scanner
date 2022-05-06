#users.py
 
 
def loadUsers():
  """Reads NFC UUID to User mapping from users.txt
  """
  users = dict()
  with open("users.txt", "r") as f:
    for line in f.readlines():
      if line.startswith("#") or line.strip() == "":
        continue
      parts = line.split(" ")
      user_uuid = parts[0]
      user_name = parts[1].strip()
      users[user_uuid] = user_name
  return users
 
def findUser(uuid):
  """Looks up a user from the users.txt file.
  """
  users = loadUsers()
  user = users[uuid]
  return user