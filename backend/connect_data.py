import pymongo

#create connection to database

connection = pymongo.MongoClient('localhost', 27017)
database = connection['MezuMan_DB']