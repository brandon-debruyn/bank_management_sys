import datetime

today = datetime.date.today() # global variable to permanantly store the date of day of program execution

class BankAccount(object):
    """
    A class to represent a Bank Account

    ** This class acts as a superclass for classes; SavingsAccount and CheckAccount
    
    Constructor Args:
        -> account_number (str): A Unique Bank Account Identifier
        -> funds (float): The total funds allocated to the Bank Account. Defaults to 0.0   
        -> transaction_history (list): A list that contains all the transactions that involves the said Bank Account. Defaults to None

    """    
    COUNTRY = 'IE'
    CHECK_DIGIT = '69'
    BANK_CODE = 'GBIK'     
    BRANCH_CODE = '123456' 

    def __init__(self, account_number: str, funds: float = 0.0, transaction_history: list = None) -> (None): 
        """
        constructor method for class Bank Account

        Args:
        -> account_number (str): A Unique Bank Account Identifier
        -> funds (float): The total funds allocated to the Bank Account. Defaults to 0.0   
        -> transaction_history (list): A list that contains all the transactions that involves the said Bank Account. Defaults to None
        """ 
        self.account_number = account_number
        self._funds = funds
        self.iban = self.COUNTRY + self.CHECK_DIGIT + self.BANK_CODE + self.BRANCH_CODE + self.account_number
        
        if transaction_history is None:
            self._transaction_history = []
        else:
            self._transaction_history = transaction_history

    def set_funds(self, funds: float) -> (None): 
        """
        set method to set the protected variable funds to a new value (arg) funds

        Args:
            -> funds (float): update float value to set _funds to

        """        
        self._funds = funds

    def get_funds(self) -> (float):
        """
        get method to return the value of the protected variable funds

        Returns:
            -> float: funds is a float value
        """        
        return self._funds

    def get_transactions(self) -> (list[str]): 
        """
        get method to return the protected list of transactions associated with the bank account

        Returns:
            -> list: list of strings of all the transactions
        """        
        return self._transaction_history
        
    def _file_index(self, file_name: str) -> (int):
        """
        method that finds the final index within a given file (file_name: str)

        Args:
            -> file_name (str): text file to find index for

        Returns:
            -> int: returns the index of the final item in the text file
        """        
        # try-except to catch file name error  
        try:     
            with open(file_name, 'r') as f:
                num_lines = len([line.strip('\n') for line in f.readlines() if line != '\n']) 
           
            return num_lines

        except IOError as file_unidentified:
            print(file_unidentified)
            
    def deposit(self, amount: float) -> (None):
        """
        method to deposit money into a given Bank Account, updates text files; accounts and transactions
        with updated values

        Args:
            -> amount (float): amount to be added to current funds
        """ 
        # check for non-negative input       
        if amount > 0: 

            with open('data/accounts.txt', mode='r') as f:  

                new_accounts = []

                '''
                for loop to read and modify a specific account that matches the current instance's bank account number.
                if a match is found, the specific account gets modified to the updated funds value within the accounts.txt file
                '''
                for account in f.readlines():        
                    # check if instance bank account number matches with current account in the loop 
                    if str(self.account_number) in account: 

                        # if account number matched -> funds gets replaced with added funds
                        account = account.replace(str(self._funds), str(self._funds + amount), 1) 
                    
                    new_accounts.append(account) 

            # writing all accounts back to the accounts text file
            with open('data/accounts.txt', mode='w') as f:
                for account in new_accounts:
                    f.write(account)           
           
            self._funds += amount

            # appending deposit transaction to text accountsTransactions.txt
            with open('data/accountsTransactions.txt', mode='a+') as g:

                # using the protected _file_index method to get the appropriate index of last transaction made in the text file accountsTransactions.txt
                i = self._file_index('data/accountsTransactions.txt')

                # define transaction string format appropriatly for writing and write transaction
                transaction = f'{i + 1}, {self.account_number}, +{amount}, {today}, deposit\n'
                g.write(transaction)

                # append transaction to protected instance attribute transaction history
                transaction = [str(i+1), self.account_number, '+' + str(amount), str(today), 'deposit']
                self._transaction_history.append(transaction)
                                    
    def withdraw(self, amount: float) -> (None):
        """
        method to withdraw money from a given Bank Account, updates databases i.e updates accounts and 
        transactions text files with updated values

        Args:
            -> amount (float): amount to be subtracted from current instance funds attribute
        """        
        if amount > 0:
            with open('data/accounts.txt', mode='r') as f:
                new_accounts = []

                '''
                    for loop to read and modify a specific account that matches the current instance's bank account number.
                    if a match is found, the specific account gets modified to the updated funds value within the accounts.txt file
                '''
                for account in f.readlines():
                    if self.account_number in account:

                        # if account number matched, modify account -> funds gets replaced with updated subtracted funds
                        account = account.replace(str(self._funds), str(self._funds - amount), 1)

                    new_accounts.append(account)

            # writing all accounts back to the accounts text file
            with open('data/accounts.txt', mode='w') as f:
                for account in new_accounts:
                    f.write(account)

            # update instance attribute funds
            self._funds -= amount

            # appending withdraw transaction to text accountsTransactions.txt
            with open('data/accountsTransactions.txt', mode='a') as g:

                # using the protected _file_index method to get the appropriate index of last transaction made in the text file accountsTransactions.txt
                i = self._file_index('data/accountsTransactions.txt')

                # define transaction string format appropriatly for writing and write transaction
                transaction_txt = f'{i + 1}, {self.account_number}, -{amount}, {today}, withdrawal\n'
                g.write(transaction_txt)

                # append to protected instance attribute transaction history
                transaction = [str(i + 1), self.account_number, '-' + str(amount), str(today), 'withdrawal']
                self._transaction_history.append(transaction)
        else:
            print('\nError, Invalid Amount\n')

    def transfer(self, amount: float, recipAccount) -> (None):
        """
        method to transfer money from instance to another instance, updates text files; accounts and 
        accountTransactions with updated funds values

        Args:
            -> amount (float): amount to be transferred from current instance bank account
            -> recipAccount (BankAccount): BankAccount instance that receives transfer from current instance
        """        

        # check for non-negative input 
        if amount > 0:
    
            with open('data/accounts.txt', mode='r') as f:
                new_accounts = []

                '''
                for loop to read and modify a specific account that matches the recipient object's bank account number.
                if a match is found, the specific account gets modified to the updated funds value within the accounts.txt file
                '''
                for account in f.readlines():

                    # check if recipient bank account number matches with current account in the loop 
                    if recipAccount.account_number in account:

                        # if account number matched -> funds gets replaced with added funds
                        account = account.replace(str(recipAccount.get_funds()), str(recipAccount.get_funds() + amount), 1)
                    
                    # check if (self)instance account number m atches with current account in loop
                    elif self.account_number in account:
                        # if account number matched -> funds gets replaced with added funds
                        account = account.replace(str(self._funds), str(self._funds + amount), 1)

                    new_accounts.append(account)

            # writing all accounts back to the accounts text file
            with open('data/accounts.txt', mode='w') as f:
                for account in new_accounts:
                    f.write(account)           
           
            # update current instance funds and use recipient instance's set funds class method to update(set) its protected funds attribute 
            self._funds -= amount
            recipAccount.set_funds(recipAccount.get_funds() + amount)

            # appending transfer transaction to text accountsTransactions.txt
            with open('data/accountsTransactions.txt', mode='a+') as g:

                # using the protected _file_index method to get the appropriate index of last transaction made in the text file
                i = self._file_index('data/accountsTransactions.txt')
                
                # define transaction string format appropriatly for writing and write transaction
                transaction = f'{i + 1}, {self.account_number}, -{amount}, {today}, transfer to {recipAccount.account_number}\n{i + 2}, {recipAccount.account_number}, +{amount}, {today}, transfer from {self.account_number}\n'
                g.writelines(transaction)

                # append to both current Bank Account instance and Recipient Bank Account protected attribute transaction history 
                transaction_to = [str(i + 1), self.account_number, '-' + str(amount), str(today), f'transfer to {recipAccount.account_number}']
                self._transaction_history.append(transaction_to)
                
                transaction_from = [str(i + 2), self.account_number, '+' + str(amount), str(today), f'transfer from {self.account_number}']
                recipAccount.get_transactions().append(transaction_from)
        else:
            print('\nError, Invalid Amount\n')

    def __str__(self) -> (str):
        """
        convert instance to string -> displays non-sensitive account information
        """        
        return f"Account Number: {self.account_number}\nIBAN: {self.iban}\n"


class SavingsAccount(BankAccount):
    """
    Subclass of class Bank Account to represent a Savings Account at a bank. Some superclass methods
    are modified -> withdraw, transfer. Added methods are -> num_withdrawl_transfers
    
    Constructor Args:
        -> account_number (str): A Unique Bank Account Identifier
        -> funds (float): The total funds allocated to the Bank Account. Defaults to 0.0   
        -> transaction_history (list): A list that contains all the transactions that involves the said Bank Account. Defaults to None
    """    

    def __init__(self, account_number: float = None, funds: float = 0.0, transaction_history: list = None) -> (None):
        BankAccount.__init__(self, account_number, funds, transaction_history)
        """
        Constructor for class Savings Account

        Args:
            -> account_number (str): A Unique Bank Account Identifier
            -> funds (float): The total funds allocated to the Bank Account. Defaults to 0.0   
            -> transaction_history (list): A list that contains all the transactions that involves the said Bank Account. Defaults to None
        """        

    def __num_withdrawal_transfers(self) -> (bool):
        """
        method to find total amount of transactions performed using this instance. Used to satisfy system
        requirement to limit number of transactions a month to 1.

        ** Does not include deposit transactions

        Returns:
            -> bool: True or False -> transactions performed exceeds allowed limit
        """        
        transfer_limt = False

        # for loop used to check dates on transactions
        for transaction in self._transaction_history:

            # cast transaction date into datetime object
            date_obj = datetime.datetime.strptime(transaction[3], '%Y-%m-%d')

            # check if current month matches transaction date and if transaction methods are withdrawl or transfer
            if today.month == date_obj.month and (transaction[4] == 'withdrawal' or transaction[4] == 'transfer'):
                transfer_limt = True
                break

        return transfer_limt

    def withdraw(self, amount: float) -> (BankAccount.withdraw):
        """
        identical method to superclass method withdraw, just added max withdrawl/transfer limit requirement and non-negative validation 
        
        Args:
            -> amount (float): amount to be withdrawn from current instance account
        """        
        # if statement to check if there's sufficient funds for a withdrawl and also check num monthly withdrawls
        if(self._funds - amount) > 0 and not self.__num_withdrawal_transfers():
            return BankAccount.withdraw(self, amount)
        else:
            print('\n\nMonthly withdrawal limit reached')
           
    def transfer(self, amount: float, recipAccount : BankAccount) -> (None):
        """
        identical method to superclass method withdraw, just added max withdrawl/transfer limit requirement and non-negative validation 

        Args:
            -> amount (float): amount to be transfered from current instance account
            -> recipAccount (BankAccount): recipient instance to receive funds
        """     
        # if statement to check if there's sufficient funds for a withdrawl and also check num monthly withdrawls
        if(self._funds - amount) > 0 and not self.__num_withdrawal_transfers():
            BankAccount.transfer(self, amount, recipAccount)
        else:
            print('\n\nMonthly transfer limit reached')  

class CheckAccount(BankAccount):
    """
    Subclass of class Bank Account to represent a Savings Account at a bank. Some superclass methods
    are modified -> withdraw, transfer. Added methods are -> num_withdrawl_transfers
    
    Constructor Args:
            -> account_number (str): A Unique Bank Account Identifier
            -> funds (float): The total funds allocated to the Bank Account. Defaults to 0.0   
            -> transaction_history (list): A list that contains all the transactions that involves the said Bank Account. Defaults to None
            -> credit_limit (float): The maximum credit allowed by the account. Defaults to a credit of 50
    """    

    def __init__(self, account_number:str = None, funds: float = 0.0, transaction_history: list = None, credit_limit: float = 50.0) -> (None):
        BankAccount.__init__(self, account_number, funds, transaction_history)
        """
        Constructor for class Check Account

        Args:
            -> account_number (str): A Unique Bank Account Identifier
            -> funds (float): The total funds allocated to the Bank Account. Defaults to 0.0   
            -> transaction_history (list): A list that contains all the transactions that involves the said Bank Account. Defaults to None
            -> credit_limit (float): The maximum credit allowed by the account. Defaults to a credit of 50
        """    
        # if statement to convert credit limit to negative value
        if credit_limit > 0:
            credit_limit = credit_limit * -1
            self.__credit_limit = credit_limit
        else:
            self.__credit_limit = credit_limit
    
    def withdraw(self, amount: float) -> (BankAccount.withdraw):
        """
        identical method to superclass method withdraw, just added max withdrawl/transfer limit requirement and non-negative validation 
        
        Args:
            -> amount (float): amount to be withdrawn from current instance account
        """      
        # if statement to check if withdrawl falls within the credit limit
        if(self._funds - amount) > self.__credit_limit:
            return BankAccount.withdraw(self, amount)
        else:
            print('\nTransaction exceeds Credit Limit\n')

    def get_credit_limit(self) -> (float):
        """
        get method to return private instance credit limit

        Returns:
            -> float: max credit allowed for instance
        """        
        return self.__credit_limit

    def transfer(self, amount: float, recipAccount : BankAccount) -> (None):
        """
        identical method to superclass(BankAccount) method withdraw, added credit check

        Args:
            -> amount (float): amount to be transfered from current instance account
            -> recipAccount (BankAccount): recipient instance to receive funds
        """     

        # if statement to check if transfer falls within instance credit limit
        if(self._funds - amount) > self.__credit_limit:
            BankAccount.transfer(self, amount, recipAccount)
        else:
            print('\nTransaction Exceeds Credit Limit\n')


class Customer(object):
    """
    A class to represent a customer in a Bank Management System. 

    Constructor Args:
        -> customer_id (int): A unique Customer identifier
        -> name (str): Name of customer
        -> surname (str): Surname of customer
        -> dob (datetime.datetime): stores customer date of birth as datetime.datime object
        -> address (str): living address of customer
        -> accounts (list): list of customer bank account objects
    """   

    def __init__(self, customer_id: int = 0, name: str = None, surname: str = None, dob: datetime.datetime = None, address:str = None, accounts: list[BankAccount] = None) -> (None):
        """
        Customer constructor method

        Constructor Args:
        -> customer_id (int): A unique Customer identifier
        -> name (str): Name of customer
        -> surname (str): Surname of customer
        -> dob (datetime.datetime): stores customer date of birth as datetime.datime object
        -> address (str): living address of customer
        -> accounts (list): list of customer bank account objects
        """        
        self.__customer_id = customer_id
        self.name = name
        self.surname = surname
        self.__dob = dob
        self.__address = address
        
        if accounts is None:
            self.__accounts = []
        else:
            self.__accounts = accounts

        # initializes age of instance based upon current date and given date of birth
        age = today.year - self.__dob.year

        # check if birth day has already occured within year of execution (if birthday is yet to occur, hence age - 1)
        if today < datetime.date(today.year, self.__dob.month, self.__dob.day):
            age -= 1
        
        self.age = age

    def get_custID(self) -> (int):
        """
        get method to return instance customer ID

        Returns:
            (int): unique customer identifier defined as integer
        """        
        return self.__customer_id

    def get_accounts(self) -> (list[BankAccount]):
        """
        get method to return list of instance's list of bank account instances

        Returns:
            (list[BankAccount]): list of bank accounts associated with instance
        """        
        return self.__accounts

    def add_account(self, account: BankAccount) -> (None):
        """
        adds a new account object to instance's list of accounts

        Args:
            account (BankAccount): BankAccount instance to be added to protected class attribute accounts
        """        

        # if statement to check if account is an instance of subclass SavingsAccount and customer has an age of 14 or older
        if isinstance(account, SavingsAccount) and self.age >= 14:
            
            # read all customer data from customers.txt
            with open('data/customers.txt', 'r') as g:
                new_customers = []

                # for loop to get specific customer in customers.txt file that matches current instance customer id
                for customer in g.readlines():
                    
                    # if statement to check if customer at specific line in text, matches instance customer id
                    if ((customer.strip('\n')).split(', '))[0] == str(self.__customer_id): # TEST

                        # modify string format of current instance
                        customer = customer.strip('\n') + f', {account.account_number}\n'
                        
                    new_customers.append(customer)
            
            # write updated instance and customers back into customers.txt
            with open('data/customers.txt', 'w') as g:
                for customer in new_customers:
                    g.write(customer)

            # append new account to protected class list attribute, accounts
            self.__accounts.append(account)

            # append new account to accounts.txt in appropriate string format
            with open('data/accounts.txt', 'a+') as f:
                account_info = f'{account.account_number}, SavingsAccount, {account.get_funds()}\n'
                f.write(account_info)

        # if statement to check if account is an instance of subclass CheckAccount and customer has an age of 18 or older
        elif isinstance(account, CheckAccount):

            # read all customer data from customers.txt
            with open('data/customers.txt', 'r') as f:
                new_customers = []

                # for loop to get specific customer in customers.txt file that matches current instance customer id
                for customer in f.readlines():
                    #customer_data = (customer.strip('\n')).split(', ')
                    # if statement to check if formatted customer at specific line in text matches instance customer id
                    if ((customer.strip('\n')).split(', '))[0] == str(self.__customer_id):

                        # modify string format of current instance
                        customer = customer.strip('\n') + f', {account.account_number}\n'
                        
                    new_customers.append(customer)
            
            # write updated instance and customers back into customers.txt
            with open('data/customers.txt', 'w') as f:
                for customer in new_customers:
                    f.write(customer)

            # append new account to protected class list attribute, accounts
            self.__accounts.append(account)

            # append new account to accounts.txt in appropriate string format
            with open('data/accounts.txt', 'a+') as g:
                account_info = f'{account.account_number}, CheckAccount, {account.get_funds()}, {account.get_credit_limit()}\n'
                g.write(account_info)

        else: 

            print(f"{account} is not an instance of BankAccount")

    def delete_cust_account(self, account : BankAccount) -> (None):
        """
        deletes account object from instance's list of accounts

        Args:
            account (BankAccount): account object associated with instance to be remove from protected class attribute accounts
        """        
        # read all account data from accounts.txt
        with open('data/accounts.txt', mode='r') as f:
            new_accounts = []

            # for loop to find account to be deleted in accounts.txt
            for acc in f.readlines():

                # if statement to skip over (prevent) account from being appended to new_accounts array
                if account.account_number in acc:
                    continue

                new_accounts.append(acc)

        # read all customer data from customers.txt
        with open('data/customers.txt', mode='r') as g:      
            new_customers = []

            # for loop to find current instance's data in customers.txt
            for cust in g.readlines():

                # if statement to modify instance's data
                if account.account_number in cust:
                    pre_cust = ((cust.strip('\n')).split(', '))
                    pre_cust.remove(account.account_number)
                    cust = (', '.join(pre_cust)) + '\n'
                    
                new_customers.append(cust)
        
        # removes account from protected list class attributes
        self.__accounts.remove(account)

        # write back all account and customer updated data
        with open('data/accounts.txt', mode='w') as f:
            for acc in new_accounts:
                f.write(acc)

        with open('data/customers.txt', mode='w') as g:
            for cust in new_customers:
                g.write(cust)

    def __str__(self) -> (str):
        """
        convert instance to string -> displays non-sensitive customer information
        """     
        return f'Name: {self.name}\nSurname: {self.surname}\nAge: {self.age}\nAddress: {self.__address}\n'