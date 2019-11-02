import pymongo 
import backend
from backend.connect_data import database
from backend.debts import Debts


#define variable for 'users' collection 
users = database['Users']

class DuplicateError(Exception):
    pass

class Users():
    @staticmethod
    #make list of all users
    def make_list():
        users_list = []
        for user in users.find():
            users_list.append(user)
        return users_list

    #check if user exsits
    @staticmethod
    def user_exists(name):
        user = users.find_one({'name' : name}) 
        if user != None:
            return True
        return False

    #creates group document in DB and make sure there is no other group with the same name
    @staticmethod
    def add(name):
        if Users.user_exists(name):
            raise DuplicateError
        new_user = {'name' : name, 'balance' : 0, 'groups' : []}
        try:
            users.insert_one(new_user)
            return True
        except:
            return False
        
    #edit user's balance
    @staticmethod
    def edit_balance(name, new_value): 
        try:
            users.update({'name': name}, {'$set':{'balance' : new_value}})
            return True
        except:
            return False

    #adds group to user's groups list in DB (nested array)
    @staticmethod
    def add_group(username, groupname):
        try:
            users.update({'name':username}, {'$push': {'groups': groupname}})
            return True
        except:
            return False

    #removes group from user's groups list in DB (nested array)
    @staticmethod
    def remove_group(username, groupname):
        users.update({'name':username}, {'$pull': {'groups': groupname}})
        return True

    #update users's balances and edit debt accordingly.
    @staticmethod
    def transaction(debtorname, creditorname, amount):
        debtor = users.find_one({'name': debtorname})
        debtor_balance = debtor['balance'] - amount
        Users.edit_balance(debtorname, debtor_balance)
        creditor = users.find_one({'name': creditorname})
        creditor_balance = creditor['balance'] + amount
        Users.edit_balance(creditorname, creditor_balance)
        Debts.edit(creditorname, debtorname, amount)
        return True

