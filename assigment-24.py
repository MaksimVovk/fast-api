# - Create a list of 5 animals called zoo

# - Delete the animal at the 3rd index.

# - Append a new animal at the end of the list

# - Delete the animal at the beginning of the list.

# - Print all the animals

# - Print only the first 3 animals

zoo = ['Elephant', 'Zebra', 'Girafe', 'Lion', 'Volf']
print(f'zoo: ${zoo}')
zoo.pop(3)
print(f'Delete the animal at the 3rd index: ${zoo}')
zoo.append('python')
print(f'Append a new animal at the end of the list: ${zoo}')
zoo.remove(zoo[0])
print(f'Delete the animal at the beginning of the list: ${zoo}')
print(f'Print only the first 3 animals: ${zoo[0:3]}')