import pymongo 
import backend
from backend.connect_data import database

groupscl = database['Groups']

class DuplicateError(Exception):
    pass

#If exists returns group id, if not- returns None.
def group_exists(name):
    group = groupscl.find_one({'name' : name})
    if group != None:
        return group['_id']


def add_group_document(name):
    if len(name.strip()) > 1 and len(name.strip()) < 21:
        if group_exists(name):
            print("this group's name already exists, choose another name")
            raise DuplicateError
        new_group = {'name' : name, 'size': 0, 'members' : [], 'group history' : []}
        groupscl.insert_one(new_group)
        return True
    print("Invalid name")
    return False

#key = 'name' or 'size'
def edit_group(name, key, new_value): 
    groupscl.update({'name': name}, {"$set":{key : new_value}})
    return True

def push_member_in_group(username, groupname):
    try:
        #add member to nested array
        group = groupscl.find_one({'name': groupname})
        groupscl.update({'name': groupname}, {'$push': {'members': username}})
        groupsize = group['size'] #update group size
        groupsize += 1 #TODO - make it update according to array length
        edit_group(groupname, 'size', groupsize) 
        return True
    except:
        return False
        
def remove_member_from_group(username, groupname):
    try:
        #remove member from nested array
        group = groupscl.find_one({'name': groupname})
        groupscl.update({'name': groupname}, {'$pull': {'members': username}})
        groupsize = group['size'] #update group size
        groupsize -= 1 
        edit_group(groupname, 'size', groupsize) 
        return True
    except:
        return False