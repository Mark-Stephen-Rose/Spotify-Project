from jsonpickle import encode
from jsonpickle import decode
from flask import Flask
from flask import abort, redirect, url_for
from flask import request
from flask import render_template
from flask import session
from accountdao import AccountDAO
from account import Account

app = Flask(__name__)

@app.route('/')
def index():
  dao = AccountDAO()
  dao.populate()
  return render_template('login.html', **locals())

@app.route('/login',methods=['GET','POST'])
def login():
  # get account id from login and get account from db
  dao = AccountDAO()

  # if account is not none it's a valid account jump to home page
  if ('username' in request.form) and ('password' in request.form):
    dao = AccountDAO()
    account = dao.selectByUsernameAndPassword(request.form['username'],request.form['password'])
    print(dir(account))
    # save account to session
    session['account'] = encode(account)
    if (account.status == 'admin'):
      return redirect(url_for('admin'))
    else:
      return redirect(url_for('home'))

  # if account is none then invalid account or first time jump to login page
  else:
    return render_template('login.html', **locals())

@app.route('/register',methods=['GET','POST'])
def register():
  dao = AccountDAO()
  
  if ('fname' in request.form) and ('lname' in request.form):
    id = None
    while (id == None): #If this returns none that means there is a match and a new id has to be made
      id = dao.makeId()
    row = [request.form['fname'],request.form['lname'],request.form['street'],request.form['city'],request.form['state'],int(request.form['zip']),int(request.form['phone']),request.form['email'],request.form['username'],request.form['password'],'guest',int(id)]
    account = dao.rowToAccount(row)
    dao.insert(account)
    return redirect(url_for('login'))
  else:
    return render_template('register.html', **locals())


@app.route('/home',methods=['GET','POST'])
def home():
  account = decode(session['account'])
  return render_template('home.html', **locals())

@app.route('/settings',methods=['GET','POST'])
def settings():
  dao = AccountDAO()
  account = decode(session['account'])
  
  if ('modifyuser' in request.form):
    return redirect(url_for('modifyuser'))
  elif ('delete' in request.form):
    dao.delete(account)
    return redirect(url_for('login'))
  else:
    return render_template('settings.html', **locals())

@app.route('/modifyuser',methods=['GET','POST'])
def modifyuser():
  dao = AccountDAO()
  account = decode(session['account'])
  row = dao.accountToRow(account)
  if ('fname' in request.form) and ('lname' in request.form) and ('street' in request.form) and ('city' in request.form) and ('state' in request.form) and ('zip' in request.form) and ('phone' in request.form) and ('email' in request.form) and ('username' in request.form) and ('password' in request.form):
    id = account.id
    row1=[request.form['fname'],request.form['lname'],request.form['street'],request.form['city'],request.form['state'],int(request.form['zip']),int(request.form['phone']),request.form['email'],request.form['username'],request.form['password'],'guest',int(id)]
    account1 = dao.rowToAccount(row1)
    dao.update(account1)
    return redirect(url_for('settings'))
  else:
    return render_template('modifyuser.html', **locals())

@app.route('/adminmodify',methods=['GET','POST'])
def adminmodify():
  dao = AccountDAO()
  account = decode(session['account'])
  row = dao.accountToRow(account)
  if ('fname' in request.form) and ('lname' in request.form) and ('street' in request.form) and ('city' in request.form) and ('state' in request.form) and ('zip' in request.form) and ('phone' in request.form) and ('email' in request.form) and ('username' in request.form) and ('password' in request.form):
    id = account.id
    row1=[request.form['fname'],request.form['lname'],request.form['street'],request.form['city'],request.form['state'],int(request.form['zip']),int(request.form['phone']),request.form['email'],request.form['username'],request.form['password'],'admin',int(id)]
    account1 = dao.rowToAccount(row1)
    dao.update(account1)
    return redirect(url_for('admin'))
  else:
    return render_template('adminmodify.html', **locals())


@app.route('/admin',methods=['GET','POST'])
def admin():
  accounts = AccountDAO().selectAll()
  return render_template('admin.html', **locals())


@app.route('/adminview', methods=['GET', 'POST'])
def admin_view():
  if 'account' in session:
    accounts = AccountDAO().selectAll()
    return render_template('adminview.html', **locals())
  else:
    return redirect(url_for('login'))


@app.route('/viewuser', methods=['POST'])
def viewuser():
  if 'id' in request.form:
    user_id = int(request.form['id'])
    dao = AccountDAO()
    user = dao.selectById(user_id)
    if user:
      return render_template('viewuser.html', **locals())
  return redirect(url_for('admin'))


@app.route('/deleteuser', methods=['POST'])
def delete_user():
  if 'deleteaction' in request.form:
    user_id = int(request.form['delete_userid'])  
    dao = AccountDAO()
    user = dao.selectById(user_id)
    if user:
      dao.delete(user)
  return redirect(url_for('admin'))


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)
