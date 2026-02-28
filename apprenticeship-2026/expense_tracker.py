# expense_tracker.py
# CLI Expense Tracker - starter version

# Stores transactions in memory for now
transactions = []

def add_income():
    amount = float(input("Enter income amount: "))
    source = input("Enter income source: ")
    transactions.append({"type": "income", "amount": amount, "description": source})
    print("Income recorded!\n")

def add_expense():
    amount = float(input("Enter expense amount: "))
    desc = input("Enter expense description: ")
    transactions.append({"type": "expense", "amount": amount, "description": desc})
    print("Expense recorded!\n")

def view_balance():
    income = sum(t["amount"] for t in transactions if t["type"] == "income")
    expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = income - expense
    print(f"Total Income: {income}")
    print(f"Total Expenses: {expense}")
    print(f"Current Balance: {balance}\n")

def main():
    while True:
        print("Welcome to CLI Expense Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_balance()
        elif choice == "4":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Try again.\n")

if __name__ == "__main__":
    main()
