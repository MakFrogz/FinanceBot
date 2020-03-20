import db

user_dict = {}


def insert_user(user_id: int, first_name: str, last_name: str):
    if not check_user_existing(user_id):
        db.insert_user(user_id, first_name, last_name)
        user_dict[user_id] = {'first_name': first_name, 'last_name': last_name, 'current_group': ''}


def check_user_online(user_id):
    try:
        return user_dict[user_id]['current_group']
    except KeyError:
        return False


def check_user_existing(user_id):
    return user_id in user_dict


def set_group(user_id, group_id):
    user_dict[user_id]['current_group'] = group_id
    print(user_dict)


def get_current_group(user_id):
    return user_dict[user_id]['current_group']


def get_user_fullname(user_id):
    return user_dict[user_id]['first_name'] + ' ' + user_dict[user_id]['last_name']


def get_data_from_db():
    data = db.select_users()
    global user_dict
    user_dict = {user[0]: {'first_name': user[1], 'last_name': user[2], 'current_group': user[3]} for user in data}


get_data_from_db()