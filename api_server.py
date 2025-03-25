from flask import Flask, request, jsonify
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Инициализация Flask
app = Flask(__name__)

# Загружаем API-ключи из переменных окружения
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")

# Инициализация Firebase (ключ теперь загружается из переменной окружения)
firebase_key = os.getenv("FIREBASE_KEY")
if not firebase_key:
    raise ValueError("FIREBASE_KEY is not set in environment variables")

cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Функция для получения данных из Ticketmaster
def get_ticketmaster_events():
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        'apikey': TICKETMASTER_API_KEY,
        'city': 'New York',
        'classificationName': 'music',
        'size': 5
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if '_embedded' in data and 'events' in data['_embedded']:
            return [{
                'title': event['name'],
                'url': event['url'],
                'date': event['dates']['start']['localDate'],
                'image': event['images'][0]['url'] if 'images' in event else ''
            } for event in data['_embedded']['events']]
    return []

# Функция для получения данных из Google Custom Search
def get_google_search_results(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return [{
            'title': item['title'],
            'link': item['link']
        } for item in data.get('items', [])]
    return []

# Функция для сохранения данных в Firebase
def save_to_firebase(user_id, ticketmaster_events, google_results):
    user_ref = db.collection('users').document(user_id)
    data = {
        'ticketmaster_events': ticketmaster_events,
        'google_search_results': google_results
    }
    user_ref.set(data, merge=True)

# API-эндпоинт для поиска мероприятий
@app.route('/search_events', methods=['POST'])
def search_events():
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    ticketmaster_events = get_ticketmaster_events()
    google_results = get_google_search_results("concert New York USA")

    save_to_firebase(user_id, ticketmaster_events, google_results)

    return jsonify({
        "message": f"Data saved for user {user_id}",
        "ticketmaster_events": ticketmaster_events,
        "google_search_results": google_results
    })

# Запуск сервера (без debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
