import db
import shelve
import uuid
import group
import datetime

bills = []


class Bill:

    def __init__(self, payment_id, user_id, group_id, description, amount, date):
        self.__payment_id = payment_id
        self.__user_id = user_id
        self.__group_id = group_id
        self.__description = description
        self.__amount = amount
        self.__date = date

    def get_payment_id(self):
        return self.__payment_id

    def get_user_id(self):
        return self.__user_id

    def get_group_id(self):
        return self.__group_id

    def get_description(self):
        return self.__description

    def get_amount(self):
        return self.__amount

    def get_date(self):
        return self.__date


def create_bill(user_id):
    with shelve.open('data') as sh:
        sh[str(user_id)] = {'payment_id': uuid.uuid4(), 'group_id': group.get_current_group(user_id)}


def put_data(user_id, key, val):
    with shelve.open('data') as sh:
        sh[str(user_id)][key] = val


def get_data(user_id, key):
    with shelve.open('data') as sh:
        return sh[str(user_id)][key]


def insert_payment(user_id):
    data = get_data(user_id)
    db.insert_payment(data['payment_id'], user_id, data['group_id'], data['description'], data['amount'], datetime.date.today().strftime('%Y-%m-%d'))
    bills.append(Bill(data['payment_id'], user_id, data['group_id'], data['description'], data['amount'], datetime.date.today().strftime('%Y-%m-%d')))


def get_data():
    data = db.select_bills()
    for bill in data:
        bills.append(Bill(bill[0], bill[1], bill[2], bill[3], bill[4], bill[5]))


get_data()
