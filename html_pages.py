#!/usr/bin/python3

#Author: Andy Garcia

import random
import string
import cgi, cgitb, os
cgitb.enable()

#Login page prompts user for credentials and generates token
def login_page():

    print("Content-Type: text/html")
    print()

    loginpage = """
    <!DOCTYPE html>
    <!-- HTML code to send a POST request to login.py -->
    <html>
    <head>
        <title>Safe Bank Website</title>
    </head>
    <body>
        <form action="login.py" method="POST">
            <h1>Safe Bank Website</h1>
            <strong>Username:</strong><br>
            <input type="text" name="username"><br>
            <strong>Password:</strong><br>
            <input type="text" name="password"><br>
            <input type="hidden" name="CSRFtoken" value="{token}">
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """
    
    #Generate CSRF token
    token = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=15))
    print(loginpage.format(token=token))   

#Welcome page when users successfully log on
def welcome_page(username, checkings, savings):

    print("Content-Type: text/html")
    print()

    welcomepage = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table, th, td {{ border: 2px solid black; text-align: left;}}
    th, td {{ padding: 5px; }}
    </style>
    </head>
    <body>

    <h2>Welcome {username}!</h2>
        
    <table style="width:100%">
        <tr>
            <th>Checkings</th>
            <th>Savings</th>
        </tr>
        <tr>
            <td>{checkings}</td>
            <td>{savings}</td>
        </tr>
    </table>
    <a href="http://localhost/srt311/project2/transfer_form.py">Transfer money</a>
        
    </body>
    </html>"""
    print(welcomepage.format(username=username,checkings=checkings,savings=savings))

#Prints success page and redirects user upon successful login and creates cookies
def success_page(username, password, CSRFtoken):

    successpage = """Content-Type: text/html
Set-Cookie: username={username}
Set-Cookie: password={password}
Set-Cookie: CSRFtoken={CSRFtoken}

<!DOCTYPE html>
<html>
<head>
    <title>Login successful!</title>
    <meta http-equiv = "refresh" content = "3; url = http://localhost/srt311/project2/main.py"/>
</head>
<body>
    <h1>Login</h1>
    <p> Status: <br> Succesful login! Please wait 3 seconds for the page to redirect you.</p>
</body>
</html>
"""

    print(successpage.format(username=username,password=password,CSRFtoken=CSRFtoken))
    
#Failure page will redirect users to the main page
def failure_page(status):
    failurepage = """Content-Type: text/html

    <!DOCTYPE html>
    <html>
    <head>
        <title>Error!</title>
        <meta http-equiv = "refresh" content = "3; url = http://localhost/srt311/project2/main.py"/>
    </head>
    <body>
        <h1>Error!</h1>
        <p> Status: <br> {status} Please wait 3 seconds for the page to redirect you.</p>
    </body>
    </html>
    """
    print(failurepage.format(status=status))

#Transfer page if cookies are valid
def transfer_page(CSRFtoken):
    
    transferpage = """Content-Type: text/html

    <!DOCTYPE html>
    <!-- HTML code to send a POST request to transfer.py -->
    <html>
        <head>
            <title>Safe Bank Website</title>
        </head>
        <body>
            <form action="transfer.py" method="POST">
            <h1><strong>Safe Bank Website</strong></h1>
            <input type="hidden" name="CSRFtoken" value="{CSRFtoken}">
            <strong>Enter recipient's username</strong><br>
            <input type="text" name="recipient"><br>
            <strong>Sender's account</strong><br>
            <input type="radio" name="SenderAccount" value="checkings"> Checkings<br>
            <input type="radio" name="SenderAccount" value="savings"> Savings<br><br>
            <strong>Recipient's account</strong><br>
            <input type="radio" name="RecipientAccount" value="checkings"> Checkings<br>
            <input type="radio" name="RecipientAccount" value="savings"> Savings<br><br>
            <strong>How much would you like to transfer?</strong><br>
            <input type="text" name="transfer"><br>
            <input type="submit" value="Submit">
            </form>
        </body>
    </html>"""
    print(transferpage.format(CSRFtoken=CSRFtoken))

#If funds are successfully transferred then this message will display
def transfersuccess_page():
    TransferSuccess = """Content-Type: text/html

    <!DOCTYPE html>
    <html>
    <head>
        <title>Success!</title>
        <meta http-equiv = "refresh" content = "3; url = http://localhost/srt311/project2/main.py"/>
    </head>
    <body>
        <h1>Login</h1>
        <p> Status: <br> Funds successfully transferred! Please wait 3 seconds for the page to redirect you.</p>
    </body>
    </html>
    """
    print(TransferSuccess)