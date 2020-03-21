import db
import uuid
import group
import user
import datetime
import debt

temp = {}


def create_bill(user_id):
    temp[user_id] = {'payment_id': str(uuid.uuid4()), 'group_id': user.get_current_group(user_id), 'selected': []}


def put_data(user_id, key, val):
    try:
        temp[user_id][key] = val
    except KeyError:
        temp[user_id] = {}
        temp[user_id][key] = val


def get_data(user_id, key):
    return temp[user_id][key]


def set_selected(user_id, selected_id):
    temp[user_id]['selected'].append(selected_id)


def get_selected(user_id):
    return temp[user_id]['selected']


def clear_selected(user_id):
    temp[user_id]['selected'].clear()


def insert_payment(user_id):
    db.insert_payment(get_data(user_id, 'payment_id'), user_id, get_data(user_id, 'group_id'),
                      get_data(user_id, 'description'), get_data(user_id, 'amount'),
                      datetime.date.today().strftime('%Y-%m-%d'))


def get_bills_msg(user_id):
    group_id = group.get_current_group(user_id)
    l = [bill for bill in bills if bill.get_group_id() == group_id]
    msg = ""
    for b in l:
        msg = msg + str(b) + '\n'
    return msg


def get_bills_for_edit(user_id):
    group_id = user.get_current_group(user_id)
    data = db.select_payments_by_user_id_and_group_id(user_id, group_id)
    return data


def update_bill_description(user_id):
    db.update_bill_description(get_data(user_id, 'edit_bill_description'), get_data(user_id, 'edit_payment_id'))


def update_bill_amount(user_id):
    db.update_bill_amount(get_data(user_id, 'edit_bill_amount'), get_data(user_id, 'edit_payment_id'))
    debt.update_debt(user_id, get_data(user_id, 'edit_bill_amount'), get_data(user_id, 'edit_payment_id'))
