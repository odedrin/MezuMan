import pymongo
import backend
from backend.groups import *
from backend.users import *
from backend.debts import *
from backend.history import *

#the following function adds user to group's members list and 
#group to user's groups list in DB by calling 'push_member_in_group'
#and 'push_group_to_user' functions.
#returns True if successful, False if not and 
#raises DuplicateError if user already in group.
def add_user_to_group(username, groupname):
    group = groups.find_one({'name': groupname})
    if username in group['members']: #this prevents from adding the same member twice
        raise DuplicateError ('member already in group')
     #attemp to make changes to DB
    member_pushed = Groups.add_member(username, groupname)
    group_pushed = Users.add_group(username, groupname)
    #make sure the everything worked. if not- undo changes and return False
    if member_pushed and group_pushed: #if both sides succeeded
        return True
    elif group_pushed and not member_pushed: #if only user's groups updated
        remove_group_from_user(username, groupname)
    else: # if only group's side updated
        remove_member_from_group(username, group)
    return False

#the following function removess user from group's members list and
#group from user's groups list in DB by calling 'remove_member_from_group'
# and 'remove_group_from_user' functions.
#returns True if successful and False if not
def remove_user_from_group(username, groupname):
    group = groups.find_one({'name': groupname})
    if username in group['members']:
        #attempt to make changes to DB
        member_removed = Groups.remove_member(username, groupname)
        group_removed = Users.remove_group(username, groupname)
        #make sure the everything worked. if not- undo changes and return False
        if member_removed and group_removed:
            return True
        elif group_removed and not member_removed:
            Users.add_group(username, groupname)
        else:
            Groups.add_member(username, groupname)
        return False
    return False

#Removes the user from all of it's groups and deletes user's document from DB 
def delete_user_doc(username):
    all_groups = groups.find()
    #remove user from all of it's groups
    for group in all_groups: 
        if username in group['members']: #update all groups' documents
            Groups.remove_member(username, group['name'])
    #settle and delete all user's debts
    for debt in debts.find():
        if user_in_debt(username, debt['_id']):
            settle_debt(debt['_id'])
            debts.find_one_and_delete({'_id': debt['_id']})     
    #delete user document from DB
        for event in history.find():
            if event['debtor'] == username:
                history.find_one_and_update({'_id': event['_id']}, {'$set': {'debtor': username + " - deleted"}})
            elif event['creditor'] == username:
                history.find_one_and_update({'_id': event['_id']}, {'$set': {'creditor': username + " - deleted"}})
    users.find_one_and_delete({'name': username})
    return True

#Removes the group from all of it's users groups list and deletes group's document from DB 
def delete_group_doc(groupname):
    #remove group from all the users' group list
    all_users = users.find()
    for user in all_users:
        if groupname in user['groups']:
            Users.remove_group(user['name'], groupname)
    for event in history.find():
        if event['group'] == groupname:
            history.find_one_and_update({'_id': event['_id']}, {'$set': {'group': groupname + " - deleted"}})
    #remove group document from DB
    groups.find_one_and_delete({'name': groupname})
    return True
    

def equal_exspense(group, debtor_list, creditorname, amount, description='unknown'):
    personal_debt = amount/len(debtor_list)
    for member in debtor_list:
        if member != creditorname:
            Users.transaction(member, creditorname, personal_debt)
            History.add('expense', group['name'], member, creditorname, personal_debt, description)
    return True

def user_in_debt(username, debt_id):
    debt = debts.find_one({'_id': debt_id})
    if debt['left'] == username or debt['right'] == username:
        return True
    return False

def settle_debt(debt_id, groupname = None):
    debt = debts.find_one({'_id': debt_id})
    if debt != None:
        left_user = users.find_one({'name': debt['left']})
        right_user = users.find_one({'name': debt['right']})
        Users.edit_balance(left_user['name'], (left_user['balance'] - debt['balance']))
        Users.edit_balance(right_user['name'], (right_user['balance'] + debt['balance']))
        debts.update_one({'_id': debt_id}, {'$set':{'balance': 0}})
        History.add('settle_up', groupname, left_user['name'], right_user['name'], debt['balance'], 'settle up')
        return True
    else:
        return False
    