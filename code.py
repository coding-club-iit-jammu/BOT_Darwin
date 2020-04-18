import requests

URL = "https://api.adviceslip.com/advice"
r = requests.get(url = URL) 
data = r.json() 
print(data['slip']['advice'])