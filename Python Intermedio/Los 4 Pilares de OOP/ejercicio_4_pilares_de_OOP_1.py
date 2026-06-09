class BankAccount:

    def __init__(self, balance):
        self.__balance = balance 


    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Depositing: {amount}. New balance: {self.__balance}")
        else:
            print("Deposit amount must be positive.")


    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrawing: {amount}. New balance: {self.__balance}")
        else:
            print("Withdrawal amount is invalid or insufficient funds.")


    def get_balance(self):
        return self.__balance 


class SavingsAccount(BankAccount):

    def __init__(self, balance, min_balance):
        super().__init__(balance)  

        if balance < min_balance:
            raise ValueError(
                "The initial balance cannot be lower than the minimum balance."
            )

        self.min_balance = min_balance


    def withdraw(self, amount):
        new_balance = self.get_balance() - amount

        if new_balance < self.min_balance:
            raise ValueError("The withdrawal would leave the balance below the minimum balance.")

        super().withdraw(amount)