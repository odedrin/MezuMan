import pymongo 
import backend
from backend.connect_data import database

#defines variable for 'History' collection
historycl = database['History']

def add_event(event_type, group, debtor, creditor, amount, description="unknown"):
    new_event = {'type': event_type, 'group': group, 'debtor': debtor, 'creditor': creditor,
     'description': description, 'amount': amount}
    try:
        historycl.insert(new_event)
        return True
    except:
        return False

def show_event(event):
    if event['type'] == 'expense':
        result = ("%s gave %s %d$ for %s in %s group" %(event['creditor'], event['debtor'], event['amount'], event['description'], event['group']))
    elif event['type'] == 'settle_up':
        result = ("%s and %s settled up" %(event['creditor'], event['debtor']))
    else:
        return "invalid event type"
    return result