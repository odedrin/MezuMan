import pymongo 
import backend
from backend.connect_data import database

#define variable for 'groups' collection
groupscl = database['Groups']

class DuplicateError(Exception):
    pass

#If exists returns group id, if not- returns None.
def group_exists(name):
    group = groupscl.find_one({'name' : name})
    if group != None:
        return group['_id']

#Following funtions: if successful- returns True.

#create group document in DB and make sure there is no other group with the same name
def add_group_document(name):
    if len(name.strip()) > 1 and len(name.strip()) < 21:
        if group_exists(name):
            print("this group's name already exists, choose another name")
            raise DuplicateError
        new_group = {'name' : name, 'size': 0, 'members' : []}
        groupscl.insert_one(new_group)
        return True
    print("Invalid name")
    return False

#key = 'name' or 'size'
def edit_group(name, key, new_value): 
    groupscl.update({'name': name}, {"$set":{key : new_value}})
    return True

#adds user to group's members list in DB (nested array) and updates group's size
def push_member_in_group(username, groupname):
    try:
        #add member to nested array
        groupscl.find_one_and_update({'name': groupname}, {'$push': {'members': username}})
        group = groupscl.find_one({'name': groupname})
        groupsize = len(group['members']) #update group size
        edit_group(groupname, 'size', groupsize) 
        return True
    except:
        return False
        
#removes user from group's members list in DB (nested array) and updates group's size
def remove_member_from_group(username, groupname):
    try:
        #remove member from nested array
        groupscl.find_one_and_update({'name': groupname}, {'$pull': {'members': username}})
        group = groupscl.find_one({'name': groupname})
        groupsize = len(group['members'])
        edit_group(groupname, 'size', groupsize) 
        return True
    except:
        return False