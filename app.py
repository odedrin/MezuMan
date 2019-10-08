import pymongo
from flask import Flask, flash, redirect, render_template, request, url_for
import backend
from backend.group_functions import *
from backend.group_functions import DuplicateError
from backend.user_functions import *
from backend.connect_data import database, connection


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
    except backend.group_functions.DuplicateError:
        flash("Username already exists, try a different one.")
        return render_template('add_user.html', title = 'Add user', userscl =userscl)
    # except:
    #     flash("Something went wrong")
    #     return render_template('add_user.html', title = 'Add user', userscl =userscl)

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
    user = userscl.find_one_and_delete({'name':username})
    flash("The user %s was deleted Successfully" %(username))
    return redirect('/users/', code= 302)

@app.route("/groups/delete_group/<groupname>", methods= ["POST", 'GET'])
def delete_group(groupname):
    group = groupscl.find_one_and_delete({'name':groupname})
    flash("The group %s was deleted Successfully" %(groupname))
    return redirect('/groups/', code= 302)

@app.route("/groups/<groupname>/edit_group_members", methods= ["POST", "GET"])
def edit_group_members(groupname):
    if request.method == "GET":
        return render_template('edit_group_members.html', groupname=groupname)
    groupname = request.form['text']
    return groupname

if __name__ == "__main__":
    app.run(port=8000, debug=True)

    connection.close()
