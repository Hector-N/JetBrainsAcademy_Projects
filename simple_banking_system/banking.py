import random
import sqlite3
from sqlite3 import Error
from sqlite3 import IntegrityError


def luhn(card_15):
    """
    Checksum given string of integers.
    """
    mult2 = [int(card_15[i]) * 2 if i % 2 == 0 else int(card_15[i]) for i in range(len(card_15))]
    substract9 = [n if n <= 9 else n - 9 for n in mult2]
    reminder = sum(substract9) % 10
    checksum = '0' if reminder == 0 else str(10 - reminder)

    return f'{card_15}{checksum}'


class Bank:

    def __init__(self):
        self.name = 'SmallBank'

    def __str__(self):
        return f"{self.name} with {storage.acc_number()} customers accounts."

    # @classmethod
    def create_account(cls):

        while True:  # generate new unique account number (card number)
            inn = '400000'
            account_id = ''.join(str(random.randint(0, 9)) for _ in range(9))
            first_15 = inn + account_id
            new_card_num = luhn(first_15)

            if not storage.account_exists(new_card_num):
                new_pin = ''.join(str(random.randint(0, 9)) for _ in range(4))
                storage.add_account(new_card_num, new_pin, 0)
                card, pin, _ = storage.get_account_details(new_card_num)
                print('Your card has been created')
                print(f"Your card number:\n{card}")
                print(f"Your card PIN:\n{pin}\n")

                return True

    # @classmethod
    def log_in(cls):
        card_input = input('Enter your card number:').strip()
        pin_input = input('Enter your PIN:').strip()

        if storage.account_authentication(card_input, pin_input):
            menu = [(1, 'Balance'), (2, 'Add income'), (3, 'Do transfer'),
                    (4, 'Close account'), (5, 'Log out'), (0, 'Exit')]
            menu_str = '\n'.join([f"{n}. {line}" for n, line in menu]) + '\n'
            print('\nYou have successfully logged in!\n')

            while True:
                command = int(input(menu_str))

                if command == 0:
                    print('\nBye!')
                    return False

                elif command == '1':
                    _, _, balance = storage.get_account_details(card_input)
                    print(f"\nBalance: {balance}\n")

                elif command == 2:
                    income = int(input('\nEnter income:\n').strip())
                    storage.deposit(income, card_input)
                    print('Income was added!\n')

                elif command == 3:
                    storage.transfer(card_input)

                elif command == 4:
                    storage.close_account(card_input)
                    print('\nThe account has been closed!\n')

                elif command == 5:
                    print('\nYou have successfully logged out!\n')
                    break

                else:
                    continue
        else:
            print('\nWrong card number or PIN!\n')


# class BankingAccount(Bank):
#
#     def __init__(self):
#         self.card_number, self.pin = Bank.create_account()


class Storage(Bank):

    def __init__(self, path):
        conn = None
        try:
            conn = sqlite3.connect(path)
        except Error as e:
            print(f"Error creating connection: \n{e}")
        cur = None
        try:
            cur = conn.cursor()
        except Error as e:
            print(f"Error creating cursor: \n{e}")

        if conn and cur:
            self.conn = conn
            self.cur = cur

        self.cur.execute("CREATE TABLE IF NOT EXISTS card (\n"
                         "  id INTEGER PRIMARY KEY NOT NULL,\n"
                         "  number TEXT NOT NULL,\n"
                         "  pin TEXT NOT NULL,\n"
                         "  balance INTEGER DEFAULT 0"
                         "  );")
        self.conn.commit()

    def __str__(self):
        return f"This is storage for banking data with {self.acc_number()} records."

    def acc_number(self):
        self.cur.execute("SELECT SUM(*) FROM card;")
        return self.cur.fetchone()[0]

    def add_account(self, new_card_num, new_pin, initial_balance):
        try:
            dml = "INSERT INTO card (number, pin, balance) VALUES (?, ?, ?);"
            self.cur.execute(dml, (new_card_num, new_pin, initial_balance,))
            self.conn.commit()
        except IntegrityError as e:
            print(f"Integrity constraints violation!\n{e}")
        except Error as e:
            print(f"Insertion problem: {e}")

    def get_account_details(self, card_num_input):
        dql = "SELECT id, number, pin, balance FROM card\n" \
              "WHERE number == ?"
        self.cur.execute(dql, (card_num_input,))
        rec = self.cur.fetchone()
        if rec:
            _, card, pin, balance = rec

            return card, pin, balance

        else:
            print('no such record\n')

    def close_account(self, account):
        ddl = "DELETE FROM card WHERE number == ?;"
        try:
            self.cur.execute(ddl, (account,))
            self.conn.commit()
        except Error as e:
            print(f"Error while deleting account {account}: \n{e}")

    def deposit(self, amount, account):
        try:
            dml = "UPDATE card SET balance = (SELECT balance FROM card WHERE number == ?) + ?\n" \
                  "WHERE number == ?;"
            self.cur.execute(dml, (account, amount, account))
            self.conn.commit()
        except Error as e:
            print(f"Error while making deposit: \n{e}")

    def account_exists(self, account):
        dql = "SELECT id FROM card WHERE number == ?;"
        self.cur.execute(dql, (account,))
        acc_id = self.cur.fetchone()
        if acc_id:
            return acc_id
        else:
            return False

    def account_authentication(self, card_input, pin_input):
        dql = "SELECT 1 FROM card WHERE number == ? AND pin == ?;"
        self.cur.execute(dql, (card_input, pin_input,))

        return True if self.cur.fetchone() else False

    def transfer(self, account_from):
        print('\nTransfer')
        account_to = input('Enter card number:\n')

        if account_to != luhn(account_to[:-1]):
            print('Probably you made a mistake in the card number. Please try again!')
            return False
        elif account_to == account_from:
            print("You can't transfer money to the same account!")
            return False
        elif not self.account_exists(account_to):
            print('Such a card does not exist.')
            return False

        amount = int(input('Enter how much money you want to transfer:\n'))
        avail = self.get_account_details(account_from)[2]
        if int(avail) < amount:
            print('Not enough money!')
            return False
        else:
            _, _, available_funds = self.get_account_details(account_from)
            new_available_funds = int(available_funds) - amount

            _, _, available_funds_in_target = self.get_account_details(account_to)
            new_available_funds_in_target = int(available_funds_in_target) + amount

            # todo: make it like transaction
            transaction_1 = "UPDATE card SET balance = ? WHERE number == ?;"
            transaction_2 = "UPDATE card SET balance = ? WHERE number == ?;"
            self.cur.execute(transaction_1, (new_available_funds, account_from,))
            self.cur.execute(transaction_2, (new_available_funds_in_target, account_to,))
            self.conn.commit()
            print('Success!\n')
            return True


lol_bank = Bank()
storage = Storage('card.s3db')

menu = dict([(1, 'Create an account'), (2, 'Log into account'), (0, 'Exit')])
menu_str = '\n'.join([f"{n}. {line}" for n, line in menu.items()]) + '\n'

while True:
    command = int(input(menu_str).strip())

    if command == 0:
        print('\nBye!\n')
        break

    elif command == 1:
        print()
        lol_bank.create_account()

    elif command == 2:
        print()
        res = lol_bank.log_in()
        if res is False:
            break
