import pymongo 
import backend
from backend.connect_data import database

userscl = database['Users']

class DuplicateError(Exception):
    pass


#If exists returns user id, if not- returns None.
def user_exists(name):
    user = userscl.find_one({'name' : name}) 
    if user != None:
        return user['_id']

#Following funtions: if successful- returns True.
def add_user_document(name):
    if len(name.strip()) > 1 and len(name.strip()) < 21:
        if user_exists(name):
            print("this username already exists, choose another name")
            raise DuplicateError
        new_user = {'name' : name, 'balance' : 0, 'groups' : [], 'user history' : []}
        userscl.insert_one(new_user)
        return True
    print("invalid name inserted")
    return False

    
#key='name' or 'balance' 
def edit_user(name, key, new_value): 
    userscl.update({'name': name}, {"$set":{key : new_value}})
    return True

def push_group_to_user(username, groupname):
    try:
        userscl.update({'name':username}, {'$push': {'groups': groupname}})
        return True
    except:
        return False

def remove_group_from_user(username, groupname):
    try:
        userscl.update({'name':username}, {'$pull': {'groups': groupname}})
        return True
    except:
        return False