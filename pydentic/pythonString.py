def add(firstname:str , lastname: str = None):
    return firstname + " " + lastname

first = 66
last = "Doe"
print(add(first, last))  # Output: John Doe

# for password escaping
from urllib.parse import quote_plus

my_password = "2266abdul@123"
escaped_password = quote_plus(my_password)

print(f"Original password: {my_password}")
print(f"Escaped password: {escaped_password}")