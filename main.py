#!/usr/bin/python3

#Author: Andy Garcia

import html_pages
import os
import database

#Grabs cookie data and parses data
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

   #Checks if cookies are valid
   from database import validCookies  
   if(validCookies(CookieUsername, CookiePassword, CookieToken)):

      #Passes banking information from database to welcome page
      from database import UserInfo
      user = UserInfo(CookieUsername)
      from html_pages import welcome_page
      html_pages.welcome_page(user[0], user[3], user[4])

   #Returns to login page if credentials fail
   else: 
      from html_pages import login_page
      html_pages.login_page()

#If there are no cookies then call display login page
else:
   from html_pages import login_page
   html_pages.login_page()

   
