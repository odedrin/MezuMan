import pymongo

connection = pymongo.MongoClient('localhost', 27017)
database = connection['MezuMan_DB']