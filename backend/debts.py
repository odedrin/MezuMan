import pymongo 
import backend
from backend.connect_data import database

#define variable for 'debts' collection
debts = database['Debts']


class Debts():
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

#check if user1 and user2 already have an existing debt, no matter the sides. 
# if so returns the debt's id in the DB, if not returns False.
    @staticmethod
    def find(user1, user2):
        for debt in debts.find():
            if debt['left'] != user1 and debt['right'] != user1:
                continue
            if debt['left'] == user2 or debt['right'] == user2:
                return debt['_id']
        return None

#if debt already exists between the users it is updated. if not a new debt is created.
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

#return string: '(debtor) owes (creditor) (balance)' or '(debtor) and (creditor) settled up'
    @staticmethod
    def show(debt_id):
        debt = debts.find_one({'_id': debt_id})
        balance = debt['balance']
        if balance == 0:
            result = '%s and %s are settled up' %(debt['left'], debt['right'])
            return result
        if balance > 0:
            creditor = debt['left']
            debtor = debt['right']
        else:
            creditor = debt['right']
            debtor = debt['left']
            balance = -balance
        result = '%s owes %s %d$' %(debtor, creditor, balance)
        return result