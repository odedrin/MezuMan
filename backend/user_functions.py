import pymongo 
import backend
from backend.connect_data import database

#define variable for 'users' collection 
userscl = database['Users']

class DuplicateError(Exception):
    pass

#If exists returns user id, if not- returns None.
def user_exists(name):
    user = userscl.find_one({'name' : name}) 
    if user != None:
        return user['_id']

#Following funtions: if successful- returns True.

#creates group document in DB and make sure there is no other group with the same name
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

    
#key='name' or 'balance' to decide what to update
def edit_user(name, key, new_value): 
    userscl.update({'name': name}, {"$set":{key : new_value}})
    return True

#adds group to user's groups list in DB (nested array)
def push_group_to_user(username, groupname):
    try:
        userscl.update({'name':username}, {'$push': {'groups': groupname}})
        return True
    except:
        return False

#removes group from user's groups list in DB (nested array)
def remove_group_from_user(username, groupname):
    try:
        userscl.update({'name':username}, {'$pull': {'groups': groupname}})
        return True
    except:
        return False

def transaction(debtorname, creditorname, amount):
    debtor = userscl.find_one({'name': debtorname})
    debtor_balance = debtor['balance'] - amount
    edit_user(debtorname, "balance", debtor_balance)
    creditor = userscl.find_one({'name': creditorname})
    creditor_balance = creditor['balance'] + amount
    edit_user(creditorname, "balance", creditor_balance)
    return True

