import pymongo 
from connect_data import database

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
    if group_exists('name'):
        groupscl.update({'name': name}, {"$set":{key : new_value}})
        return True
    print("group does not exist")
    return False 

def add_member_in_group(groupname, newmember):
    group= groupscl.update({'name': groupname}, {'$push': {'members': newmember}})
