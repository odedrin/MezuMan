import pymongo
from flask import Flask, flash, redirect, render_template, request, url_for
import backend
from backend.connect_data import connection
from backend.user_functions import *
from backend.group_functions import *
from backend.group_functions import DuplicateError
from backend.user_group_integration import *



#initialize database
userscl = database['Users']
groupscl = database['Groups']


app = Flask(__name__)
app.config['SECRET_KEY'] = 'JH864Fzwimx792qs7s6ge6fs57MKAjh5jwiqks876dbapayeGFDJ'
app.config.from_object(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('homepage.html')

@app.route("/users/", methods= ["GET", "POST"])
def users():
    return render_template('users.html', title = 'Users',userscl =userscl)

@app.route("/groups/")
def groups():
      return render_template('groups.html', title = 'Groups',groupscl =groupscl)

@app.route("/add_user/", methods= ["POST", "GET"])
def add_user():
    if request.method == 'GET':
         return render_template('add_user.html', title = 'Add user', userscl =userscl)
    username = request.form['text']
    try:    
        if add_user_document(username):
            flash("User created successfully!")
            return redirect('/users/', code=302)
        else:
            flash("Invalid username, please try again")
            return render_template('add_user.html', title = 'Add user', userscl =userscl)
    except DuplicateError:
        flash("Username already exists, try a different one.")
        return render_template('add_user.html', title = 'Add user', userscl =userscl)
    except:
        flash("Something went wrong")
        return render_template('add_user.html', title = 'Add user', userscl =userscl)

@app.route("/add_group/", methods= ["POST", "GET"])
def add_group():
    if request.method == 'GET':
         return render_template('add_group.html', title = 'Add group', groupscl =groupscl)
    username = request.form['text']
    try:
        if add_group_document(username):
            flash("group created successfully!")
            return redirect('/groups/', code=302)
        else:
            flash("Invalid name, Try again")
            return render_template('add_group.html', title = 'Create group', groupscl =groupscl)
    except group_functions.DuplicateError:
        flash("group name already exists, try a different one.")
        return render_template('add_group.html', title = 'Create group', groupscl =groupscl)
    except:
        flash("Something went wrong.")
        return render_template('add_group.html', title = 'Create group', groupscl =groupscl)
   
@app.route("/users/<username>", methods= ["POST", "GET"])
def user_info(username):
    user = userscl.find_one({'name': username})
    if user != None:
        return render_template('user_info.html', title= username, user= user)
    else:
        return 'No such user'

@app.route("/groups/<groupname>", methods= ["POST", "GET"])
def group_info(groupname):
    group = groupscl.find_one({'name': groupname})
    if group != None:
        return render_template('group_info.html', title= groupname, group= group)
    else:
        return 'No such group'
        
@app.route("/users/delete_user/<username>", methods= ["POST", 'GET'])
def delete_user(username):
    #missing: remove the user from all other groups and change size
    deleted = delete_user_doc(username)
    if deleted:
        flash("The user %s was deleted Successfully" %(username))
    else:
        flash("User not deleted")
    return redirect('/users/', code= 302)

@app.route("/groups/delete_group/<groupname>", methods= ["POST", 'GET'])
def delete_group(groupname):
    #missing: remove group from all user's lists
    deleted = delete_group_doc(groupname)
    if deleted:
        flash("The group %s was deleted Successfully" %(groupname))
    else:
        flash("Group not deleted")
    return redirect('/groups/', code= 302)

@app.route("/groups/<groupname>/edit_group_members", methods= ["POST", "GET"])
def edit_group_members(groupname):
    if request.method == "GET":
        title = "edit " + groupname
        group = groupscl.find_one({'name':groupname})
        return render_template('edit_group_members.html', title= title, groupname=groupname, group = group, userscl = userscl)

@app.route("/groups/<groupname>/edit_group_members/add/<new_member>")
def add_new_member(groupname, new_member):
    try:
        added = add_user_to_group(new_member, groupname)
    except DuplicateError:
        flash("%s is already a member in the group" %(new_member))
        return redirect(url_for('edit_group_members', groupname= groupname), code= 302)    
    if added:    
        flash("%s added to %s!" %(new_member, groupname))
    else:
        flash("something went wrong")
    return redirect(url_for('edit_group_members', groupname= groupname), code= 302)    

@app.route("/groups/<groupname>/edit_group_members/remove/<member>")
def remove_user(groupname, member):
    removed = remove_user_from_group(member, groupname)
    if removed:
        flash("%s removed from %s!" %(member, groupname))
    else:
        flash("something went wrong")
    return redirect(url_for('edit_group_members', groupname= groupname), code= 302) 


if __name__ == "__main__":
    app.run(port=8000, debug=True)
    
    connection.close()

