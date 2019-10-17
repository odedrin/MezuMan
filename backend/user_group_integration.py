import pymongo
import backend
from backend.group_functions import *
from backend.user_functions import *
from backend.debts_functions import *
from backend.history_functions import *

#the following function adds user to group's members list and 
#group to user's groups list in DB by calling 'push_member_in_group'
#and 'push_group_to_user' functions.
#returns True if successful, False if not and 
#raises DuplicateError if user already in group.
def add_user_to_group(username, groupname):
    if not user_exists(username):
        return False
    group = groupscl.find_one({'name': groupname})
    if username in group['members']: #this prevents from adding the same member twice
        raise DuplicateError ("member already in group")
     #attemp to make changes to DB
    member_pushed = push_member_in_group(username, groupname)
    group_pushed = push_group_to_user(username, groupname)
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
    group = groupscl.find_one({'name': groupname})
    if username in group['members']:
        #attempt to make changes to DB
        member_removed = remove_member_from_group(username, groupname)
        group_removed = remove_group_from_user(username, groupname)
        #make sure the everything worked. if not- undo changes and return False
        if member_removed and group_removed:
            return True
        elif group_removed and not member_removed:
            print("member not removed")
            push_group_to_user(username, groupname)
        else:
            print("member not removed")
            push_member_in_group(username, groupname)
        return False
    print("No user named %s in %s" %(username, groupname))
    return False

#Removes the user from all of it's groups and deletes user's document from DB 
def delete_user_doc(username):
    if user_exists(username):
        all_groups = groupscl.find()
        #remove user from all of it's groups
        for group in all_groups: 
            if username in group['members']: #update all groups' documents
                remove_member_from_group(username, group['name'])
        #settle and delete all user's debts
        for debt in debtscl.find():
            if user_in_debt(username, debt['_id']):
                settle_debt(debt['_id'])
                debtscl.find_one_and_delete({'_id': debt['_id']})     
        #delete user document from DB
        userscl.find_one_and_delete({'name': username})
        return True

#Removes the group from all of it's users groups list and deletes group's document from DB 
def delete_group_doc(groupname):
    if group_exists(groupname):
        #remove group from all the users' group list
        all_users = userscl.find()
        for user in all_users:
            if groupname in user['groups']:
                remove_group_from_user(user['name'], groupname)
        #remove group document from DB
        groupscl.find_one_and_delete({'name': groupname})
        return True
    

def equal_exspense(group, creditorname, amount, description='unknown'):
    personal_debt = amount/group['size']
    for member in group['members']:
        if member != creditorname:
            transaction(member, creditorname, personal_debt)
            add_event('expense', group['name'], member, creditorname, personal_debt, description)
    return True

def user_in_debt(username, debt_id):
    debt = debtscl.find_one({"_id": debt_id})
    if debt['left'] == username or debt['right'] == username:
        return True
    return False

def settle_debt(debt_id, groupname = None):
    debt = debtscl.find_one({"_id": debt_id})
    if debt != None:
        left_user = userscl.find_one({'name': debt['left']})
        right_user = userscl.find_one({'name': debt['right']})
        edit_user(left_user['name'], 'balance', (left_user['balance'] - debt['balance']))
        edit_user(right_user['name'], 'balance', (right_user['balance'] + debt['balance']))
        debtscl.update_one({'_id': debt_id}, {'$set':{'balance': 0}})
        add_event('settle_up', groupname, left_user['name'], right_user['name'], 0, 'settle up')
        return True
    else:
        return False
    