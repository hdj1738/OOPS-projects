from abc import ABC,abstractmethod
import csv
import io

class Customer:
    def __init__(self,name,customer_id,phone_number):
        self.name=name
        self.__customer_id=customer_id
        self.phone_number=phone_number
    def get_customerid(self):
        return self.__customer_id
    

class Bank_Account(ABC):
    def __init__(self,account_number,account_holder,balance,account_type):
        self.__account_number=account_number
        self.account_holder=account_holder #tis the customer
        self.__balance=balance
        self.account_type=account_type
        self.transaction_history=[]

    def __str__(self):
        return f"customer ID:{self.account_holder.get_customerid()} account number:{self.get_accountnumber()} account type:{self.account_type} customer:{self.account_holder.name} balance:{self.checkbalance()}"
    
    def get_accountnumber(self):
        return self.__account_number
    def checkbalance(self):
        return self.__balance
    def deposit(self,deposit_amount):
        if deposit_amount>0:
            self.__balance+=deposit_amount
            print("Deposit successful. Current balance:",self.checkbalance())
            self.transaction_history.append(f"deposited: +{deposit_amount}")
            return True
        print("Deposit failed. Current balance:",self.checkbalance())
        return False

    #The parent class should give the shared withdrawal operation; subclasses provide the rule.
    @abstractmethod
    def can_withdraw(self,withdraw_amount):
        pass
    #every concrete account type must implement its own withdrawal check
    
    def withdraw(self, withdraw_amount):
        if self.can_withdraw(withdraw_amount):
            self.__balance -= withdraw_amount
            print(f"Withdrawal successful. Current balance: {self.checkbalance()}")
            self.transaction_history.append(f"withdrawn: -{withdraw_amount}")
            return True
        print(f"Withdrawal failed. Current balance: {self.checkbalance()}")
        return False
        
    def display_transaction_history(self):
        if self.transaction_history==[]:
            print("No transactions done")
        else:
            print("---- transaction history ----")
            for history in self.transaction_history:
                print(history)
            print("---- final balance ----")
            print(self.checkbalance())

class Savings_Account(Bank_Account): #savingsaccisabankacc
    def __init__(self,account_number,account_holder,balance,interest_rate):
        super().__init__(account_number,account_holder,balance,"savings")
        self.interest_rate=interest_rate
    def can_withdraw(self,withdraw_amount):
        if self.checkbalance()>=withdraw_amount and withdraw_amount>0:
            return True
        return False
    def calculate_interest(self,years):
        interest=self.interest_rate*self.checkbalance()*years/100
        return interest

class Current_Account(Bank_Account): #currentaccisabankacc
    def __init__(self,account_number,account_holder,balance,overdraft_limit):
        super().__init__(account_number,account_holder,balance,"current")
        self.overdraft_limit=overdraft_limit  
    def can_withdraw(self,withdraw_amount):
            if self.checkbalance()+self.overdraft_limit>=withdraw_amount and withdraw_amount>0:
                return True
            return False

def error_present(value):
    if type(value)==int or type(value)==float:
        if value<0:
            return True
    else:
        if value.strip()=="":
            return True
    return False
        
def looping_error_checking(prompt,datatype):
    while True:
        try:
            inputvalue=datatype(input(f"Enter {prompt}: "))
            if prompt in ["balance", "interest_rate", "overdraft_limit"] and inputvalue < 0:
                raise ValueError("cannot be negative")
            if prompt in ["deposit amount", "withdraw amount"] and inputvalue <= 0:
                raise ValueError("transaction amount must be positive")
            if prompt in ["customer_id","account_number","Number of customers"]:
                if inputvalue==0:
                    raise ValueError("Zero not allowed.")
            if prompt=="phone_number":
                if not inputvalue.isdigit() or len(inputvalue) != 10 or set(inputvalue) == {"0"}:
                    raise ValueError("Phone number must contain exactly 10 digits")
            if prompt == "name" and (not any(char.isalpha() for char in inputvalue)
                    or any(not (char.isalpha() or char.isspace() or char in "-'.’") for char in inputvalue)):
                raise ValueError("Enter a valid name.")
            if error_present(inputvalue):
                raise ValueError
            if prompt == "years" and inputvalue <= 0:
                raise ValueError("can only be positive.")
            return inputvalue
        except ValueError:
            print(f"Invalid input.")
        
def main():
    accounts=load_accounts()
    if accounts is None:
        print("Unable to load bank records. Fix bank_accounts.csv before restarting.")
        return
    if not accounts:
        n=looping_error_checking("Number of customers",int)
        for i in range(n):
            name=looping_error_checking("name",str)
            while True:
                customer_id=looping_error_checking("customer_id",int)
                if not search(accounts,customer_id,"customerid"):
                    break
                #somethingswronghereitnot
                print("Duplicate Ids not allowed.")
            phone_number=looping_error_checking("phone_number",str)
            customer=Customer(name,customer_id,phone_number)

            while True:
                account_number=looping_error_checking("account_number",int)
                if not search(accounts,account_number,"accountid"):
                    break
                print("Duplicate Ids not allowed.")
            
            balance=looping_error_checking("balance",float)
            while True:
                account_type=looping_error_checking("account type (Savings or Current)",str).strip().lower()
                if account_type == "savings":
                    interest_rate = looping_error_checking("interest_rate", float)
                    bank_account = Savings_Account(account_number, customer, balance, interest_rate)
                    break
                elif account_type == "current":
                    overdraft_limit = looping_error_checking("overdraft_limit", float)
                    bank_account = Current_Account(account_number, customer, balance, overdraft_limit)
                    break
                else:
                    print("Invalid account type.")
            accounts.append(bank_account)
        save_accounts(accounts)  

    print("---- menu ----")
    while True:
        print("1. Display all accounts")
        print("2. Search account")
        print("3. Check balance")
        print("4. Deposit money")
        print("5. Withdraw money")
        print("6. Display transaction history")
        print("7. Calculate savings interest")
        print("8. Add account")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display(accounts)

        elif choice == "2":
            account_number = looping_error_checking("account_number", int)
            result = search(accounts, account_number, "accountid")
            if result:
                print(result)
            else:
                print("Account not found.")

        elif choice == "3":
            account_number = looping_error_checking("account_number", int)
            result = search(accounts, account_number, "accountid")
            if result:
                print("Current balance:", result.checkbalance())
            else:
                print("Account not found.")

        elif choice == "4":
            account_number = looping_error_checking("account_number", int)
            result = search(accounts, account_number, "accountid")
            if result:
                amount = looping_error_checking("deposit amount", float)
                if result.deposit(amount):
                    save_accounts(accounts)
            else:
                print("Account not found.")

        elif choice == "5":
            account_number = looping_error_checking("account_number", int)
            result = search(accounts, account_number, "accountid")
            if result:
                amount = looping_error_checking("withdraw amount", float)
                if result.withdraw(amount):
                    save_accounts(accounts)
            else:
                print("Account not found.")
    
        elif choice == "6":
            account_number = looping_error_checking("account_number", int)
            result = search(accounts, account_number, "accountid")
            if result:
                result.display_transaction_history()
            else:
                print("Account not found.")

        elif choice == "7":
            account_number = looping_error_checking("account_number", int)
            result = search(accounts, account_number, "accountid")
            if result:
                if isinstance(result, Savings_Account):
                    years = looping_error_checking("years", float)
                    print("Interest:", result.calculate_interest(years))
                else:
                    print("Interest calculation is only available for savings accounts.")
            else:
                print("Account not found.")

        elif choice == "8":
            accounts.append(add_account(accounts))
            save_accounts(accounts)

        elif choice == "9":
            save_accounts(accounts)
            print("Exiting Bank Management System.")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 9.")


def add_account(accounts):
    name = looping_error_checking("name", str)
    while True:
        customer_id = looping_error_checking("customer_id", int)
        if not search(accounts, customer_id, "customerid"):
            break
        print("Duplicate Ids not allowed.")
    phone_number = looping_error_checking("phone_number", str)
    customer = Customer(name, customer_id, phone_number)
    while True:
        account_number = looping_error_checking("account_number", int)
        if not search(accounts, account_number, "accountid"):
            break
        print("Duplicate Ids not allowed.")
    balance = looping_error_checking("balance", float)
    while True:
        account_type = looping_error_checking("account type (Savings or Current)", str).strip().lower()
        if account_type == "savings":
            return Savings_Account(account_number, customer, balance,
                                   looping_error_checking("interest_rate", float))
        if account_type == "current":
            return Current_Account(account_number, customer, balance,
                                   looping_error_checking("overdraft_limit", float))
        print("Invalid account type. Choose Savings or Current.")


def display(accounts):
    for account in accounts:
        print(account)
def search(accounts,id_to_search,type):
    for account in accounts:
        if type=="accountid":
            if id_to_search==account.get_accountnumber():
                return account
        elif type=="customerid":
            if id_to_search==account.account_holder.get_customerid():
                return account
    return False


   



def save_accounts(accounts):
    fieldnames = ["name", "customer_id", "phone_number", "account_number", "balance",
                  "account_type", "transaction_history", "interest_rate", "overdraft_limit"]
    with open("bank_accounts.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for account in accounts:
            customer=account.account_holder
            history_file = io.StringIO(newline="")
            csv.writer(history_file).writerow(account.transaction_history)
            item={
                "name": customer.name,
                "customer_id": customer.get_customerid(),
                "phone_number": customer.phone_number,
                "account_number": account.get_accountnumber(),
                "balance": account.checkbalance(),
                "account_type": account.account_type,
                "transaction_history": history_file.getvalue().rstrip("\r\n")
            }
            if isinstance(account,Savings_Account):
                item["interest_rate"]=account.interest_rate
            elif isinstance(account,Current_Account):
                item["overdraft_limit"]=account.overdraft_limit
            writer.writerow(item)
    print("Bank records saved successfully.")

def load_accounts():
    fieldnames = {"name", "customer_id", "phone_number", "account_number", "balance",
                  "account_type", "transaction_history", "interest_rate", "overdraft_limit"}
    try:
        with open("bank_accounts.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if (not reader.fieldnames or not fieldnames.issubset(reader.fieldnames)
                    or len(reader.fieldnames) != len(fieldnames)):
                print("Error loading bank records: missing CSV columns.")
                return None

            accounts=[]
            for row_number, item in enumerate(reader, start=2):
                try:
                    if (None in item or any(value is None for value in item.values())
                            or not item["name"].strip() or not item["phone_number"].strip()):
                        raise ValueError("Incomplete account record.")
                    customer=Customer(
                        item["name"],
                        int(item["customer_id"]),
                        item["phone_number"]
                    )
                    if not customer.phone_number.isdigit() or len(customer.phone_number) != 10 or set(customer.phone_number) == {"0"}:
                        raise ValueError("Invalid phone number.")
                    if item["account_type"]=="savings":
                        account=Savings_Account(
                            int(item["account_number"]),
                            customer,
                            float(item["balance"]),
                            float(item["interest_rate"])
                        )
                    elif item["account_type"]=="current":
                        account=Current_Account(
                            int(item["account_number"]),
                            customer,
                            float(item["balance"]),
                            float(item["overdraft_limit"])
                        )
                    else:
                        raise ValueError("Unknown account type.")

                    if customer.get_customerid() <= 0 or account.get_accountnumber() <= 0:
                        raise ValueError("Invalid account values.")
                    if isinstance(account, Savings_Account):
                        if account.checkbalance() < 0 or account.interest_rate < 0:
                            raise ValueError("Invalid savings account values.")
                    elif account.checkbalance() < -account.overdraft_limit or account.overdraft_limit < 0:
                        raise ValueError("Invalid current account values.")
                    history = next(csv.reader([item["transaction_history"]])) if item["transaction_history"] else []
                    if not all(isinstance(entry, str) for entry in history):
                        raise ValueError("Invalid transaction history.")
                    account.transaction_history = history
                    accounts.append(account)
                except (csv.Error, TypeError, ValueError):
                    print(f"Skipping malformed bank record on row {row_number}.")
            return accounts
    except FileNotFoundError:
        return []
    except (OSError, csv.Error, UnicodeDecodeError):
        print("Error loading bank records.")
        return None
if __name__ == "__main__":
    main()
