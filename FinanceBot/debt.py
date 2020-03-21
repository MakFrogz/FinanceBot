import sqlite3

import db
import bill
import user
import group

debtors = {}


# def calc_debs(user_id, users_id):
#     bill.show_data(user_id)
#     amount = round(bill.get_data(user_id, 'amount') / len(users_id), 2)
#     bill.insert_payment(user_id)
#     for _id in users_id:
#         if not _id == user_id:
#             data = db.select_debts(_id, user_id)
#             p_amount = amount
#             if data:
#                 for debt in data:
#                     if p_amount >= debt[1]:
#                         db.update_debt(0, debt[0], user_id)
#                         p_amount -= debt[1]
#                     else:
#                         db.update_debt(debt[1] - p_amount, debt[0], user_id)
#                         p_amount = 0
#                         db.insert_debt(bill.get_data(user_id, 'payment_id'), _id, p_amount)
#                         break
#                 if p_amount > 0:
#                     db.insert_debt(bill.get_data(user_id, 'payment_id'), _id, p_amount)
#             else:
#                 db.insert_debt(bill.get_data(user_id, 'payment_id'), _id, amount)

def calc_debs(user_id, status):
    group_id = user.get_current_group(user_id)
    if status:
        members = group.get_members_by_group_id(group_id)
        debt_amount = round(bill.get_data(user_id, 'amount') / len(members), 2)
    else:
        members = bill.get_selected(user_id)
        debt_amount = round(bill.get_data(user_id, 'amount') / (len(members) + 1), 2)
    for _id in members:
        if not _id == user_id:
            data = db.select_debts(_id, user_id)
            if data:
                if data[0] >= debt_amount:
                    db.update_debt(-debt_amount, _id - user_id)
                else:
                    db.update_debt(-data[0], _id - user_id)
                    db.insert_debt(user_id - _id, user_id, debt_amount - data[0], _id)
            else:
                db.insert_debt(user_id - _id, user_id, debt_amount, _id)
            db.insert_debt_to_history_debt(bill.get_data(user_id, 'payment_id'), _id, debt_amount)
    bill.insert_payment(user_id)


def get_debtors_for_keyboard(user_id):
    data = db.select_debtors_for_keyboard(user_id)
    return list(map(lambda x: x[0], data))


def add_debtor(user_id, debtor_id):
    debtors[user_id] = debtor_id


def get_debtor(user_id):
    return debtors[user_id]


def refund(user_id, amount):
    debtor_id = get_debtor(user_id)
    debt_amount = db.select_debts(user_id, debtor_id)[0]
    if debt_amount - amount >= 0:
        msg = 'Возврат подтвержден!'
    else:
        msg = 'Вы ввели сумму больше, чем Вам должны, но я взял нужную сумму, не беспокойтесь :)'
        amount = debt_amount
    create_refund_bill(user_id, amount, debtor_id)
    db.update_debt(-amount, user_id - debtor_id)
    db.insert_debt_to_history_debt(bill.get_data(user_id, 'payment_id'), debtor_id, - amount)
    return msg


def create_refund_bill(user_id, amount, debtor_id):
    bill.create_bill(user_id)
    bill.put_data(user_id, 'description', user.get_user_fullname(debtor_id) + '-->' + user.get_user_fullname(user_id))
    bill.put_data(user_id, 'amount', amount)
    bill.insert_payment(user_id)


def update_debt(user_id, amount, payment_id):
    data = db.select_debtors_by_payment_id(payment_id)
    users = list(map(lambda d: d[0], data))
    old_debt_amount = data[0][1]
    new_debt_amount = round(amount / (len(users) + 1), 2)
    res = new_debt_amount - old_debt_amount
    for _id in users:
        debt_data = db.select_debts(user_id, _id)[0]
        if debt_data + res >= 0:
            db.update_debt(res, user_id - _id)
        else:
            db.update_debt(-debt_data, user_id - _id)
            db.insert_debt(_id - user_id, _id, (debt_data + res) * -1, user_id)
    db.update_history_debt(new_debt_amount, payment_id)


def get_debtors(user_id):
    debtors = db.select_debtors(user_id)
    msg = ''
    for debtor in debtors:
        msg = msg + debtor[0] + ' ' + debtor[1] + '--->' + str(debtor[2]) + '\n'
    return msg


def get_debts(user_id):
    debts = db.select_user_debts(user_id)
    msg = ''
    for d in debts:
        msg = msg + d[0] + ' ' + d[1] + '<---' + str(d[2]) + '\n'
    return msg


def get_alert(users_id, message):
    amount = round(bill.get_data(message.from_user.id, 'amount') / len(users_id), 2)
    return message.from_user.first_name + ' ' + message.from_user.last_name + ' заплатил за тебя сумму ' + str(amount) + '('  + bill.get_data(message.from_user.id, 'description') + ')'