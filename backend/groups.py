import pymongo 
import backend
from backend.connect_data import database

#define variable for 'groups' collection
groups = database['Groups']

class DuplicateError(Exception):
    pass

class Groups():
    @staticmethod
    #makes list of all groups
    def make_list():
        groups_list = []
        for group in groups.find():
            groups_list.append(group)
        return groups_list

    #Checks if group exists
    @staticmethod
    def group_exists(name):
        group = groups.find_one({'name' : name})
        if group != None:
            return True
        return False

#makes sure no other group with the same name exists
#  and creates new group document in groups collection
    @staticmethod
    def add(name):
        if Groups.group_exists(name):
            print('this group name already exists, choose another name')
            raise DuplicateError
        new_group = {'name' : name, 'size': 0, 'members' : []}
        groups.insert_one(new_group)
        return True

#Edit group. keys to insert = 'name' or 'size'
    @staticmethod
    def edit(name, key, new_value): 
        groups.update({'name': name}, {'$set':{key : new_value}})
        return True

#adds user to group's members list in DB (nested array) and updates group's size
    @staticmethod
    def add_member(username, groupname):
        try:
            #add member to nested array
            groups.find_one_and_update({'name': groupname}, {'$push': {'members': username}})
            group = groups.find_one({'name': groupname})
            groupsize = len(group['members']) #update group size
            Groups.edit(groupname, 'size', groupsize) 
            return True
        except:
            return False
        
#removes user from group's members list in DB (nested array) and updates group's size
    @staticmethod
    def remove_member(username, groupname):
        #remove member from nested array
        groups.find_one_and_update({'name': groupname}, {'$pull': {'members': username}})
        group = groups.find_one({'name': groupname})
        groupsize = len(group['members'])
        Groups.edit(groupname, 'size', groupsize) 
        return True
