#User Registration Signin Signup
from customer import *
from bank import Bank
import random
import re

def SignUp():
    username = input("Create Username: ")

    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", username):
        print("Invalid username")
        return

    temp = db_query(
        "SELECT username FROM customers WHERE username = %s",
        (username,)
    )

    if temp:
        print("Username Already Exists")
        return
    else:
        print("Username is Available Please Proceed")
        password = input("Enter Your Password: ")
        name = input("Enter Your Name: ")
        age = input("Enter Your Age: ")
        city = input("Enter Your City: ")
        while True:
            account_number = int(random.randint(10000000, 99999999))
            temp = db_query(f"SELECT account_number FROM customers WHERE account_number = '{account_number}';")
            if temp:
                continue
            else:
                print("Your Account Number",account_number)
                break
    cobj = Customer(username, password, name, age, city, account_number)
    cobj.createuser()
    bobj = Bank(username, account_number)
    bobj.create_transaction_table()
def SignIn():
    username = input("Enter Username: ")

    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", username):
        print("Invalid username")
        return

    temp = db_query(
        "SELECT username FROM customers WHERE username = %s",
        (username,)
    )

    if temp:
        while True:
            password = input(
                f"Welcome {username.capitalize()} Enter Password: "
            )

            temp = db_query(
                "SELECT password FROM customers WHERE username = %s",
                (username,)
            )

            if temp[0][0] == password:
                print("Sign IN Successfully")
                return username
            else:
                print("Wrong Password Try Again")
    else:
        print("Enter Correct Username")
