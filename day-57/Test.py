import requests

r_gender = requests.get(f"https://api.genderize.io?name=neil").json()
r_age = requests.get(f"https://api.agify.io?name=neil").json()
name = "neil".title()
print(r_age["age"])
print(r_gender["gender"])



