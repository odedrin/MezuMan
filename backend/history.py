import pymongo 
import backend
from backend.connect_data import database
from datetime import datetime

#defines variable for 'History' collection
history = database['History']

class History():
    #create new event document in history collection
    @staticmethod
    def add(event_type, group, debtor, creditor, amount, description):
        now = datetime.now()
        now_str = now.strftime('%d/%m/%Y %H:%M')
        new_event = {'type': event_type, 'group': group, 'debtor': debtor, 'creditor': creditor,
        'description': description, 'amount': amount, 'time': now_str}
        try:
            history.insert(new_event)
            return True
        except:
            return False
   