import db
import bill

debtors = {}


def calc_debs(user_id, users_id):
    bill.show_data(user_id)
    amount = round(bill.get_data(user_id, 'amount') / len(users_id), 2)
    bill.insert_payment(user_id)
    for _id in users_id:
        if not _id == user_id:
            data = db.select_debts(_id, user_id)
            p_amount = amount
            if data:
                for debt in data:
                    if p_amount >= debt[1]:
                        db.update_debt(0, debt[0], user_id)
                        p_amount -= debt[1]
                    else:
                        db.update_debt(debt[1] - p_amount, debt[0], user_id)
                        p_amount = 0
                        break
                if p_amount > 0:
                    db.insert_debt(bill.get_data(user_id, 'payment_id'), _id, p_amount)
            else:
                db.insert_debt(bill.get_data(user_id, 'payment_id'), _id, amount)


def get_debtors_for_keyboard(user_id):
    data = db.select_debtors_for_keyboard(user_id)
    return list(map(lambda x: x[0], data))


def add_debtor(user_id, debtor_id):
    debtors[user_id] = debtor_id


def get_debtor(user_id):
    return debtors[user_id]


def update_debts(user_id, amount):
    debtor_id = get_debtor(user_id)
    data = db.select_debts(user_id, debtor_id)
    r_amount = amount
    for debt in data:
        if r_amount >= debt[1]:
            db.update_debt(0, debt[0], debtor_id)
            r_amount -= debt[1]
        else:
            db.update_debt(debt[1] - r_amount, debt[0], debtor_id)
            break


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