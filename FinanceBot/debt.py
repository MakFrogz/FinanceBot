import db
import bill
import user
import group
import alert

debtors = {}


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
        alert.send_debt_msg(user_id, _id, bill.get_data(user_id, 'description'), debt_amount)
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
    alert.send_approve_refund(user_id, debtor_id, amount)
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
        db.update_history_debt(payment_id, _id, new_debt_amount)


def recalc_debts(user_id):
    payment_id = bill.get_data(user_id, 'edit_payment_id')
    bill_amount = db.select_bill_amount(payment_id)[0]
    selected = bill.get_selected(user_id)
    debt_amount = round(bill_amount / (len(selected) + 1), 2)
    for _id in selected:
        db.update_history_debt(payment_id, _id, debt_amount)
        d_amount = db.select_sum_history_debts(user_id, _id)
        m_amount = db.select_sum_history_debts(_id, user_id)
        if m_amount - d_amount > 0:
            db.e_update_debt(m_amount - d_amount, _id - user_id)
        else:
            db.e_update_debt(d_amount - m_amount, user_id - _id)


def get_debtors(user_id):
    debtor_list = db.select_debtors(user_id)
    msg = ''
    for debtor in debtor_list:
        msg = msg + 'Должник:' + user.get_user_fullname(debtor[0]) + '\n' \
                    'Сумма:' + str(debtor[1]) + '\n\n'
    return msg


def get_debts(user_id):
    debts = db.select_user_debts(user_id)
    msg = ''
    for d in debts:
        msg = msg + 'Имя:' + user.get_user_fullname(d[0]) + '\n' \
                    'Сумма:' + str(d[1]) + '\n\n'
    return msg
