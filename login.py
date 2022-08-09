#!/usr/bin/python3

#Author: Andy Garcia

import html_pages
import database
import cgi, cgitb, os, pymysql, hashlib

#Grabs information from login_page
cgitb.enable()
form = cgi.FieldStorage()

try:
   username = cgi.escape(form["username"].value)
except KeyError:
   username = "void"

#Hashes the password 
try:
   password = cgi.escape(form["password"].value)
   encoded_password = password.encode(encoding='UTF-8')
   hashed = hashlib.sha224(encoded_password)
   password = hashed.hexdigest()

except KeyError:
   password = "void"

try:
   CSRFtoken = form["CSRFtoken"].value
except KeyError:
   CSRFtoken = "void"

#Grabs information from the database
from database import UserInfo
user = UserInfo(username)

#Validates user credentials with database
from database import validCookies
if user:
   if user[1] == password:

      #Updates CSRFtoken in mysql database
      from database import updateToken
      updateToken(username, CSRFtoken)

      #Prints success page which will redirect to welcome page
      from html_pages import success_page
      success_page(username, password, CSRFtoken)

   else:
      status = "Incorrect credentials!"
      from html_pages import failure_page
      failure_page(status)

else:
   status = "Incorrect credentials!"
   from html_pages import failure_page
   failure_page(status)
