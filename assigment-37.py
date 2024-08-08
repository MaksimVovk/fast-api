# - Create a function that takes in 3 parameters(firstname, lastname, age) and

# returns a dictionary based on those values

def getUserData(firstname, lastname, age):
  return {
    'firstname': firstname,
    'lastname': lastname,
    'age': age,
  }

userData = getUserData(firstname='Frodo', lastname='Baggins', age=40)

print(userData)