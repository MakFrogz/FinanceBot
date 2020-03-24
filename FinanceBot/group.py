import db
import user

groups_dict = {}
temp = {}


def set_temp(user_id, key, group_id):
    if user_id in temp:
        temp[user_id][key] = group_id
    else:
        temp[user_id] = {}
        temp[user_id][key] = group_id


def create_group(user_id):
    group_id = temp[user_id]['group_id']
    password = temp[user_id]['password']
    db.insert_group(group_id, password)
    db.insert_to_history_group(group_id, user_id, True)
    user.set_group(user_id, group_id)
    groups_dict[group_id] = {'password': password, 'members': [user_id]}


def insert_member_to_group(user_id):
    db.insert_to_history_group(temp[user_id]['connect_group'], user_id, True)
    add_new_member_to_group(user_id)


def add_new_member_to_group(user_id):
    group_id = temp[user_id]['connect_group']
    user.set_group(user_id, group_id)
    groups_dict[group_id]['members'].append(user_id)
    print(groups_dict)


def check_group_existing(group_id):
    return group_id in groups_dict


def check_existing_member_in_group(user_id, group_id):
    return user_id in groups_dict[group_id]['members']


def check_group_password(user_id, password):
    key = temp[user_id]['connect_group']
    return groups_dict[key]['password'] == password


def get_groups_by_user_id(user_id):
    return [key for key in groups_dict.keys() if user_id in groups_dict[key]['members']]


def update_user_online(user_id, group_id, online):
    if group_id:
        user.set_group(user_id, group_id)
        db.update_user_online(online, group_id, user_id)
    else:
        group_id = user.get_current_group(user_id)
        db.update_user_online(online, group_id, user_id)
        user.set_group(user_id, None)


def get_members_by_group_id(group_id):
    return groups_dict[group_id]['members']


def get_group_info(user_id):
    group_id = user.get_current_group(user_id)
    data = groups_dict[group_id]
    msg = 'Группа:' + group_id + '\n' \
          'Пароль:' + data['password'] + '\n' \
          'Участники: \n'
    for member in data['members']:
        msg = msg + user.get_user_fullname(member) + '\n'
    return msg


def get_data_from_db():
    data = db.select_groups()
    global groups_dict
    groups_dict = {group[0]: {'password': '', 'members': []} for group in data}
    for group_id, password, user_id, online in data:
        groups_dict[group_id]['password'] = password
        groups_dict[group_id]['members'].append(user_id)


get_data_from_db()
