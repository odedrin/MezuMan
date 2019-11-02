import pymongo 
import backend
from backend.connect_data import database

#define variable for 'debts' collection
debts = database['Debts']


class Debts():
    #creates list of all debts
    @staticmethod
    def make_list():
        debts_list = []
        for debt in debts.find():
            debts_list.append(debt)
        return debts_list
#creates new debt, when left user is initially the creditor.
#positive balance signifies left user is creditor. negitive signifies right is creditor.
# returns debt id
    @staticmethod
    def add(left_user, right_user, balance):
        new_debt = {'left': left_user, 'right': right_user, 'balance': balance}
        debt = debts.insert_one(new_debt)
        return debt.inserted_id

#finds a debt between user1 and user2.
# if exists returns the debt's _id, if not, returns False.
    @staticmethod
    def find(user1, user2):
        for debt in debts.find():
            if debt['left'] != user1 and debt['right'] != user1:
                continue
            if debt['left'] == user2 or debt['right'] == user2:
                return debt['_id']
        return None

#updates debt betwen 2 users. if no such debt, a new debt is created.
#returns debt DB id.
    @staticmethod
    def edit(creditor, debtor, balance):
        debt_id = Debts.find(creditor, debtor)
        if debt_id:
            debt = debts.find_one({'_id': debt_id})
            if debt['right'] == creditor:
                balance = -balance
            new_balance = debt['balance'] + balance
            debts.update_one({'_id': debt_id}, {'$set':{'balance' : new_balance}})
            return debt_id
        else:
            return Debts.add(creditor, debtor, balance)
