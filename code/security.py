from user import User #imports user.py and the 'user' class

users = [
    User(1 , 'bob' , 'asdf')
]

#The dictionaries below help us not iterating every time we authenticate.
username_mapping = { u.username: u for u in users} #points a username to the name dictionary for each name
userid_mapping = { u.id: u for u in users }

def authenticate( username , password ):
    user = username_mapping.get(username , None) #If you can't ind it, return None.
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get( user_id , None )
