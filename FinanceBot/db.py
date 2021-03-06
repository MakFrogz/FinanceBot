import sqlite3
import config

conn = sqlite3.connect(config.db_name, check_same_thread=False)
cursor = conn.cursor()


def insert_user(*args):
    with conn:
        sql = 'INSERT INTO user(user_id, first_name, last_name) VALUES (?,?,?)'
        cursor.execute(sql, args)
        conn.commit()


def insert_group(*args):
    with conn:
        sql = 'INSERT INTO groups(group_id, password) VALUES (?,?)'
        cursor.execute(sql, args)
        conn.commit()


def insert_to_history_group(*args):
    with conn:
        sql = 'INSERT INTO history_groups(group_id, user_id, online) VALUES (?,?,?)'
        cursor.execute(sql, args)
        conn.commit()


def insert_payment(*args):
    with conn:
        sql = 'INSERT INTO payment(payment_id, user_id, group_id, description, amount, date) VALUES (?,?,?,?,?,?)'
        cursor.execute(sql, args)
        conn.commit()


def insert_debt(*args):
    try:
        with conn:
            sql = 'INSERT INTO debt(debt_id, user_id, amount, debtor_id) VALUES (?,?,?,?)'
            cursor.execute(sql, args)
            conn.commit()
    except sqlite3.IntegrityError:
        update_debt(args[2], args[0])


def insert_debt_to_history_debt(*args):
    with conn:
        sql = 'INSERT INTO history_debt(payment_id, user_id, amount) VALUES (?,?,?)'
        cursor.execute(sql, args)
        conn.commit()


def select_users():
    with conn:
        sql = 'SELECT u.user_id, u.first_name, u.last_name, h.group_id FROM user u LEFT JOIN history_groups h ON u.user_id = h.user_id AND h.online = 1'
        return cursor.execute(sql).fetchall()


def select_groups():
    with conn:
        sql = 'SELECT h.group_id, g.password, h.user_id, h.online FROM groups g INNER JOIN history_groups h ON g.group_id = h.group_id'
        return cursor.execute(sql).fetchall()


def select_bills(*args):
    with conn:
        sql = 'SELECT  user_id, description, amount, date FROM payment WHERE group_id = ? ORDER BY date DESC LIMIT 5'
        return cursor.execute(sql, args).fetchall()


def select_debts(*args):
    with conn:
        sql = 'SELECT amount FROM debt WHERE user_id = ? AND debtor_id = ?'
        return cursor.execute(sql, args).fetchone()


def select_debtors_for_keyboard(*args):
    with conn:
        sql = 'SELECT h.user_id FROM history_debt h INNER JOIN payment p ON h.payment_id = p.payment_id WHERE ' \
              'p.user_id = ? GROUP BY h.user_id '
        return cursor.execute(sql, args).fetchall()


def select_debtors(*args):
    with conn:
        sql = 'SELECT debtor_id, amount FROM debt WHERE user_id = ?'
        return cursor.execute(sql, args).fetchall()


def select_user_debts(*args):
    with conn:
        sql = 'SELECT user_id, amount FROM debt WHERE debtor_id = ?'
        return cursor.execute(sql, args).fetchall()


def select_debtors_by_payment_id(*args):
    with conn:
        sql = 'SELECT user_id, amount FROM history_debt WHERE payment_id = ?'
        return cursor.execute(sql, args).fetchall()


def select_payments_by_user_id_and_group_id(*args):
    with conn:
        sql = 'SELECT description, payment_id FROM payment WHERE user_id = ? AND group_id = ?'
        return cursor.execute(sql, args).fetchall()


def select_bill_amount(*args):
    with conn:
        sql = 'SELECT amount FROM payment WHERE payment_id = ?'
        return cursor.execute(sql, args).fetchone()


def select_sum_history_debts(*args):
    with conn:
        sql = 'SELECT SUM(h.amount) FROM history_debt h INNER JOIN payment p ON h.payment_id = p.payment_id WHERE p.user_id = ? AND h.user_id = ?'
        data = cursor.execute(sql, args).fetchone()
        if data[0]:
            return data[0]
        else:
            return 0


def update_user_online(*args):
    with conn:
        sql = 'UPDATE history_groups SET online = ? WHERE group_id = ? AND user_id = ?'
        cursor.execute(sql, args)
        conn.commit()


def update_debt(*args):
    with conn:
        sql = 'UPDATE debt SET amount = amount + ? WHERE debt_id = ?'
        cursor.execute(sql, args)
        conn.commit()


def e_update_debt(*args):
    with conn:
        sql = 'UPDATE debt SET amount = ? WHERE debt_id = ?'
        cursor.execute(sql, args)
        conn.commit()


def update_bill_description(*args):
    with conn:
        sql = 'UPDATE payment SET description = ? WHERE payment_id = ?'
        cursor.execute(sql, args)
        conn.commit()


def update_bill_amount(*args):
    with conn:
        sql = 'UPDATE payment SET amount = ? WHERE payment_id = ?'
        cursor.execute(sql, args)
        conn.commit()


def update_history_debt(*args):
    with conn:
        if check_existing_history_debt(args[0], args[1]):
            sql = 'UPDATE history_debt SET amount = ? WHERE payment_id = ?'
            cursor.execute(sql, (args[2], args[0]))
            conn.commit()
        else:
            insert_debt_to_history_debt(*args)


def check_existing_history_debt(*args):
    with conn:
        sql = 'SELECT EXISTS(SELECT payment_id, user_id FROM history_debt WHERE payment_id = ? AND user_id = ?)'
        print(cursor.execute(sql, args).fetchone())
        return cursor.execute(sql, args).fetchone()[0]