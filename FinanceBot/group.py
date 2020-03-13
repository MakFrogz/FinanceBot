import db
import user
group_list = []


class Group:

    def __init__(self, group_id, user_id, online):
        self.__group_id = group_id
        self.__user_id = user_id
        self.__online = online

    def get_group(self):
        return self.__group_id

    def get_user_id(self):
        return self.__user_id

    def get_online(self):
        return self.__online

    def set_online(self, online):
        self.__online = online


def create_group(group_id, user_id, online):
    group_list.append(Group(group_id, user_id, online))
    db.insert_group(group_id, user_id, online)


def check_online_group(user_id):
    if [group for group in group_list if group.get_user_id() == user_id and group.get_online()]:
        return True
    return False


def get_current_group(user_id):
    data = [group for group in group_list if group.get_user_id() == user_id and group.get_online()]
    if data:
        return data[0].get_group()
    return []


def check_group_existing(group_id):
    if [group for group in group_list if group.get_group() == group_id]:
        return True
    return False


def check_existing_member_in_group(user_id, group_id):
    if [group for group in group_list if group.get_user_id() == user_id and group.get_group() == group_id]:
        return True
    return False


def get_groups_by_user_id(user_id):
    return [group for group in group_list if group.get_user_id() == user_id]


def update_user_online(user_id, group_id, online):
    data = [group for group in group_list if group.get_user_id() == user_id and group.get_group() == group_id]
    if data:
        data[0].set_online(online)
        db.update_user_online(online,group_id, user_id)


def get_members_by_group_id(group_id):
    data = [group for group in group_list if group.get_group() == group_id]
    if data:
        l = []
        for obj in data:
            l.append(obj.get_user_id)
        return l
    return []


def get_data():
    data = db.select_groups()
    for group_id, user_id, online in data:
        group_list.append(Group(group_id, user_id, online))


get_data()
