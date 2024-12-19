"""
PR: This project is a simple banking system designed to support basic account management operations, 
such as deposits, withdrawals, and transfers. The system aims to be secure, user-friendly, and efficient, 
while also maintaining data integrity and providing basic error handling.
"""

class BankAccount:
    def __init__(self, account_number: str, balance: float = 0.0):
        self.account_number = account_number
        self.balance = balance
        self.frozen = False

    def deposit(self, amount: float):
        if self.frozen:
            print("Account is frozen. Cannot perform this operation.")
            return
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        print(f"Deposited {amount}. New balance is {self.balance}")

    def withdraw(self, amount: float):
        if self.frozen:
            print("Account is frozen. Cannot perform this operation.")
            return
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("Insufficient funds.")
            return
        self.balance -= amount
        print(f"Withdrew {amount}. New balance is {self.balance}")

    def get_balance(self):
        return self.balance

    def freeze_account(self):
        self.frozen = True
        print(f"Account {self.account_number} has been frozen.")

    def unfreeze_account(self):
        self.frozen = False
        print(f"Account {self.account_number} has been unfrozen.")


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number: str):
        if account_number in self.accounts:
            print("Account already exists.")
            return
        self.accounts[account_number] = BankAccount(account_number)
        print(f"Account {account_number} created.")

    def delete_account(self, account_number: str):
        if account_number not in self.accounts:
            print("Account not found.")
            return
        del self.accounts[account_number]
        print(f"Account {account_number} has been deleted.")

    def transfer(self, from_account: str, to_account: str, amount: float):
        if from_account not in self.accounts or to_account not in self.accounts:
            print("One or both accounts not found.")
            return

        from_acc = self.accounts[from_account]
        to_acc = self.accounts[to_account]

        if from_acc.frozen or to_acc.frozen:
            print("One or both accounts are frozen. Cannot perform transfer.")
            return

        if amount <= 0:
            print("Transfer amount must be positive.")
            return
        if from_acc.balance < amount:
            print("Insufficient funds for transfer.")
            return

        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        print(f"Transferred {amount} from {from_account} to {to_account}.")

    def freeze_account(self, account_number: str):
        if account_number not in self.accounts:
            print("Account not found.")
            return
        self.accounts[account_number].freeze_account()

    def unfreeze_account(self, account_number: str):
        if account_number not in self.accounts:
            print("Account not found.")
            return
        self.accounts[account_number].unfreeze_account()
