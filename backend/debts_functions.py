import pymongo 
import backend
from backend.connect_data import database
# from connect_data import database

#define variable for 'debts' collection
debtscl = database['Debts']

#creates new debt, when left user is initially the creditor.
#positive balance signifies left user is creditor. negitive signifies right is creditor.
# returns debt id
def new_debt(left_user, right_user, balance):
    new_debt = {'left': left_user, 'right': right_user, 'balance': balance}
    debt = debtscl.insert_one(new_debt)
    return debt.inserted_id

#check if user1 and user2 already have an existing debt, no matter the sides. 
# if so returns the debt's id in the DB, if not returns False.
def debt_exists(user1, user2):
    for debt in debtscl.find():
        if debt['left'] != user1 and debt['right'] != user1:
            continue
        if debt['left'] == user2 or debt['right'] == user2:
            return debt['_id']
    return None

#if debt already exists between the users it is updated. if not a new debt is created.
#returns debt DB id.
def edit_debt(creditor, debtor, balance):
    debt_id = debt_exists(creditor, debtor)
    if debt_id:
        debt = debtscl.find_one({'_id': debt_id})
        if debt['right'] == creditor:
            balance = -balance
        new_balance = debt['balance'] + balance
        debtscl.update_one({'_id': debt_id}, {"$set":{'balance' : new_balance}})
        return debt_id
    else:
        return new_debt(creditor, debtor, balance)

#return string: "(debtor) owes (creditor) (balance)" or "(debtor) and (creditor) settled up"
def show_debt(debt_id):
    debt = debtscl.find_one({"_id": debt_id})
    balance = debt['balance']
    if balance == 0:
        result = "%s and %s are settled up" %(debt['left'], debt['right'])
        return result
    if balance > 0:
        creditor = debt['left']
        debtor = debt['right']
    else:
        creditor = debt['right']
        debtor = debt['left']
        balance = -balance
    result = "%s owes %s %d$" %(debtor, creditor, balance)
    return result