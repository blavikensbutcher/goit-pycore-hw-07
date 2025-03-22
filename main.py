import datetime
from collections import UserDict

from colorama import Back, Fore

from decorators.input_error import input_error
from helpers.parse_input import parse_input


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

        if not isinstance(value, str):
            raise ValueError("Date should be a string")

        try:
            self.value = datetime.datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Number must contain 10 numbers")
        self.phone = value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    @input_error
    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def get_birthday(self):
        return self.birthday

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                self.phones.remove(ph)

    def edit_phone(self, old_number: str, new_number: str):
        for index, phone in enumerate(self.phones):
            if str(old_number) == str(phone):
                self.phones[index] = Phone(new_number)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    @staticmethod
    def is_next_week(value: datetime.datetime) -> bool:
        today = datetime.datetime.today().date()
        start_of_next_week = today + datetime.timedelta(days=(7 - today.weekday()))
        end_of_next_week = start_of_next_week + datetime.timedelta(days=6)

        value = value.replace(year=today.year)

        return start_of_next_week <= value.date() <= end_of_next_week

    def add_record(self, record):
        self.data[record.name.value] = record
        return self.data[record.name.value]

    def find(self, name: str) -> Record | str:
        try:
            print(self.data[name])
            return self.data[name]
        except KeyError:
            return "Not found"

    def get_upcoming_birthdays(self):
        return [
            {
                "name": guy.name.value,
                "phone": [phone.value for phone in guy.phones],
                "birthday": (
                    guy.birthday.value.strftime("%d.%m.%Y") if guy.birthday else None
                ),
            }
            for guy in self.data.values()
            if guy.birthday and self.is_next_week(guy.birthday.value)
        ]

    def show_all(self):
        all_people = [str(human) for _, human in self.data.items()]
        print(all_people)
        return all_people

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)


@input_error
def add_contact(args, book: AddressBook):
    message = f"Contact: {Back.GREEN} {args[0]} updated {Back.RESET}"
    if args[0] in book:
        record = book[args[0]]
        record.add_phone(args[1])
    else:
        record = Record(args[0])
        record.add_phone(args[1])
        book.add_record(record)
        message = f"Contact: {Back.GREEN}{Fore.BLACK} {args[0]} created {Back.RESET} {Fore.RESET}"
    return message


@input_error
def add_birthday(args, book: AddressBook):
    message = f"Contacts: {Back.GREEN}{Fore.BLACK} {args[0]} birthday updated {Back.RESET}{Fore.RESET}"
    record = book.find(args[0])
    record.add_birthday(args[1])
    return message


@input_error
def show_birthday(args, book: AddressBook):
    record = book[args[0]]
    return record.get_birthday()


@input_error
def birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()


def main():
    book = AddressBook()
    print(Fore.CYAN + "Welcome to the assistant bot!")
    try:
        while True:
            user_input = input(Fore.GREEN + "Enter a command: " + Fore.RESET)
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print(Fore.WHITE + Back.BLACK + "Good bye!" + Fore.RESET)
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                try:
                    print(add_contact(args, book))
                except ValueError as e:
                    print(Fore.RED + f"Error: {e}")

            elif command == "change":
                record = book.find(args[0])
                record.edit_phone(args[1], args[2])
            elif command == "all":
                book.show_all()
            elif command == "phone":
                book.find(args[0])
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(book))
            else:
                print(Fore.RED + "Invalid command." + Fore.RESET)
    except KeyboardInterrupt:
        print("\n" + Fore.WHITE + Back.BLACK + "Good bye!" + Fore.RESET)
        exit()
    except Exception as e:
        print("\n" + Fore.RED + f"{e}" + Fore.RESET)


if __name__ == "__main__":
    main()
