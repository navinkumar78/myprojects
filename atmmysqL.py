import mysql.connector as sql
import random as rand

# Database Connection
conn = sql.connect(host="localhost", user="root", password="naveen", database="atm")
c1 = conn.cursor()

# Function to create a new account
def create():
    account_number = rand.randint(10000000, 99999999)
    name = input("Enter your name: ")
    password = input("Enter your password (numeric): ")

    try:
        # Insert the new account into the database
        query = "INSERT INTO records (ACCONT_NO, PASSWORD, NAME, CR_AMT, BALANCE, WITHDRAWL) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (account_number, password, name, 0, 1000, 0)  # Default balance is 1000
        c1.execute(query, values)
        conn.commit()

        print(f"Account successfully created! Your account number is {account_number}.")
        print("The minimum balance is 1000.")
    except sql.Error as err:
        print(f"Error: {err}")
    finally:
        print("================================================================================")

# Function for user login
def login():
    try:
        account_number = int(input("Enter your account number: "))
        password = input("Enter your password: ")

        # Verify account credentials
        query = "SELECT * FROM records WHERE ACCONT_NO = %s AND PASSWORD = %s"
        c1.execute(query, (account_number, password))
        result = c1.fetchone()

        if result:
            print("Login successful!")
            print("1. Deposit Money")
            print("2. Withdraw Money")
            print("3. Transfer Money")
            print("4. Check Balance")
            print("5. Change Account Number")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                deposit_money(account_number)
            elif choice == 2:
                withdraw_money(account_number)
            elif choice == 3:
                transfer_money(account_number)
            elif choice == 4:
                check_balance(account_number)
            elif choice == 5:
                change_account_number(account_number, password)
            else:
                print("Invalid choice.")
        else:
            print("Invalid account number or password.")
    except ValueError:
        print("Please enter a valid input.")
    except sql.Error as err:
        print(f"Database Error: {err}")
    finally:
        print("================================================================================")

# Function to deposit money
def deposit_money(account_number):
    try:
        amount = int(input("Enter the amount to deposit: "))
        query = "UPDATE records SET CR_AMT = CR_AMT + %s, BALANCE = BALANCE + %s WHERE ACCONT_NO = %s"
        c1.execute(query, (amount, amount, account_number))
        conn.commit()
        print("Money deposited successfully!")
    except sql.Error as err:
        print(f"Error: {err}")

# Function to withdraw money
def withdraw_money(account_number):
    try:
        amount = int(input("Enter the amount to withdraw: "))
        query = "SELECT BALANCE FROM records WHERE ACCONT_NO = %s"
        c1.execute(query, (account_number,))
        balance = c1.fetchone()[0]

        if balance >= amount:
            query = "UPDATE records SET BALANCE = BALANCE - %s, WITHDRAWL = WITHDRAWL + %s WHERE ACCONT_NO = %s"
            c1.execute(query, (amount, amount, account_number))
            conn.commit()
            print("Money withdrawn successfully!")
        else:
            print("Insufficient balance.")
    except sql.Error as err:
        print(f"Error: {err}")

# Function to transfer money
def transfer_money(account_number):
    try:
        target_account = int(input("Enter the account number to transfer to: "))
        amount = int(input("Enter the amount to transfer: "))

        # Check if target account exists
        query = "SELECT BALANCE FROM records WHERE ACCONT_NO = %s"
        c1.execute(query, (target_account,))
        if c1.fetchone() is None:
            print("Target account does not exist.")
            return

        # Check if the current account has sufficient balance
        c1.execute(query, (account_number,))
        balance = c1.fetchone()[0]

        if balance >= amount:
            # Update balances
            query = "UPDATE records SET BALANCE = BALANCE - %s WHERE ACCONT_NO = %s"
            c1.execute(query, (amount, account_number))
            query = "UPDATE records SET BALANCE = BALANCE + %s WHERE ACCONT_NO = %s"
            c1.execute(query, (amount, target_account))
            conn.commit()
            print("Money transferred successfully!")
        else:
            print("Insufficient balance.")
    except sql.Error as err:
        print(f"Error: {err}")

# Function to check balance
def check_balance(account_number):
    try:
        query = "SELECT BALANCE FROM records WHERE ACCONT_NO = %s"
        c1.execute(query, (account_number,))
        balance = c1.fetchone()[0]
        print(f"Your current balance is {balance}.")
    except sql.Error as err:
        print(f"Error: {err}")

# Function to change account number
def change_account_number(account_number, password):
    try:
        new_account_number = int(input("Enter your new account number: "))

        # Check if the new account number already exists
        query = "SELECT * FROM records WHERE ACCONT_NO = %s"
        c1.execute(query, (new_account_number,))
        if c1.fetchone():
            print("This account number is already in use. Please try again.")
        else:
            # Update account number
            query = "UPDATE records SET ACCONT_NO = %s WHERE ACCONT_NO = %s AND PASSWORD = %s"
            c1.execute(query, (new_account_number, account_number, password))
            conn.commit()
            print("Account number changed successfully!")
    except sql.Error as err:
        print(f"Error: {err}")

# Main Menu
print("WELCOME TO OUR ATM")
print("1. Create Account")
print("2. Login")
print("3. Exit")

choice = int(input("Enter your choice: "))
if choice == 1:
    create()
elif choice == 2:
    login()
elif choice == 3:
    print("Thank you for using our ATM service!")
else:
    print("Invalid choice.")
