# - Create a variable grade holding an integer between 0 - 100

# - Code if, elif, else statements to print the letter grade of the number grade variable

# Grades:

# A = 90 - 100

# B = 80 - 89

# C = 70-79

# D = 60 - 69

# F = 0 - 59



# Example:

# if grade = 87 then print('B')

grade = int(input('Enter your grade: '))
if grade >= 90 and grade < 101:
  print('A')
elif grade >= 80 and grade < 90:
  print('B')
elif grade >= 70 and grade < 80:
  print('C')
elif grade >= 60 and grade < 70:
  print('D')
else:
  print('F')