from models.user import UserModel #imports user.py and the 'user' class

def authenticate( username , password ):
    user = UserModel.find_by_username(username) #Use method to retrieve from DB instead of mapping
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
