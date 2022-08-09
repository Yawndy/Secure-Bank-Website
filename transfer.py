#!/usr/bin/python3

#Author: Andy Garcia

import database
import os
import cgi
import html_pages

#Grabs cookie information stored in browser
cookie_dict = dict()
if "HTTP_COOKIE" in os.environ:
   cookie_info = os.environ["HTTP_COOKIE"]
   cookies = cookie_info.split(';')

   for cookie in cookies:
      cookie_split = cookie.split('=')
      cookie_dict[cookie_split[0].strip()] = cookie_split[1].strip()

   #Stores cookie data
   CookieUsername = cookie_dict.get('username')
   CookiePassword = cookie_dict.get('password')
   CookieToken = cookie_dict.get('CSRFtoken')

#Grabs information from transfer_page
form = cgi.FieldStorage()

try:
   Recipient = cgi.escape(form["recipient"].value)
except KeyError:
   Recipient = "void"
try:
   SendersAcc = cgi.escape(form["SenderAccount"].value)
except KeyError:
   SendersAcc = "void"
try:
   RecipientsAcc = cgi.escape(form["RecipientAccount"].value)
except KeyError:
   RecipientsAcc = "void"
try:
   Transfer = cgi.escape(form["transfer"].value)
except KeyError:
   Transfer = "void"

#Grabs user from database
from database import UserInfo
user = UserInfo(CookieUsername)

#Validates cookies with credentials from database
from database import validCookies
if (validCookies(CookieUsername, CookiePassword, CookieToken)):

   #Checks for a valid recipient
   RecipientUser = UserInfo(Recipient)

   #Validates form for any blank information
   if RecipientUser:
      
      if RecipientsAcc != "void":

         if Transfer != "void": 

            if SendersAcc == "checkings":
               
               #Checks if enough funds are in the account
               if int(Transfer) <= int(user[3]):
                  from  database import updateBalance                  
                  updateBalance(Recipient, user[0], RecipientsAcc, SendersAcc, Transfer)
                  from html_pages import transfersuccess_page
                  transfersuccess_page()
            
               elif int(Transfer) > int(user[3]):
                  status = "Not enough funds!"
                  from html_pages import failure_page
                  failure_page(status)
            
            elif SendersAcc == "savings":

               #Checks if enough funds are in the account
               if int(Transfer) <= int(user[4]):     
                  from  database import updateBalance 
                  updateBalance(Recipient, user[0], RecipientsAcc, SendersAcc, Transfer)
                  from html_pages import transfersuccess_page
                  transfersuccess_page()

               elif int(Transfer) > int(user[4]):
                  status = "Not enough funds!"
                  from html_pages import failure_page
                  failure_page(status)         

            #Checks sender's account box for blank information
            elif SendersAcc == "void":
               status = "You need to select the sender's account!"
               from html_pages import failure_page
               failure_page(status)

         #Checks transfer box for blank information
         else:
               status = "You need to enter the amount to transfer!"
               from html_pages import failure_page
               failure_page(status)

      #Checks recipient's account box for blank information
      else:
         status = "You need to select the recipient's account!"
         from html_pages import failure_page
         failure_page(status)

   #Checks recipient box for blank information
   else:
      status = "Invalid recipient!"
      from html_pages import failure_page
      failure_page(status)

#Returns to login page if cookies are missing
elif (validCookies(CookieUsername, CookiePassword, CookieToken) is not True):
   from html_pages import login_page
   login_page()

