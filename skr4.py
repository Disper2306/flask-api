import requests

def search_ticketmaster(query, location=""):
    ticketmaster_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": "P59jKnr7xCEswA82pIAI4cyeL2hnWq2q",
        "keyword": query,
        "city": location,
    }
    response = requests.get(ticketmaster_url, params=params)
    return response.json()

# Пример использования
events = search_ticketmaster("concert", "New York")
print(events)
