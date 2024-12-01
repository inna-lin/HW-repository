from pymongo import MongoClient
import json

# Підключення до MongoDB
client = MongoClient("mongodb+srv://lin:****@hw.gdpsk.mongodb.net/?retryWrites=true&w=majority")
db = client['quotes_db']

# Імпорт даних у MongoDB
with open('authors.json', 'r', encoding='utf-8') as a_file:
    authors_data = json.load(a_file)
    db.authors.insert_many(authors_data)

with open('qoutes.json', 'r', encoding='utf-8') as q_file:
    quotes_data = json.load(q_file)
    db.qoutes.insert_many(quotes_data)