#!/usr/bin/python3

#Author: Andy Garcia

#Validate cookie info and parse data
import os
import html_pages
import database

#Checks for cookies in browser and parses data
cookie_dict = dict()
if "HTTP_COOKIE" in os.environ :
    cookie_info = os.environ["HTTP_COOKIE"]
    cookies = cookie_info.split(';')
    for cookie in cookies:
        cookie_split = cookie.split('=')
        cookie_dict[cookie_split[0].strip()] = cookie_split[1].strip()

    #Stores cookie data
    CookieUsername = cookie_dict.get('username')
    CookiePassword = cookie_dict.get('password')
    CookieToken = cookie_dict.get('CSRFtoken')

    #Grabs user information from database
    from database import UserInfo
    user = UserInfo(CookieUsername)

    #Validates cookies with the credentials from database
    #Returns to login page if cookie credentials are invalid
    from database import validCookies
    if (validCookies(CookieUsername, CookiePassword, CookieToken)):

        #Displays transfer page if successful
        from html_pages import transfer_page
        transfer_page(user[2])

    #If cookies are invalid then returns to login page
    elif (validCookies(CookieUsername, CookiePassword, CookieToken) is not True):
        from html_pages import login_page
        login_page()

#If no cookies are detected
else:
    status = "Cookies missing!"
    from html_pages import failure_page
    failure_page(status)
