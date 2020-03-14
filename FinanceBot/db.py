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
        sql = 'INSERT INTO groups(group_id, user_id, online) VALUES (?,?,?)'
        cursor.execute(sql, args)
        conn.commit()


def insert_payment(*args):
    with conn:
        sql = 'INSERT INTO payment(payment_id, user_id, group_id, description, amount, date) VALUES (?,?,?,?,?,?)'
        cursor.execute(sql, args)
        conn.commit()


def insert_debt(*args):
    with conn:
        sql = 'INSERT INTO debt(payment_id, user_id, amount) VALUES (?,?,?)'
        cursor.execute(sql, args)
        conn.commit()


def select_users_id():
    with conn:
        sql = 'SELECT user_id, first_name, last_name FROM user'
        return cursor.execute(sql).fetchall()


def select_groups():
    with conn:
        sql = 'SELECT group_id, user_id, online FROM groups'
        return cursor.execute(sql).fetchall()


def select_bills():
    with conn:
        sql = 'SELECT payment_id, user_id, group_id, description, amount, date FROM payment'
        return cursor.execute(sql)


def select_debts(*args):
    with conn:
        sql = 'SELECT debt.payment_id, debt.amount FROM debt INNER JOIN payment ON payment.payment_id = debt.payment_id WHERE payment.user_id = ? AND debt.user_id = ?'
        return cursor.execute(sql, args).fetchall()


def select_debtors(*args):
    with conn:
        sql = 'SELECT debt.user_id FROM debt INNER JOIN payment ON debt.payment_id = payment.payment_id WHERE payment.user_id = ? GROUP BY debt.user_id'
        return cursor.execute(sql, args).fetchall()


def update_user_online(*args):
    with conn:
        sql = 'UPDATE groups SET online = ? WHERE group_id = ? AND user_id = ?'
        cursor.execute(sql, args)
        conn.commit()


def update_debt(*args):
    with conn:
        sql = 'UPDATE debt SET amount = ? WHERE payment_id = ? AND user_id = ?'
        cursor.execute(sql, args)
        conn.commit()