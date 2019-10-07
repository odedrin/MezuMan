import pymongo 
from app import database
userscl = database['Users']
groupscl = database['Groups']

#If exists returns group id, if not- returns None.
def group_exists(name):
    group = groupscl.find_one({'name' : name})
    if group != None:
        return group['_id']

#If exists returns user id, if not- returns None.
def user_exists(name):
    user = userscl.find_one({'name' : name}) 
    if user != None:
        return user['_id']

#Following funtions: if successful- returns True.
def add_user_document(name):
    if name.strip():
        if user_exists(name):
            print("this username already exists, choose another name")
            return False
        new_user = {'name' : name, 'balance' : 0, 'groups' : [], 'user history' : []}
        userscl.insert_one(new_user)
        return True
    print("invalid name inserted")
    return False

def add_group_document(name):
    if name.strip():
        if group_exists(name):
            print("this group's name already exists, choose another name")
            raise DuplicateError
        new_group = {'name' : name, 'members' : [], 'group history' : []}
        groupscl.insert_one(new_group)
        return True
    print("Name must have at least 2 characters")
    return False

def delete_user_document(name):
    if user_exists(name):
        userscl.delete_one({'name': name})
        return True
    else:
        return False

def delete_group_document(name):
    if group_exists(name):
        groupscl.delete_one({'name': name})
        return True
    else:
        return False

#key='name' or 'balance' 
def edit_user(name, key, new_value): 
    if user_exists('name'):
        userscl.update({'name': name}, {"$set":{key : new_value}})
        return True
    print("User does not exist")
    return False

#key = 'name'
def edit_group(name, key, new_value): 
    if group_exists('name'):
        groupscl.update({'name': name}, {"$set":{key : new_value}})
        return True
    print("group does not exist")
    return False 

def edit_user_groups(username, newgroups):
    if user_exists():
        user = userscl.find_one({'name':username})
        


