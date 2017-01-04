from user import User #imports user.py and the 'user' class

def authenticate( username , password ):
    user = User.find_by_username(username) #Use method to retrieve from DB instead of mapping
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
