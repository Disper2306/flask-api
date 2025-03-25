import requests

# Замените YOUR_API_KEY на ваш ключ
url = "https://www.eventbriteapi.com/v3/events/search/"
params = {
    'q': 'Concert',  # Тип события
    'location.address': 'New York',  # Местоположение
    'token': 'YHPP2UZ2XWOTLDXM26QN'  # Ваш API ключ
}

response = requests.get(url, params=params)

if response.status_code == 200:
    events = response.json()
    print(events)
else:
    print(f"Error {response.status_code}: {response.text}")

