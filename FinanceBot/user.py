import db

user_list = []


class User:
    __user_id: int
    __first_name: str
    __last_name: str

    def __init__(self, user_id, first_name, last_name):
        self.__user_id = user_id
        self.__first_name = first_name
        self.__last_name = last_name

    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name


def insert_user(user_id: int, first_name: str, last_name: str):
    if not check_user_existing(user_id):
        db.insert_user(user_id, first_name, last_name)
        user_list.append(User(user_id, first_name, last_name))


def check_user_existing(user_id):
    if [user for user in user_list if user.get_user_id() == user_id]:
        return True
    return False


def ger_user_obj(user_id):
    obj = [user for user in user_list if user.get_user_id() == user_id]
    if obj:
        return obj[0]
    return None


def get_data():
    data = db.select_users_id()
    for user in data:
        user_list.append(User(user[0], user[1], user[2]))


get_data()