import requests

url = ""
files = {"file": open("","rb")}
reponse = request.post(url , files=files)

print(reponse.json())
