from pymongo import MongoClient
from bson.objectid import ObjectId

# Налаштування підключення
client = MongoClient("mongodb://localhost:27017/")
db = client["cat_database"]
collection = db["cats"]

# CREATE
def add_cat(name, age, features):
    """Додає нового кота до колекції."""
    try:
        cat = {"name": name, "age": age, "features": features}
        result = collection.insert_one(cat)
        print(f"Кота додано з id: {result.inserted_id}")
    except Exception as e:
        print(f"Помилка при додаванні кота: {e}")

# READ
def get_all_cats():
    """Виводить усіх котів з колекції."""
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Помилка при отриманні котів: {e}")

def get_cat_by_name(name):
    """Виводить інформацію про кота за його ім'ям."""
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f"Помилка при отриманні кота: {e}")

# UPDATE
def update_cat_age(name, new_age):
    """Оновлює вік кота за ім'ям."""
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count:
            print(f"Вік кота '{name}' оновлено до {new_age} років.")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f"Помилка при оновленні віку кота: {e}")

def add_cat_feature(name, feature):
    """Додає нову характеристику до списку features кота за ім'ям."""
    try:
        result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
        if result.modified_count:
            print(f"До характеристик кота '{name}' додано: {feature}")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f"Помилка при додаванні характеристики: {e}")

# DELETE
def delete_cat_by_name(name):
    """Видаляє кота з колекції за його ім'ям."""
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"Кота '{name}' видалено.")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f"Помилка при видаленні кота: {e}")

def delete_all_cats():
    """Видаляє всі записи з колекції."""
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів.")
    except Exception as e:
        print(f"Помилка при видаленні всіх записів: {e}")

# Меню
def main():
    while True:
        print("\nВиберіть дію:")
        print("1 Додати кота")
        print("2 Перелік котів")
        print("3 Знайти кота за ім'ям")
        print("4 Оновити вік кота")
        print("5 Додати характеристику коту")
        print("6 Видалити кота за ім'ям")
        print("7 Видалити всіх котів")
        print("0 Вийти")

        choice = input("Ваш вибір: ")

        if choice == "1":
            name = input("Ім'я кота: ")
            age = int(input("Вік кота: "))
            features = input("Характеристики (через кому): ").split(", ")
            add_cat(name, age, features)
        elif choice == "2":
            get_all_cats()
        elif choice == "3":
            name = input("Ім'я кота: ")
            get_cat_by_name(name)
        elif choice == "4":
            name = input("Ім'я кота: ")
            new_age = int(input("Новий вік: "))
            update_cat_age(name, new_age)
        elif choice == "5":
            name = input("Ім'я кота: ")
            feature = input("Нова характеристика: ")
            add_cat_feature(name, feature)
        elif choice == "6":
            name = input("Ім'я кота: ")
            delete_cat_by_name(name)
        elif choice == "7":
            delete_all_cats()
        elif choice == "0":
            print("Вихід.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
