import requests

# Example 1: Correct way to send code
code1 = """def calculate():
    x = 10
    y = 20
    print(x + y)
calculate()"""

# Example 2: Also correct, using triple quotes with no initial newline
code2 = """def hello():
    print("Hello, World!")
hello()"""

# Example 3: If you need multiple blank lines, that's fine too
code3 = """
def greet(name):
    print(f"Hello, {name}!")

def main():
    greet("World")

main()
"""

# Test the formatting
response = requests.post("http://localhost:8000/format", json={"code": code1})
print(response.json()["formatted_code"])

# If the formatting looks good, execute it
response = requests.post("http://localhost:8000/execute", json={"code": code1})
print(response.json())

# Test the formatting
response = requests.post("http://localhost:8000/format", json={"code": code2})
print(response.json()["formatted_code"])

# If the formatting looks good, execute it
response = requests.post("http://localhost:8000/execute", json={"code": code2})
print(response.json())

# Test the formatting
response = requests.post("http://localhost:8000/format", json={"code": code3})
print(response.json()["formatted_code"])

# If the formatting looks good, execute it
response = requests.post("http://localhost:8000/execute", json={"code": code3})
print(response.json())
