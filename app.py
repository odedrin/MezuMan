import pymongo
from flask import Flask, flash, redirect, render_template, request, url_for
import backend
from backend.connect_data import connection
from backend.users import *
from backend.groups import *
from backend.groups import DuplicateError
from backend.integration import *
from backend.debts import *

#initialize database
users = database['Users']
groups = database['Groups']


app = Flask(__name__)
app.config['SECRET_KEY'] = 'JH864Fzwimx792qs7s6ge6fs57MKAjh5jwiqks876dbapayeGFDJ'
app.config.from_object(__name__)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('homepage.html')

@app.route('/users_page/', methods= ['GET', 'POST'])
def users_page():
    users_list = Users.make_list()
    return render_template('users.html', title = 'Users',users_list =users_list)

@app.route('/groups_page/')
def groups_page():
    groups_list = Groups.make_list()
    return render_template('groups.html', title = 'Groups', groups_list =groups_list)

@app.route('/add_user/', methods= ['POST', 'GET'])
def add_user():
    if request.method == 'GET':
         return render_template('add_user.html', title = 'Add user')
    username = request.form['username']
    if len(username.strip()) in range(2, 21):
        try:    
            if Users.add(username):
                flash('User created successfully!')
                return redirect('/users_page/', code=302)
            else:
                flash('Something went wrong')
                return render_template('add_user.html', title = 'Add user')
        except DuplicateError:
            flash('Username already exists, try a different one.')
            return render_template('add_user.html', title = 'Add user')
    else:
        flash('Invalid username')
        return render_template('add_user.html', title = 'Add user')

@app.route('/add_group/', methods= ['POST', 'GET'])
def add_group():
    if request.method == 'GET':
         return render_template('add_group.html', title = 'Add group')
    groupname = request.form['groupname']
    if len(groupname.strip()) in range(2, 21):
        try:
            if Groups.add(groupname):
                flash('group created successfully!')
                return redirect('/groups_page/', code=302)
            else:    
                flash('Something went wrong.')
                return render_template('add_group.html', title = 'Create group')
        except DuplicateError:
            flash('group name already exists, try a different one.')
            return render_template('add_group.html', title = 'Create group')
    else:
        flash('Invalid name, Try again')
        return render_template('add_group.html', title = 'Create group')

# app.jinja_env.globals.update(user_in_debt=user_in_debt)
# app.jinja_env.globals.update(show_debt=show_debt)
# app.jinja_env.globals.update(show_event=show_event)


@app.route('/users_page/<username>')
def user_info(username):
    user = users.find_one({'name': username})
    if user != None:
        user_debts = []
        user_history = []
        for debt in debts.find():
            if user_in_debt(username, debt['_id']):
                user_debts.append(debt)
                # debt_strings.append(Debts.show(debt['_id']))
        for event in history.find():
            if event['debtor'] == user['name'] or event['creditor'] == user['name']:
                user_history.append(event)
                # event_strings.append(History.show(event))
        return render_template('user_info.html', title= username, user= user,
         user_debts = user_debts, user_history= user_history)

@app.route('/groups_page/<groupname>', methods= ['POST', 'GET'])
def group_info(groupname):
    group = groups.find_one({'name': groupname})
    if group != None:
        group_debts = []
        group_history = []
        for debt in debts.find():
            for member in group['members']:
                if user_in_debt(member, debt['_id']) and debt not in group_debts:
                        group_debts.append(debt)
        for event in history.find():
            if event['group'] == groupname:
                group_history.append(event)
        return render_template('group_info.html', title= groupname, 
        group= group, group_debts = group_debts, group_history= group_history)
    else:
        return 'No such group'
       
@app.route('/users_page/delete_user/<username>', methods= ['POST', 'GET'])
def delete_user(username):
    #missing: remove the user from all other groups and change size
    deleted = delete_user_doc(username)
    if deleted:
        flash('The user %s was deleted Successfully' %(username))
    else:
        flash('User not deleted')
    return redirect('/users_page/', code= 302)

@app.route('/groups_page/delete_group/<groupname>', methods= ['POST', 'GET'])
def delete_group(groupname):
    #missing: remove group from all user's lists
    deleted = delete_group_doc(groupname)
    if deleted:
        flash('The group %s was deleted Successfully' %(groupname))
    else:
        flash('Group not deleted')
    return redirect('/groups_page/', code= 302)

@app.route('/groups_page/<groupname>/edit_group_members')
def edit_group_members(groupname):
    title = 'edit ' + groupname
    group = groups.find_one({'name':groupname})
    users_list = Users.make_list()
    return render_template('edit_group_members.html', title= title, group = group, users_list = users_list)

@app.route('/groups_page/<groupname>/edit_group_members/add/<new_member>')
def add_new_member(groupname, new_member):
    added = add_user_to_group(new_member, groupname)    
    if added:    
        flash('%s added to %s!' %(new_member, groupname))
    else:
        flash('something went wrong')
    return redirect(url_for('edit_group_members', groupname= groupname), code= 302)    

@app.route('/groups_page/<groupname>/edit_group_members/remove/<member>')
def remove_user(groupname, member):
    removed = remove_user_from_group(member, groupname)
    if removed:
        flash('%s removed from %s!' %(member, groupname))
    else:
        flash('something went wrong')
    return redirect(url_for('edit_group_members', groupname= groupname), code= 302) 

@app.route('/groups_page/<groupname>/new_expense/', methods = ['GET'])
def new_expense_get(groupname):
    group = groups.find_one({'name': groupname})
    return render_template('new_expense.html', group= group, title = 'New expense')

@app.route('/groups_page/<groupname>/new_expense/', methods = ['POST'])
def new_expense_post(groupname):
    group = groups.find_one({'name': groupname})
    amount = request.form['amount']
    amount = int(amount)
    creditorname = request.form['creditorname']
    description = request.form['description']
    debtor_list = request.form.getlist('debtors')
    if debtor_list == []:
        flash('No members in expense')
        return redirect(url_for('group_info', groupname = groupname))
    if not description:
        description = 'unknown'
    equal_exspense(group, debtor_list, creditorname, amount, description)
    flash('Expense added to %s' %(groupname))
    return redirect(url_for('group_info', groupname = groupname))

@app.route('/settle_up/<creditor>/<debtor>', methods = ['POST'])
def settle_up(creditor, debtor):
    debt_id = Debts.find(creditor, debtor)
    groupname = request.form['groupname']
    destination = request.form['destination']
    settled = settle_debt(debt_id, groupname)
    if settled:
        flash('settled')
        return redirect(destination, code=302)
    flash('debt not settled. An error occured')
    return redirect(destination)

if __name__ == '__main__': 
    app.run(port=8000, debug=True)
    
    connection.close()

