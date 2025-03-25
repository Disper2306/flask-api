import requests

# Настроенные параметры
API_KEY = 'AIzaSyCw1C3DWgsDhqthKtEZ0PbFvyEHEfmJwTc'  # Здесь твой API-ключ
CX = '40e99c9ba07c64486'  # Здесь твой Custom Search Engine ID


def search_google_custom(query):
    google_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
    }

    # Выполнение запроса
    response = requests.get(google_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None


# Пример использования
query = "concert New York USA events"
results = search_google_custom(query)

if results:
    for item in results.get("items", []):
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print("-----")
