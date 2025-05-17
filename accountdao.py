import cx_Oracle
from account import Account

class AccountDAO:
  def __init__(self):
    #Establishes a connection to the database
    self.dsn = cx_Oracle.makedsn('csc325.cjjvanphib99.us-west-2.rds.amazonaws.com', 1521, sid="ORCL")
    self.connection = cx_Oracle.connect(user='mrose6', password='csrocks55',dsn=self.dsn)
    # Obtain a cursor
    self.cursor = self.connection.cursor()

  def __del__(self):
    #is a finalizer that will close and disconnect from the database at the end
    self.cursor.close()
    self.connection.close()

  def rowToAccount(self,row):
    account = Account(row[0],row[1],row[2])
    return account

  def accountToRow(self,account):
    row = dict( email=account.email, username=account.username, id=account.id)
    return row

  def insert(self,account):
    sql = "insert into ACCOUNT values (\'" + str(account.email) + "\', \'" + str(account.username) + "\', \'" + str(account.id) +"\')"
    self.cursor.execute(sql)
    self.connection.commit()

  def delete(self, account):
    sql = "delete from ACCOUNT where id='" + str(account.id) + "'"
    self.cursor.execute(sql)
    self.connection.commit()

  def deleteAll(self):
    sql = "delete from ACCOUNT"
    self.cursor.execute(sql)
    self.connection.commit()

  def selectAll(self):
    sql = "select * from ACCOUNT"
    self.cursor.execute(sql)
    accounts=[]
    while True:
      row = self.cursor.fetchone()
      if row is None:
        break
      account = self.rowToAccount(row)
      accounts.append(account)
    return accounts

  def selectById(self,id):
    sql = "select * from ACCOUNT where id='" + str(id) + "'"
    self.cursor.execute(sql)
    row = self.cursor.fetchone()
    if row!= None:
      user = self.rowToAccount(row)
      return user
    return None
  
  def selectByUsernameAndEmail(self,username,email):
    sql = "select * from ACCOUNT where username='"+str(username)+"' and email='"+str(email)+"'"
    self.cursor.execute(sql)
    row = self.cursor.fetchone()
    if row != None:
      user = self.rowToAccount(row)
      return user
    return None

  def update(self, account):
    sql = str("update ACCOUNT set email=\'" + str(account.email) + "\', username=\'" + str(account.username) + "\', id=\'" + str(account.id) + "\' where id='" + str(account.id) + "'")
    self.cursor.execute(sql)
    self.connection.commit()

  def populate(self):
    self.deleteAll()
    account = Account('mrosey204@gmail.com','Mahk','31vynekravirp75ptf2ba2b2i6du')
    self.insert(account)

  def getIds(self):
    accounts = self.selectAll()
    ids = []
    for account in accounts:
      ids.append(account.id)
    return ids

  def getUser(self, email, username, userid):
    existing_user = self.selectById(userid)
    if existing_user:
      return existing_user

    new_account = Account(email, username, userid)
    self.insert(new_account)
    return new_account