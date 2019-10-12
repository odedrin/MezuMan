import pymongo
import backend
from backend.group_functions import *
from backend.user_functions import *

def add_user_to_group(username, groupname):
    group = groupscl.find_one({'name': groupname})
    if username in group['members']: #this prevents from adding the same member twice
        raise DuplicateError ("member already in group")
     #<try to remove member from group and group from user>
    member_pushed = push_member_in_group(username, groupname)
    group_pushed = push_group_to_user(username, groupname)
    if member_pushed and group_pushed: #if both sides succeeded
        return True
    elif group_pushed and not member_pushed: #if only user's groups updated
        remove_group_from_user(username, groupname)
    else: # if only group's side updated
        remove_member_from_group(username, group)
    return False

def remove_user_from_group(username, groupname):
    group = groupscl.find_one({'name': groupname})
    if username in group['members']:
        member_removed = remove_member_from_group(username, groupname)
        group_removed = remove_group_from_user(username, groupname)
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


def delete_user_doc(username):
    all_groups = groupscl.find()
    #remove user from all of it's groups
    for group in all_groups: 
        if username in group['members']: #update all groups' documents
            remove_member_from_group(username, group['name'])
    #delete user document from DB
    userscl.find_one_and_delete({'name': username})
    return True

def delete_group_doc(groupname):
    #remove group from all the users' group list
    all_users = userscl.find()
    for user in all_users:
        if groupname in user['groups']:
            remove_group_from_user(user['name'], groupname)
    #remove group document from DB
    groupscl.find_one_and_delete({'name': groupname})
    return True

if __name__ == "__main__":
    print(add_user_to_group('Moomoo', 'English Bulldogs'))
    


