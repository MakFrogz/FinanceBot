import telebot
import user

alert_bot = None


def set_bot(bot):
    global alert_bot
    alert_bot = bot


def send_debt_msg(user_id, debtor_id, description, amount):
    msg = 'Привет!\n' + \
          user.get_user_fullname(user_id) + ' заплатил за тебя:\n' + \
          'Оплачено:' + description + '\n' + \
          'Сумма:' + str(amount)
    alert_bot.send_message(debtor_id, msg)


def send_approve_refund(user_id, debtor_id, amount):
    msg = user.get_user_fullname(user_id) + 'подтвердил возврат средств на сумму ' + str(amount)
    alert_bot.send_message(debtor_id, msg)
