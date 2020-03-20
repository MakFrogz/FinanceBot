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


def select_bills():
    with conn:
        sql = 'SELECT payment_id, user_id, group_id, description, amount, date FROM payment ORDER BY date DESC'
        return cursor.execute(sql)


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
        sql = 'SELECT user.first_name, user.last_name, SUM(debt.amount) FROM user INNER JOIN debt ON user.user_id = debt.user_id ' \
              'INNER JOIN payment ON debt.payment_id = payment.payment_id WHERE payment.user_id = ? AND debt.amount > 0 GROUP BY user.user_id'
        return cursor.execute(sql, args).fetchall()


def select_user_debts(*args):
    with conn:
        sql = 'SELECT user.first_name, user.last_name, SUM(debt.amount) FROM user INNER JOIN payment ON user.user_id = payment.user_id  ' \
                'INNER JOIN debt ON payment.payment_id = debt.payment_id WHERE debt.user_id = ? AND debt.amount > 0 GROUP BY user.user_id'
        return cursor.execute(sql, args).fetchall()


def select_debtors_by_payment_id(*args):
    with conn:
        sql = 'SELECT user_id FROM debt WHERE payment_id = ?'
        return cursor.execute(sql, args).fetchall()


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