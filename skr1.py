import firebase_admin
from firebase_admin import credentials, firestore

# Инициализация Firebase
cred = credentials.Certificate(r"C:\Users\snat1\PycharmProjects\pythonProject22\firebase-key.json")
firebase_admin.initialize_app(cred)

# Получаем ссылку на базу данных Firestore
db = firestore.client()

# Указываем путь к документу
doc_ref = db.collection('counties').document('TPigcWbtBXOEXaG600VS75Iwk3s2')

# Получаем документ
doc = doc_ref.get()

# Проверяем, существует ли документ и выводим его данные
if doc.exists:
    print(f"Документ найден: {doc.to_dict()}")
else:
    print("Документ с указанным ID не найден!")


    # AIzaSyCw1C3DWgsDhqthKtEZ0PbFvyEHEfmJwTc
    # r"C:\Users\snat1\Documents\chromedriver-win64\chromedriver.exe"
    # GQA5LB3UD4MF3ZJBVL - api eventbrite