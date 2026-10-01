import requests

url = "https://amflip-backend-production.up.railway.app/extract"
files = {"file": open("","rb")}
reponse = request.post(url , files=files)

print(reponse.json())
