import requests
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Инициализация Firebase
cred = credentials.Certificate(r"C:\Users\snat1\PycharmProjects\pythonProject22\firebase-key.json")
firebase_admin.initialize_app(cred)

# Получение ссылки на Firestore
db = firestore.client()


# 2. Функция для получения данных из Ticketmaster
def get_ticketmaster_events():
    # API запрос для поиска событий Ticketmaster
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        'apikey': 'P59jKnr7xCEswA82pIAI4cyeL2hnWq2q',
        'city': 'New York',
        'classificationName': 'music',
        'size': 5  # Получаем 5 событий
    }
    response = requests.get(url, params=params)

    events = []
    if response.status_code == 200:
        data = response.json()
        if '_embedded' in data and 'events' in data['_embedded']:
            events = [{
                'title': event['name'],
                'url': event['url'],
                'date': event['dates']['start']['localDate'],
                'image': event['images'][0]['url'] if 'images' in event else ''
            } for event in data['_embedded']['events']]
    else:
        print(f"Ошибка Ticketmaster: {response.status_code}")

    return events


# 3. Функция для получения данных из Google Custom Search
def get_google_search_results(query):
    # API запрос для поиска событий через Google Custom Search
    api_key = 'AIzaSyCw1C3DWgsDhqthKtEZ0PbFvyEHEfmJwTc'
    cx = '40e99c9ba07c64486'
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"

    response = requests.get(url)

    results = []
    if response.status_code == 200:
        data = response.json()
        results = [{
            'title': item['title'],
            'link': item['link']
        } for item in data.get('items', [])]
    else:
        print(f"Ошибка Google Custom Search: {response.status_code}")

    return results


# 4. Функция для сохранения результатов в Firebase
def save_to_firebase(user_id, ticketmaster_events, google_results):
    # Ссылка на коллекцию пользователей в Firestore
    user_ref = db.collection('users').document(user_id)

    # Собираем данные для сохранения
    data = {
        'ticketmaster_events': ticketmaster_events,
        'google_search_results': google_results
    }

    # Записываем в Firebase
    user_ref.set(data, merge=True)
    print(f"Данные для пользователя {user_id} успешно сохранены в Firebase!")


# 5. Главная функция
def main():
    # Пример user_id, который вы получаете из Firebase
    user_id = "user_example_id"

    # Получаем данные о событиях
    ticketmaster_events = get_ticketmaster_events()
    google_results = get_google_search_results("concert New York USA")

    # Сохраняем результаты в Firebase
    save_to_firebase(user_id, ticketmaster_events, google_results)


if __name__ == "__main__":
    main()
