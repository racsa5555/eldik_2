def write_user_in_file(user_id):
    with open('users_ids.txt', 'a') as f:
        f.write(str(user_id))
        f.write(' ')

def get_users():
    users = set()
    with open('users_ids.txt', 'r') as f:
        data = f.read()
        for user_id in data.split():
            users.add(int(user_id))
    return users

