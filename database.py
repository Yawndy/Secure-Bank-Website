#!/usr/bin/python3

#Author: Andy Garcia

#Connects to the MySQL database
import pymysql
conn = pymysql.connect(db='project2', user='algarcia1', passwd='root', host='localhost')
c = conn.cursor()

#Compares the cookies with the credentials on the database
def validCookies(username, password, CSRFtoken):
    query = "SELECT * FROM bank WHERE username='{username}'"
    c.execute(query.format(username=username))
    conn.commit()
    user = c.fetchone()

    if user:
        if password == user[1]:
            if CSRFtoken == user[2]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

#Grabs the information from a given username
#Returns False if the username is invalid
def UserInfo(user):

    query = "SELECT * FROM bank WHERE username='{user}'"
    c.execute(query.format(user=user))
    conn.commit()
    newuser = c.fetchone()

    if newuser:
        return newuser
    else:
        return False

#Uses the generated token from the browser and stores it in the user's database
def updateToken(username, CSRFtoken):

    query = "UPDATE bank SET current_csrf_token='{CSRFtoken}' WHERE username='{username}'"
    c.execute(query.format(CSRFtoken=CSRFtoken,username=username))
    conn.commit()

#Updates the balance of the bank accounts based on the data generated from transfer.py
def updateBalance(Recipient, Sender, RecipientsAcc, SendersAcc, transfer):
    query = "SELECT {SendersAcc} FROM bank WHERE username='{Sender}'"
    c.execute(query.format(SendersAcc=SendersAcc,Sender=Sender))
    conn.commit()
    SendersBal = c.fetchone()
    SendersNewBal = int(SendersBal[0]) - int(transfer)

    query = "SELECT {RecipientsAcc} FROM bank WHERE username='{Recipient}'"
    c.execute(query.format(RecipientsAcc=RecipientsAcc, Recipient=Recipient))
    conn.commit()
    RecipientsBal = c.fetchone()
    RecipientsNewBal = int(RecipientsBal[0]) + int(transfer)

    query = "UPDATE bank SET {SendersAcc}={SendersNewBal} WHERE username='{Sender}'"
    c.execute(query.format(SendersAcc=SendersAcc,SendersNewBal=SendersNewBal,Sender=Sender))
    conn.commit()

    query = "UPDATE bank SET {RecipientsAcc}={RecipientsNewBal} WHERE username='{Recipient}'"
    c.execute(query.format(RecipientsAcc=RecipientsAcc,RecipientsNewBal=RecipientsNewBal,Recipient=Recipient))
    conn.commit()

    
