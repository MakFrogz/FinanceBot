import telebot
import config
import keyboard
import group
import user
import bill

bot = telebot.TeleBot(config.toker)


@bot.message_handler(commands=['start'])
def call_start(message):
    if group.check_online_group(message.from_user.id):
        bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=keyboard.get_main_keyboard())
    else:
        bot.send_message(message.from_user.id, 'Выберите пункт меню:',
                         reply_markup=keyboard.get_create_and_connection_keyboard())
    user.insert_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)


@bot.message_handler(func=lambda message: message.text == 'Создать группу')
def call_create_group(message):
    bot.send_message(message.from_user.id, 'Введите название группы', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, process_create_group)


def process_create_group(message):
    if not group.check_group_existing(message.text):
        group.create_group(message.text, message.from_user.id, True)
        bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=keyboard.get_main_keyboard())
    else:
        bot.send_message(message.from_user.id, 'Такая группа уже существует. Попробуйте ещё раз!')
        bot.register_next_step_handler(message, process_create_group)


@bot.message_handler(func=lambda message: message.text == 'Присоединиться к существующей')
def call_connect_to_existing_group(message):
    answer = keyboard.get_existing_group_keyboard(message.from_user.id)
    bot.send_message(message.from_user.id, answer[0], reply_markup=answer[1])


@bot.callback_query_handler(func=lambda call: group.check_group_existing(call.data))
def callback_connect_to_existing_group(call):
    group.update_user_online(call.from_user.id, call.data, True)
    bot.send_message(call.from_user.id, 'Выберите пункт меню:', reply_markup=keyboard.get_main_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Присоединиться к новой')
def call_connect_to_new_group(message):
    bot.send_message(message.from_user.id, 'Введите название группы', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, process_connect_to_new_group)


def process_connect_to_new_group(message):
    if group.check_group_existing(message.text):
        if group.check_existing_member_in_group(message.from_user.id, message.text):
            group.update_user_online(message.from_user.id, message.text, True)
        else:
            group.create_group(message.text, message.from_user.id, True)
    else:
        bot.send_message(message.from_user.id, 'Такой группы не существует!', reply_markup=keyboard.get_create_and_connection_keyboard())


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


@bot.message_handler(func=lambda message: message.text == 'Заплатить за всех')
def call_pay_for_all(message):
    current_group = group.get_current_group(message.from_user.id)
    users = group.get_members_by_group_id(current_group)


@bot.message_handler(func=lambda message: message.text == 'Выйти из группы')
def call_leave_group(message):
    current_group = group.get_current_group(message.from_user.id)
    group.update_user_online(message.from_user.id, current_group, False)
    bot.send_message(message.from_user.id, 'Выберите пункт меню:',
                     reply_markup=keyboard.get_create_and_connection_keyboard())


if __name__ == '__main__':
    bot.polling(none_stop=True)
