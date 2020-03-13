import telebot
import group


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
    markup.row('Выйти из группы')
    return markup


def get_bills_control_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Внести чек')
    markup.row('Просмотреть чеки')
    return markup


def get_pay_control_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Выбрать людей из списка')
    markup.row('Заплатить за всех')
    return markup


def get_existing_group_keyboard(user_id):
    markup = telebot.types.InlineKeyboardMarkup()
    groups = group.get_groups_by_user_id(user_id)
    if groups:
        for gr in groups:
            btn = telebot.types.InlineKeyboardButton(text=gr.get_group(), callback_data=gr.get_group())
            markup.row(btn)
        msg = 'Выберите группу из списка'
        return [msg, markup]
    else:
        msg = 'Список пустой :('
        return [msg, get_create_and_connection_keyboard()]
