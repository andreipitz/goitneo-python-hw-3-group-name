from collections import UserDict
import datetime


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
def input_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command."

    return inner
@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."
@input_error
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        return "Contact not found."
def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        else:
            print("Invalid command.")
class Field:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

class Record:
    def __init__(self):
        self.fields = []

    def add_field(self, name, value):
        field = Field(name, value)
        self.fields.append(field)

    def remove_field(self, name):
        for field in self.fields:
            if field.name == name:
                self.fields.remove(field)
                break

    def edit_field(self, name, value):
        for field in self.fields:
            if field.name == name:
                field.set_value(value)
                break

class ContactBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def remove_record(self, name):
        for record in self.records:
            if record.name == name:
                self.records.remove(record)
                break

    def search(self, criteria):
        results = []
        for record in self.records:
            match = True
            for criterion in criteria:
                found = False
                for field in record.fields:
                    if field.name == criterion:
                        found = True
                        if field.value != criteria[criterion]:
                            match = False
                            break
                if not found:
                    match = False
                    break
            if match:
                results.append(record)
        return results

if __name__ == "__main__":
    main()
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Birthday must be in the format DD.MM.YYYY.")
        self.value = date

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if not isinstance(phone, Phone):
            phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if str(phone) == str(old_phone):
                self.phones[i] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == str(phone):
                return p
        return None

    def add_birthday(self, birthday):
        if not isinstance(birthday, Birthday):
            birthday = Birthday(birthday)
        self.birthday = birthday

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        for record in self.data.values():
            if record.name.value == name:
                return record
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = datetime.date.today()
        next_week = today + datetime.timedelta(days=7)
        birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value
                if today <= birthday_date.date() <= next_week:
                    birthdays.append(f"{record.name}: {birthday_date.strftime('%d.%m.%Y')}")
        return birthdays

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(e)
    return inner

def add_contact(book):
    name = input("Enter the contact's name: ")
    phone = input("Enter the contact's phone number: ")
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    print("Contact added.")

def change_phone(book):
    name = input("Enter the contact's name: ")
    new_phone = input("Enter the new phone number: ")
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0], new_phone)
        print("Phone number changed.")
    else:
        print("Contact not found.")

def show_phone(book):
    name = input("Enter the contact's name: ")
    record = book.find(name)
    if record:
        phone = record.find_phone(name)
        print(phone.value)
    else:
        print("Contact not found.")

def show_all(book):
     for name, record in book.items():
        print(f"Name: {name}")
        print(f"Phones: {', '.join(str(phone) for phone in record.phones)}")
        if record.birthday:
            print(f"Birthday: {record.birthday.value.strftime('%d.%m.%Y')}")
        print()