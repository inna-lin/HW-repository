import pickle
from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.date.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, Phones: {phones}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def search(self, **criteria):
        results = []
        for record in self.data.values():
            match = True
            for key, value in criteria.items():
                if key == "name" and record.name.value != value:
                    match = False
                elif key == "phone" and not any(p.value == value for p in record.phones):
                    match = False
            if match:
                results.append(record)
        return results

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        def adjust_for_weekend(birthday):
            if birthday.weekday() >= 5:  # Якщо субота або неділя
                return find_next_weekday(birthday, 0)  # Переносимо на понеділок
            return birthday

        def find_next_weekday(start_date, weekday):
            days_ahead = weekday - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return start_date + timedelta(days_ahead)

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.date.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = record.birthday.date.replace(year=today.year + 1)

                if 0 <= (birthday_this_year - today).days <= days:
                    birthday_this_year = adjust_for_weekend(birthday_this_year)
                    upcoming_birthdays.append({"name": record.name.value, "birthday": birthday_this_year.strftime("%d.%m.%Y")})

        return upcoming_birthdays

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

# Функції серіалізації та десеріалізації

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

# Функції-обробники команд

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ValueError:
            return "Enter the argument for the command"
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Insufficient arguments."

    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday for {name} set to {birthday}"
    return f"Contact {name} not found"

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is {record.birthday}"
    elif record:
        return f"{name} has no birthday set"
    return f"Contact {name} not found"

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(f"{entry['name']}: {entry['birthday']}" for entry in upcoming_birthdays)
    return "No upcoming birthdays in the next week"

def main():
    book = load_data()  # Завантаження даних із файлу при старті програми
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)  # Збереження даних перед виходом з програми
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command in ["add", "change"]:
            print(add_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "all":
            print(book)
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
