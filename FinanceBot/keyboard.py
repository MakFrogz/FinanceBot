import telebot
import group
import user
import bill

def get_create_and_connection_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Создать группу')
    markup.row('Присоединиться к существующей')
    markup.row('Присоединиться к новой')
    return markup


def get_main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Чеки')
    markup.row('Задолженности')
    markup.row('Инф. о группе')
    markup.row('Выйти из группы')
    return markup


def get_bills_control_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Внести чек')
    markup.row('Просмотреть чеки')
    markup.row('Редактировать чеки')
    markup.row('Назад')
    return markup


def get_debts_control_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Мои долги')
    markup.row('Мои должники')
    markup.row('Подтвердить возврат средств')
    markup.row('Назад')
    return markup


def get_pay_control_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Выбрать людей из списка')
    markup.row('Заплатить за всех')
    return markup


def get_edit_bill_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Редактировать описание')
    markup.row('Редактировать сумму')
    markup.row('Редактировать список людей')
    markup.row('Назад')
    return markup

def get_existing_group_keyboard(user_id):
    markup = telebot.types.InlineKeyboardMarkup()
    groups = group.get_groups_by_user_id(user_id)
    if groups:
        for group_id in groups:
            btn = telebot.types.InlineKeyboardButton(text=group_id, callback_data='g_' + group_id)
            markup.row(btn)
        msg = 'Выберите группу из списка'
        return [msg, markup]
    else:
        msg = 'Список пустой :('
        return [msg, get_create_and_connection_keyboard()]


def get_bills_for_edit_keyboard(user_id):
    markup = telebot.types.InlineKeyboardMarkup()
    bills = bill.get_bills_for_edit(user_id)
    if bills:
        for b in bills:
            btn = telebot.types.InlineKeyboardButton(text=b[0], callback_data='eb_' + b[1])
            markup.row(btn)
        return ['Выберите чек для редактирования:', markup]
    else:
        return ['У Вас нет чеков для редактирования!', get_bills_control_keyboard()]


def get_users_keyboard(user_id, pref):
    markup = telebot.types.InlineKeyboardMarkup()
    group_id = user.get_current_group(user_id)
    users_id = group.get_members_by_group_id(group_id)
    for _id in users_id:
        if not _id == user_id:
            btn = telebot.types.InlineKeyboardButton(text=user.get_user_fullname(_id), callback_data=pref + str(_id))
            markup.row(btn)
    return markup


def get_r_users_keyboard(users_id):
    markup = telebot.types.InlineKeyboardMarkup()
    for _id in users_id:
        btn = telebot.types.InlineKeyboardButton(text=user.get_user_fullname(_id), callback_data='r_' + str(_id))
        markup.row(btn)
    return markup


def get_new_markup(old_markup, callback, pref):
    new_markup = old_markup
    for i in new_markup['inline_keyboard']:
        if i[0]['callback_data'] == callback:
            new_markup['inline_keyboard'].remove(i)
            break
    new_markup['inline_keyboard'].append([{'text': 'Подтвердить', 'callback_data': pref + 'apply'}, {'text': 'Отменить', 'callback_data': pref + 'cancel'}])
    return str(new_markup).replace('\'', '"')