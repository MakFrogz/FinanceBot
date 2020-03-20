import telebot
import config
import keyboard
import group
import user
import bill
import debt

bot = telebot.TeleBot(config.toker)


@bot.message_handler(commands=['start'])
def call_start(message):
    if user.check_user_online(message.from_user.id):
        bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=keyboard.get_main_keyboard())
    else:
        bot.send_message(message.from_user.id, 'Выберите пункт меню:',
                         reply_markup=keyboard.get_create_and_connection_keyboard())
    user.insert_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)


@bot.message_handler(func=lambda message: message.text == 'Создать группу')
def call_create_group(message):
    bot.send_message(message.from_user.id, 'Введите название группы', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, process_group_name)


def process_group_name(message):
    if not group.check_group_existing(message.text):
        group.set_temp(message.from_user.id,'group_id', message.text)
        bot.send_message(message.from_user.id, 'Введите пароль для группы:')
        bot.register_next_step_handler(message, process_group_password)
    else:
        bot.send_message(message.from_user.id, 'Такая группа уже существует. Попробуйте ещё раз!')
        bot.register_next_step_handler(message, process_group_name)


def process_group_password(message):
    group.set_temp(message.from_user.id, 'password', message.text)
    group.create_group(message.from_user.id)
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=keyboard.get_main_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Присоединиться к существующей')
def call_connect_to_existing_group(message):
    answer = keyboard.get_existing_group_keyboard(message.from_user.id)
    bot.send_message(message.from_user.id, answer[0], reply_markup=answer[1])


@bot.callback_query_handler(func=lambda call: call.data.startswith('g_'))
def callback_connect_to_existing_group(call):
    group.update_user_online(call.from_user.id, call.data[2:], True)
    bot.send_message(call.from_user.id, 'Выберите пункт меню:', reply_markup=keyboard.get_main_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Присоединиться к новой')
def call_connect_to_new_group(message):
    bot.send_message(message.from_user.id, 'Введите название группы', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, process_connect_to_new_group)


def process_connect_to_new_group(message):
    if group.check_group_existing(message.text):
        group.set_temp(message.from_user.id, 'connect_group', message.text)
        bot.send_message(message.from_user.id, 'Введите пароль:')
        bot.register_next_step_handler(message, process_password_new_group)
    else:
        bot.send_message(message.from_user.id, 'Такой группы не существует!',
                         reply_markup=keyboard.get_create_and_connection_keyboard())


def process_password_new_group(message):
    if group.check_group_password(message.from_user.id, message.text):
        group.insert_member_to_group(message.from_user.id)
        bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=keyboard.get_main_keyboard())
    else:
        bot.send_message(message.from_user.id, 'Неверный пароль! Попробуйте ещё раз!')
        bot.register_next_step_handler(message, process_password_new_group)


@bot.message_handler(func=lambda message: message.text == 'Чеки')
def call_bills(message):
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=keyboard.get_bills_control_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Внести чек')
def call_insert_bill(message):
    bot.send_message(message.from_user.id, 'Что Вы оплатили?', reply_markup=telebot.types.ReplyKeyboardRemove())
    bill.create_bill(message.from_user.id)
    bot.register_next_step_handler(message, process_pay_for)


def process_pay_for(message):
    bill.put_data(message.from_user.id, 'description', message.text)
    bot.send_message(message.from_user.id, 'Сколько Вы заплатили?')
    bot.register_next_step_handler(message, process_amount)


def process_amount(message):
    try:
        amount = round(float(message.text.replace(',', '.')), 2)
        bill.put_data(message.from_user.id, 'amount', amount)
        bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=keyboard.get_pay_control_keyboard())
    except ValueError:
        bot.send_message(message.from_user.id, 'Вы ввели некорректную сумму!Попробуйте ещё раз!')
        bot.register_next_step_handler(message, process_amount)


@bot.message_handler(func=lambda message: message.text == 'Выбрать людей из списка')
def call_select_users(message):
    bot.send_message(message.from_user.id, 'Выберите людей из списка:', reply_markup=keyboard.get_users_keyboard(message.from_user.id))


@bot.callback_query_handler(func=lambda call: call.data.startswith('p_'))
def callback_select_users(call):
    # bill.put_data(call.from_user.id, 'selected', int(call.data[2:]))
    bill.set_selected(call.from_user.id, int(call.data[2:]))
    markup = keyboard.get_new_markup(call.message.json['reply_markup'], call.data)
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'apply')
def callback_apply(call):
    debt.calc_debs(call.from_user.id, False)
    # alert = debt.get_alert(users, call)
    # for u in users:
    #     if not u == call.from_user.id:
    #         bot.send_message(u, alert)
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, 'Чек внесён!', reply_markup=keyboard.get_bills_control_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def callback_cancel(call):
    # bill.clear_data(call.from_user.id, 'selected')
    bill.clear_selected(call.from_user.id)
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=keyboard.get_users_keyboard(call.from_user.id))


@bot.message_handler(func=lambda message: message.text == 'Заплатить за всех')
def call_pay_for_all(message):
    debt.calc_debs(message.from_user.id, True)
    # alert = debt.get_alert(users, message)
    # for u in users:
    #     if not u == message.from_user.id:
    #         bot.send_message(u,alert)
    bot.send_message(message.from_user.id, 'Чек внесён!', reply_markup=keyboard.get_bills_control_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Просмотреть чеки')
def call_show_bills(message):
    try:
        msg = bill.get_bills_msg(message.from_user.id)
        bot.send_message(message.from_user.id, msg)
    except telebot.apihelper.ApiException:
        bot.send_message(message.from_user.id, 'Список чеков пуст!')


@bot.message_handler(func=lambda message: message.text == 'Редактировать чеки')
def call_edit_bills(message):
    data = keyboard.get_bills_for_edit_keyboard(message.from_user.id)
    bot.send_message(message.from_user.id, data[0], reply_markup=data[1])


@bot.callback_query_handler(func=lambda call: call.data.startswith('eb_'))
def callback_edit_bills(call):
    pass


@bot.message_handler(func=lambda message: message.text == 'Задолженности')
def call_debts(message):
    bot.send_message(message.from_user.id, 'Выберите пунк меню:', reply_markup=keyboard.get_debts_control_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Мои должники')
def call_my_debtors(message):
    try:
        msg = debt.get_debtors(message.from_user.id)
        bot.send_message(message.from_user.id, msg)
    except telebot.apihelper.ApiException:
        bot.send_message(message.from_user.id, 'У Вас нет должников!')


@bot.message_handler(func=lambda message: message.text == 'Мои долги')
def call_my_debts(message):
    try:
        msg = debt.get_debts(message.from_user.id)
        bot.send_message(message.from_user.id, msg)
    except telebot.apihelper.ApiException:
        bot.send_message(message.from_user.id, 'У Вас нет долгов!')


@bot.message_handler(func=lambda message: message.text == 'Подтвердить возврат средств')
def call_refund(message):
    bot.send_message(message.from_user.id, 'Выберите человека из списка:',
                     reply_markup=keyboard.get_r_users_keyboard(debt.get_debtors_for_keyboard(message.from_user.id)))


@bot.callback_query_handler(func=lambda call: call.data.startswith('r_'))
def callback_refund(call):
    debt.add_debtor(call.from_user.id, int(call.data[2:]))
    bot.send_message(call.from_user.id, 'Сколько Вам вернули?')
    bot.register_next_step_handler(call.message, process_refund)


def process_refund(message):
    try:
        msg = debt.refund(message.from_user.id, round(float(message.text.replace(',', '.')), 2))
        bot.send_message(message.from_user.id, msg, reply_markup=keyboard.get_debts_control_keyboard())
    except ValueError:
        bot.send_message(message.from_user.id, 'Вы ввели некорректную сумму!Попробуйте ещё раз!')
        bot.register_next_step_handler(message, process_refund)


@bot.message_handler(func=lambda message: message.text == 'Выйти из группы')
def call_leave_group(message):
    group.update_user_online(message.from_user.id, None, False)
    bot.send_message(message.from_user.id, 'Выберите пункт меню:',
                     reply_markup=keyboard.get_create_and_connection_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Назад')
def call_back(message):
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=keyboard.get_main_keyboard())


bot.enable_save_next_step_handlers(delay=2)


bot.load_next_step_handlers()


if __name__ == '__main__':
    bot.polling(none_stop=True)


