from bank_external import Customer, BankAccount, SavingsAccount, CheckAccount
import random
import datetime
import platform
import os

def clear_console() -> (None):
    """
    Clear console window for Program User based on a specifc operating system, used for general tidyness purposes.
    """    
    if platform.system() == 'Windows':
        os.system('cls')

    elif platform.system() == 'Linux':
        os.system('clear')

    else:
        print('\n' * 100)

def get_accounts(accounts_txt: str = 'data/accounts.txt', transactions_txt: str = 'data/accountsTransactions.txt') -> (list[BankAccount]):
    """
    takes accounts and transactions from text files; accounts.txt and transactions.txt, creates Bank Account instances
    from the data and returns a list of Bank Account instances

    Args:
        -> accounts_txt (str): text file containing All Bank Account data. Defaults to 'data/accounts.txt'
        -> transactions_txt: (str): text file containing All Transactions in Banking System. Defaults to 'data/accountsTransactions.txt'

    """    
    try:
        accounts = []
        transactions = []
        accObjects = []

        # read accounts from accounts.txt
        with open(accounts_txt, 'r') as f:

            # formats each account from one whole string to an array of strings seperated by ','
            for account in f.readlines():
                account = (account.strip('\n')).split(', ')
                accounts.append(account)
        
        # read transactions from transactions.txt
        with open(transactions_txt, 'r') as g:

            # formats each account from one whole string to an array of strings seperated by ','
            for transaction in g.readlines():
                transaction = transaction.strip('\n').split(', ')
                transactions.append(transaction)
                
    except IOError:
        print(IOError)
        exit()

    # for loop to associate all the transactions for each bank account instance
    for account in accounts:
        accTransactions=[]

        for transaction in transactions:

            # check if the account number in the transaction matches current account instance in for loop
            if account[0] == transaction[1]:
                accTransactions.append(transaction)
            
        # create account instance based on type of account and append to accObjects list
        if account[1] == 'SavingsAccount':
            accObjects.append(SavingsAccount(account[0], float(account[2]), accTransactions))
        else:
            accObjects.append(CheckAccount(account[0], float(account[2]), accTransactions, float(account[3])))

    return accObjects

def get_customers(customer_txt: str = 'data/customers.txt', accounts: list[BankAccount] = get_accounts()) -> (list[Customer]):
    """
    Function to return a list of all the customers in the system as Customer objects 

    Args:
        -> customer_txt (str): text file containing all customer data in Bank System. Defaults to 'data/customers.txt'
        -> accounts (list[BankAccount]): list of all Account instances in Bank System. Defaults to method get_accounts().
    """ 
    try:
        customers = []
        custObjects = []

        # read customers from customers.txt
        with open(customer_txt, 'r') as f:

            # formats each customer from one whole string to an array of strings seperated by ','
            for customer in f.readlines():
                customers.append((customer.strip('\n')).split(', '))

    except IOError:
        print(f"File {customer_txt} does not exist.")
        exit()

    # for loop to associate all the accounts owned by each customer instance
    for customer in customers:
        custAccounts = []

        ''' data in text file cleaned so as to define accounts from the 7th index onwards -> assumption that one customer can have multiple accounts '''

        # if statement to check if customer has at least one account, check if the data elements associated with current customer in loop has more than 7 elements (i.e there exists accounts)
        if len(customer) > 7:

            # for loop to check if a account instance can be associated with current customer within loop by match of account number
            for account in accounts:     

                # for loop to check each customer element from the 7th index to the length of elements
                for i in range(7, len(customer)):
                    if customer[i] == account.account_number:
                        custAccounts.append(account)

        # create customer instance with their associated accounts and append to list of customer objects
        custObjects.append(Customer( int(customer[0]), customer[1], customer[2], datetime.date(int(customer[3]), int(customer[4]), int(customer[5])), customer[6], custAccounts))

    return custObjects

def create_account(customer : Customer) -> (None):
    """
    creates new Bank Account instance for a customer instance; allows user to select type of bank account, i.e selection between Savings Account and Check Account. Displays a menu to select by type of account
    and in the case of check account selection, allows user to define credit limit. Uses sub class methods for further and final validation.

    Args:
        -> customer (Customer): customer instance to create new account instance for
    """    
    clear_console()

    # while loop to maintain GUI interface environment (in case of non-perfect user input)
    while True:
        try:
            accType = int(input("\n2 Types of Accounts are available:\n\nEnter (1) for Savings Account\nEnter (2) for Check Account *(18 and older to qualify)\n\nEnter (3) to return to your Bank\n"))

            # generate a unique customer number using the method generate_account_number()
            newAcc_number = generate_account_number()

            ''' if statements to direct based on input from menu '''

            # add a new Savings Bank Account
            if accType == 1:
                customer.add_account(SavingsAccount(newAcc_number))          
            
            # add a new Check Bank Account
            elif accType == 2:
                if customer.age >= 18:
                    while True:
                        try:
                            # get credit limit from user (usually defined by bank -> program allows user to select a limit within specific bounds)
                            get_limit = float(input('\nEnter a credit limit for your Check Account *(credit limit must be greater than 50 but smaller than 5000):\n-> '))

                            # check if credit limit falls between min and max bounds
                            if 50 <= get_limit <= 5000:
                                customer.add_account(CheckAccount(newAcc_number, credit_limit=get_limit))
                                return
                            else:
                                print('Input Error, Credit Limit must be between 50 and 5000\n')

                        except ValueError:
                            print('Input Error, Try again\n')
                            continue
                else:
                    print('\nError, You dont meet the requirements to create a Check Account\n')
                    continue

            # return bank to bank menu
            elif accType == 3:
                my_bank(customer)

            else:
                print('\nError, Select a valid option from the menu\n')
                continue

            # upon success of account creation display new account number
            print('\nSuccess, your new Bank Account number is: ' + newAcc_number)
            my_bank(customer)  

        except ValueError:
            print('\nInput Error, Try again')

def delete_account(customer : Customer) -> (None):
    """
    Deletes a Bank Account instance from a given customer instance; displays a menu with all customer instance accounts and gets user input to select an account to be deleted. Further validation
    is done to check if conditions are met for the deletion of a account instances, i.e if there are still funds associated within the account. 

    ** An account may not be deleted if there are still funds allocated with the account. **

    Args:
        -> customer (Customer): customer instance to delete specific account instance from
    """     
    clear_console()
    
    # while loop to maintain GUI interface environment (in case of non-perfect user input)
    while True:
        print(f'\nDelete a Bank Account:\n')
        i = 1

        # display current customer instance's bank accounts
        for account in customer.get_accounts():

            # if statement to check if account is a Savings / Check account
            if isinstance(account, SavingsAccount):
                print(f'{i} - {account.account_number} - Savings Account')
            else:
                print(f'{i} - {account.account_number} - Check Account')
            i += 1

        print(f'\n{i} - Return to Bank Accounts and Services\n0 - Logout\n')

        try:
            selDel = int(input(f'Select a Bank Account to delete from the menu\n\n-> '))       

            if 0 < selDel < i:

                # if statement to check if current account selected still has any funds associated with it -> if it does have funds associated with it, it is undeletable
                if (customer.get_accounts()[selDel - 1]).get_funds() != 0:

                    # while loop to maintain GUI interface environment (in case of non-perfect user input)
                    while True:

                        # display account number and notify user that funds are still allocated to account
                        print(f'\nError, Account: {(customer.get_accounts())[selDel-1].account_number} still has funds associated with it\n')

                        # create menu to manage specific account or cancel
                        try:
                            cont = int(input(f'\nEnter (1) to Manage Account {customer.get_accounts()[selDel-1].account_number}\nEnter (2) to Return to Your Accounts and Services\nEnter (3) to return to Delete Menu\n\n-> '))

                            # if statement to manage specific bank account
                            if cont == 1:
                                manage_bank_account((customer.get_accounts())[selDel - 1])

                            # if statement to return back to main bank menu
                            elif cont == 2:
                                my_bank(customer)

                            # if statement to return to deletion menu
                            elif cont == 3:
                                break
                            else:
                                print('\nError, Select a valid option from the menu\n')
                                continue

                        except ValueError:
                            print('\nInvalid Input, only numeric input allowed')
                            continue
                else:
                    # while loop to maintain GUI interface environment (in case of non-perfect user input)
                    while True:
                        try:

                            # menu to confirm deletion of selected account
                            confirm = int(input(f'\nAre you sure you want to delete Account: {customer.get_accounts()[selDel - 1].account_number}?\nEnter (1) - YES\nEnter (0) - NO\n\n-> '))

                            if confirm == 1:
                                # save the accont to be deleted's accout number to delAcc
                                delAcc = (customer.get_accounts())[selDel-1].account_number

                                # pass the selected account instance to the customer class method delete_cust_account()
                                customer.delete_cust_account((customer.get_accounts())[selDel-1])

                                print(f'\nSuccess, Your Account: {delAcc} was deleted.\n')
                                break

                            # return back to delete menu
                            elif confirm == 0:
                                break
                            else:
                                print('\nError, Select a valid option from the menu\n')
                                continue

                        except ValueError:
                            print('Invalid Input, only numeric input allowed')
                            continue

            # returns back to customer bank menu
            elif selDel == i:
                return
            
            # exits program
            elif selDel == 0:
                exit()
            else:
                print('\nError, Select a valid option from the menu\n')
                continue

        except ValueError:
            print('\nInvalid Input, only numeric input allowed') 
            continue
        
def create_customer() -> (None):
    """
    Gets all information for a new 'Registering' Customer. Does validation on All Input
    """    
    # while loop to maintain GUI interface environment (in case of non-perfect user input)
    while True:
        
        print('\nEnter your Information:')        
        customer_id = len(myCustomers) + 1

        cust_name = input('\nEnter your first name: ').strip()
        cust_surname = input('\nEnter your last name: ').strip()

        if not cust_name or cust_name.isnumeric() or not cust_surname or cust_surname.isnumeric():
            print('Error, Invalid Input\n')
            continue

        cust_dob = input('\nEnter your Date of Birth AS yyyy/mm/dd: ')

        # attempt to cast given date of birth inputted by user to datetime.datetime object
        try:
            dob = datetime.datetime.strptime(cust_dob, '%Y/%m/%d')
           
        except ValueError:
            print('\nError, Invalid Date Input -> Format should be yyyy/mm/dd\n')
            continue
        
        cust_address_street = input('\nAddress Section\n\nStreet Address: ').strip()
        cust_address_city = input('\nCity: ').strip()
        cust_address_post = input('\nEircode/Postal: ').strip()      

        # check if addresses are empty
        if not cust_address_street or not cust_address_city or not cust_address_post:
            print('\nError, Empty Input\n')
            continue
        else:
            customer_address = f'{cust_address_street} {cust_address_city} {cust_address_post}'

        # remove any unwanted character input
        for c in customer_address:
            if c in '()[]{}<>/.,!@#$%^&)_+|':
                customer_address = customer_address.replace(c, '') 

        # append new customer instance to list of all customer instances in system
        myCustomers.append(Customer(int(customer_id), cust_name, cust_surname, dob, customer_address))
        
        # append new customer to customers text file in appropriate string format
        customer = f'{str(customer_id)}, {cust_name}, {cust_surname}, {dob.year}, {dob.month}, {dob.day}, {customer_address}\n'
        with open('data/customers.txt', mode='a') as f:
            f.write(customer)
        
        # clear console
        clear_console()

        print(f'\n\nSuccess... Welcome to Galactic Bank, {cust_name} - Your user IDENTIFIER is: {customer_id}\n\n')

        # while loop to maintain GUI interface environment (in case of non-perfect user input)
        while True:
            try:
                # allow user to exit system or login with new identifier
                leave = int(input('\nEnter (1) to return to the main menu\nEnter (2) to Exit\n'))

                if leave == 1:
                    main()
                    
                elif leave == 2:
                    exit()

                else:
                    print('\nInvalid option, enter a option from the menu\n')

            except ValueError:
                print('\nInvalid Input, only numeric input allowed')
                continue

def generate_account_number() -> (str):
    """
    Generates a 8 digit random account number and Checks if it is unique given all current active account instances within the system.

    Returns:
        str: 8-digit numeric account number
    """    
    # randoms a number between 0, 99999999, cast to string and if the number length is smaller than 9, fills them with zeroes -> NOTE: (could lead to repeating account numbers like 11111111 or 000000000, Low probability)
    account_number = str(random.randint(0,99999999)).zfill(8)

    for account in myAccounts:
        # if account number does exist regenerate new account number
        if account_number == str(account.account_number):
            generate_account_number()
    
    return account_number   
    
def manage_bank_account(account : BankAccount) -> (None):
    """
    Acts as the main menu from which to manage a specific instance of a Bank Account. Allows the fundamental class method operations such as Deposit, Withdraw and Transfer. Allows the user
    to view all of their transactions too.

    Args:
        account (BankAccount): a customer's account instance
    """    
    # while loop to maintain GUI interface environment (in case of non-perfect user input)
    while True:
        try:
            # check type of Bank Account instance
            if isinstance(account, SavingsAccount):
                print(f"\n\nSavings Account - Account: {account.account_number}")
            else:
                print(f"\n\nCheck Account - Account: {account.account_number}")

            # display menu
            print("\nSelect a option from the menu:\n")

            # get menu choice
            decision = int(input("Enter (1) to View Transactions\nEnter (2) to Deposit\nEnter (3) to Withdraw\nEnter (4) to Transfer\nEnter (5) to Cancel\n\n-> "))

            # display transactions in table format
            if decision == 1:
                print("\n\n| {:^20} | {:^20} | {:^20} | {:^20}".format('Transaction Number:', 'Amount:', 'Date:', 'Transaction Type:'))

                # checks if transactions have been performed by the account yet
                if len(account.get_transactions()) > 0:
                    i = 1
        
                    # for loop to get each transaction from the instance account
                    for transaction in account.get_transactions():

                        # string format and display each transaction in table
                        print("| {:^20} | {:^20} | {:^20} | {:^20}".format(i, transaction[2], transaction[3], transaction[4]))

                        i += 1

                    print(f'\nFUNDS: {account.get_funds()}\n')

                else:
                    print('\nNo Transaction Data...\n')

            # deposit money
            elif decision == 2:
                depositAmount = float(input('\nEnter amount to deposit: \n'))
                account.deposit(depositAmount)
                print(f'\nSuccess, {depositAmount} was Deposited in to your account.')

            # withdraw money
            elif decision == 3:
                withdrawAmount = float(input('\nEnter amount to withdraw: '))
                funds = account.get_funds()
                account.withdraw(withdrawAmount)

                if account.get_funds() < funds:
                    print(f'\nSuccess, {withdrawAmount} was Withdrawn from your account.')

            # transfer funds
            elif decision == 4:
                accExist = False

                # get transfer amount and recipient account number
                transferAmount = float(input('\nEnter amount to Transfer: '))
                transfer_account_number = input('\nEnter Transfer Recipient Account Number: ')

                # store instance account old funds value
                funds = account.get_funds()

                # check if entered account does exist
                for acc in myAccounts:
                    if acc.account_number == transfer_account_number:
                        accExist = True
                        account.transfer(transferAmount, acc)    
                        break   # break to stop searching
                        
                # if statement if account number does not exist
                if accExist != True:
                    print('\nInvalid Account Number, Try Again\n')
                    continue
            
                # display success if funds changed
                if account.get_funds() < funds:
                    print(f'\nSuccess, {transferAmount} was succesfully transferred to Account: {transfer_account_number}')

            # return to back to menu
            elif decision == 5:
                clear_console()
                return

            else:
                print('\nInvalid option, enter a option from the menu\n')
                continue
                
        except ValueError:
            print("\nInvalid Input, only numeric input allowed\n")
            continue

def my_bank(customer : Customer) -> (None):
    """
    Acts as the main menu from which a customer instance can create, delete, view and select their bank account instances. If a customer does not have a Bank Account yet, they can use
    this menu to create a new bank account.

    Args:
        customer (Customer): a customer instance in the Bank System
    """  
    clear_console()

    # while loop to maintain GUI interface environment (in case of non-perfect user input)
    while True:
        print(f'Welcome, {customer.name}\n')

        # if statement to check if customer currently has any accounts
        if not len(customer.get_accounts()):
            
            # menu to allow customer to create a Bank Account -> directs create_account() function
            try:
                createAccount = int(input("You have no Bank Accounts:\n\nEnter (1) to Create a new Bank Account\nEnter (2) to return back to Main Menu\n\n-> "))
                
                # create bank account
                if createAccount == 1:
                    create_account(customer)                    
                
                # return back to 'login' menu
                elif createAccount == 2:
                    main()
                else:
                    print('\nSelect a valid option from the menu\n\n')
                    continue

            except ValueError:
                print('\nInput Error, Try again\n')
                continue
    
        else:
            # display customer instance active accounts
            print(f"Your Active Accounts are:\n")
            i = 1

            # for loop to display each account with their type
            for account in customer.get_accounts():
                if isinstance(account, SavingsAccount):
                    print(f'{i} - {account.account_number} - Savings Account')
                else:
                    print(f'{i} - {account.account_number} - Check Account')

                i += 1

            print(f'\n{i} - Create a new Bank Account\n{i + 1} - Delete Existing Bank Account\n0 - Logout\n')

            try:
                getAccount = int(input(f'Select an option from the menu\n\n-> '))

                # if statement for customer to select bank account to be managed/deleted or to create a new bank account

                # manage selected bank account
                if 0 < getAccount < i:
                    manage_bank_account(customer.get_accounts()[getAccount - 1])

                # create new bank account for customer instance
                elif getAccount == i:
                    create_account(customer)

                # delete a bank account 
                elif getAccount == i + 1:
                    delete_account(customer)

                # return to 'login' menu
                elif getAccount == 0:
                    main()
                else:
                    print('\nError, Select a valid option from the menu\n')
                    continue

            except ValueError:
                print('\nInput Error, Try again\n')
                continue

def main() -> (None):
    """
    This is the login/main menu for the Bank System. A program user can use this menu to login to their 'customer instance' using their customer identifier, from where they 
    then can view and manage their bank accounts. They can also register a new customer instance.
    """    
    clear_console()

    # while loop to maintain GUI interface environment (in case of non-perfect user input)
    while True:
        
        # display login/register menu
        print('\nWelcome to Galactic Bank \n')
        
        try:
            isCustomer = int(input('Enter (1) to Login\nEnter (2) to Register\nEnter (3) to Exit :(\n\n-> '))

            # login based on customer identifier
            if isCustomer == 1:
                customerID = int(input('\nEnter your UNIQUE Customer ID:\n\n-> '))

                # check if customer instance exists
                for customer in myCustomers:
                    if customerID == customer.get_custID():
                        my_bank(customer)

                print('\nUnable to find your data, try again\n')
                continue
            
            # create new customer instance
            elif isCustomer == 2:
                create_customer()
            
            # exit program
            elif isCustomer == 3:
                print('\nGood Bye :)')
                exit()
            else:
                print('\nInvalid Input, Choose any option from the menu')
                continue
                
        except ValueError:
            print('\nInput Error, Try again\n')

# initialize data and start program
myAccounts = get_accounts()
myCustomers = get_customers()
main()
