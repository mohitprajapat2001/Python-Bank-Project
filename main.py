

import register
import bank


blocked = [
    "union", "select", "insert", "update", "delete",
    "drop", "alter", "create", "truncate",
    "--", ";",
    "'", '"'
]

status = False

print("Welcome to Mohit Banking Project")

while True:
    try:
        choice = int(input(
            "\n1. SignUp\n"
            "2. SignIn\n"
            "Choose an option: "
        ))

        if choice == 1:
            register.SignUp()

        elif choice == 2:
            user = register.SignIn()

            # Make sure SignIn actually returned a username
            if user is None:
                continue

            # Extra username validation
            if any(word in user.lower() for word in blocked):
                print("Invalid username.")
                status = False
                continue

            # Get the account number safely from the database
            account_number = register.db_query(
                "SELECT account_number FROM customers WHERE username = %s",
                (user,)
            )

            if not account_number:
                print("Could not find your account.")
                status = False
                continue

            status = True
            break

        else:
            print("Please choose either 1 or 2.")

    except ValueError:
        print("Please enter a number.")

# Banking services
while status:

    print(
        f"\nWelcome {user.capitalize()}! "
        "What would you like to do today?\n"
    )

    try:
        facility = int(input(
            "1. Balance Enquiry\n"
            "2. Cash Deposit\n"
            "3. Cash Withdraw\n"
            "4. Fund Transfer\n"
            "5. Exit\n"
            "Choose an option: "
        ))

        if facility == 1:

            bobj = bank.Bank(user, account_number[0][0])
            bobj.balanceequiry()

        elif facility == 2:

            while True:
                try:
                    amount = int(input("Enter amount to deposit: "))

                    if amount <= 0:
                        print("Please enter an amount greater than 0.")
                        continue

                    bobj = bank.Bank(user, account_number[0][0])
                    bobj.deposit(amount)

                    register.mydb.commit()

                    print("Deposit completed successfully.")
                    break

                except ValueError:
                    print("Please enter a valid number.")

        elif facility == 3:

            while True:
                try:
                    amount = int(input("Enter amount to withdraw: "))

                    if amount <= 0:
                        print("Please enter an amount greater than 0.")
                        continue

                    bobj = bank.Bank(user, account_number[0][0])
                    bobj.withdraw(amount)

                    register.mydb.commit()

                    print("Withdrawal completed successfully.")
                    break

                except ValueError:
                    print("Please enter a valid number.")

        elif facility == 4:

            while True:
                try:
                    receive = int(
                        input("Enter receiver account number: ")
                    )

                    amount = int(
                        input("Enter amount to transfer: ")
                    )

                    if receive <= 0 or amount <= 0:
                        print(
                            "Account number and amount "
                            "must be greater than 0."
                        )
                        continue

                    bobj = bank.Bank(user, account_number[0][0])
                    bobj.fundtransfer(receive, amount)

                    register.mydb.commit()

                    print("Transfer completed successfully.")
                    break

                except ValueError:
                    print("Please enter valid numbers.")

        elif facility == 5:

            print("Thanks for using Mohit Banking Project!")
            status = False

        else:
            print("Please choose an option between 1 and 5.")

    except ValueError:
        print("Please enter a valid number.")

