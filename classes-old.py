from datetime import date

class user:
    def __init__(self, name):
        self.name = str(name)
        self.balance = 0
        # All of the user's movements
        self.uhistory = []
        # A dictionary with the user's friends as keys and debt as value
        self.friends = {}
        self.groups = []

    def __repr__(self):
        return self.name
    # checks if self is already friends with 'friend'
    def is_friend(self, friend):
        if isinstance(friend, user):
            if friend in self.friends:
                return True
        return False

    def add_friend(self, new_friend):
        if isinstance(new_friend, user) and not new_friend.is_friend(self):
            self.friends[new_friend] = 0
            new_friend.friends[self] = 0
            return True
        else:
            print("Error adding user")
            return False


    def pay(self, friend, amount, group, reason, category):
        if self.is_friend(friend):
            self.balance -= amount
            self.friends[friend] -= amount
            friend.balance += amount
            friend.friends[self] += amount
            self.uhistory.append((self, friend, amount, group, reason, category, date.today()))
            friend.uhistory.append((self, friend, amount, group, reason, category, date.today()))
        else:
            print("Transaction not available")

    def remove_friend(self, friend):
        if self.is_friend(friend):
            temp = self.friends.pop(friend, False)
            if temp != False:
                temp2 = temp.friends.pop(self, False)
                if temp2 != False:
                    return True
        return False

    def create_group(self, name):
        pass

class group:
    def __init__(self, name):
        pass
    
    def add_user(self, user):
        pass

    def remove_user(self, user):
        pass

    def has_user(self, user):
        pass
    
    def transfer(self, payers, recievers, reason):
        pass

    def devide_new_payment(self):
        pass

class database():
    def __init__(self):
        self.users = []
        self.groups = []


def is_user(database, name):
    if "name" in database.users:
        return True
    return False

def is_group(database, name):
    if isinstance(name, group):
        return True
    return False