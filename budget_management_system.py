import turtle
import random

expense_file = "expenses.txt"
budget_file = "budgets.txt"
categories = ["Food", "Housing", "Transportation", "Education", "Entertainment", "Shopping", "Other"]

print("___________WELCOME TO ASLI CEREN YILMAZ`S PERSONAL EXPENSE TRACKER!!!!!!!!___________")

open(expense_file,"w")


def load_expenses():
    expenses = []
    with open(expense_file, "r") as file:
        for line in file:
            data = line.strip().split("\t")
            if len(data) == 4:                      # In these codes, I created the expenses.txt file and divided it into categories.
                expenses.append({
                    "date": data[0],
                    "amount": float(data[1]),
                    "category": data[2],
                    "description": data[3]
                })
    return expenses


def create_budget():
    budget_data = {
        "Food": 500,
        "Housing": 1200,
        "Transportation": 300,
        "Education": 200,                           #This function automatically creates a budgets.txt file and fills it in.
        "Entertainment": 150,
        "Shopping": 400,
        "Other": 200,
    }
    with open("budgets.txt", "w") as file:
        for category, amount in budget_data.items():
            file.write(f"{category}\t{amount}\n")


create_budget()


def load_budget():
    budget = {}
    with open(budget_file, "r") as file:
        for line in file:
            data = line.strip().split("\t")              #This code loads a budget dictionary from a file with categories as keys and amounts as values.
            if len(data) == 2 and data[0] in categories:
                budget[data[0]] = float(data[1])
    return budget


def save_expenses(expenses):
    with open(expense_file, "w") as file:
        for e in expenses:
            file.write(f"{e['date']}\t{e['amount']}\t{e['category']}\t{e['description']}\n")

def valid_date(date):
    parts = date.split("-")

    if len(parts) != 3:
        return False

    day, month, year = parts                          #This code checks whether the entered dates are in the correct format.

    if not (day.isdigit() and month.isdigit() and year.isdigit()):
        return False

    if not (1 <= int(day) <= 31):
        return False

    if not (1 <= int(month) <= 12):
        return False

    if int(year) <= 0:
        return False

    return True

def menu():
    print("\nPERSONAL EXPENSE TRACKER")
    print("1. Add Expenses")
    print("2. View Expenses")
    print("3. Expense Bar Chart")                   #This code configures the application's menu.
    print("4. Search")
    print("5. Budget Alerts")
    print("6. Exit")

def add_expense(expenses):
    date = input("Enter date (DD-MM-YYYY): ")
    if not valid_date(date):
        print("Invalid date format!")
        return

    amount = input("Enter amount: ")
    if not amount.replace('.', '', 1).isdigit():
        print("Invalid amount!")
        return

    print("Categories: ", ", ".join(categories))
    category = input("Enter category: ")
    if category not in categories:
        print("Invalid category!")
        return

    description = input("Enter description: ")
    expenses.append({"date": date, "amount": float(amount), "category": category, "description": description})
    save_expenses(expenses)
    print("Expense added successfully!")


def view_expenses(expenses):
    print("1. View all expenses")
    print("2. View expenses grouped by category")    # This function lists the expenses.


    choice = input("Choose an option (1 or 2): ")

    # Option 1: View all expenses
    if choice == "1":
        print("\nDate    \tAmount\tCategory\tDescription")
        for aslı in expenses:                              # I added some spaces in between to format the table properly
            print(f"{aslı['date']}\t{aslı['amount']}\t{aslı['category']}    \t{aslı['description']}")


    elif choice == "2":
        group = {}

        for expe in expenses:
            if expe['category'] not in group:
                group[expe['category']] = []
            group[expe['category']].append(expe)

        # Display grouped expenses
        for category in group:
            print(f"\nCategory: {category}")
            for e in group[category]:
                print(f"{e['date']}\t{e['amount']}\t{e['description']}")

    else:
        print("Invalid choice! Please enter 1 or 2.")


def draw_bar(t, height, width, label, amount):
    # Senin orijinal fonksiyonunu biraz daha "renkli" ve "bilgili" yaptık
    t.fillcolor(random.choice(["blue", "green", "red", "orange", "purple"]))
    t.begin_fill()
    t.left(90)
    t.forward(height)
    t.right(90)
    t.forward(width)
    t.right(90)
    t.forward(height)
    t.left(90)
    t.end_fill()

    # Üzerine miktar yazma eklendi
    t.penup()
    t.left(90)
    t.forward(height + 5)
    t.write(f"{int(amount)} TL", align="center")
    t.backward(height + 5)
    t.right(90)

    # Altına kategori yazma
    t.forward(width / 2)
    t.right(90)
    t.forward(20)
    t.write(label, align="center")
    t.backward(20)
    t.left(90)
    t.backward(width / 2)
    t.pendown()


def produce_bar_chart(expenses):
    totals = {}
    for expense in expenses:
        totals[expense['category']] = totals.get(expense['category'], 0) + expense['amount']

    screen = turtle.Screen()
    screen.title("Expense Bar Chart")
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-200, -150)  # Biraz daha aşağı çektik ki yazılar sığsın
    t.pendown()

    bar_width = 50
    spacing = 30
    scale = 0.5

    for category, total in totals.items():
        draw_bar(t, total * scale, bar_width, category, total)  # Fonksiyona total'i de gönderiyoruz
        t.penup()
        t.forward(bar_width + spacing)
        t.pendown()

    t.hideturtle()
    screen.mainloop()

def search_expenses(expenses):
    keyword = input("Enter a keyword or category to search: ").lower()
    results = []
    for expense in expenses:
        if keyword in expense['description'].lower() or keyword == expense['category'].lower():
            results.append(f"{expense['date']}\t{expense['amount']}\t{expense['category']}\t{expense['description']}")

    if results:
        print("\nMatching Expenses:")
        for result in results:
            print(result)
    else:
        print("No matching records found!")


def budget_alerts(expenses, budget):
    category_toplam = {}        #This function gives a warning if the entered expenses exceed the budget values.

    for expense in expenses:
        category = expense['category']
        amount = expense['amount']

        if category in category_toplam:
            category_toplam[category] += amount
        else:
            category_toplam[category] = amount


    for category, total in category_toplam.items():
        if category in budget:
            if total > budget[category]:
                print(f"Warning: {category} expenses exceeded the budget! ({total} > {budget[category]})")
            else:
                print(f"{category} expenses are within the budget.")
        else:
            print(f"No budget set for the {category} category.")


def main():
    expenses = load_expenses()
    budget = load_budget()

    while True:
        menu()
        choice = input("Choose an option: ")    #This code determines which function should run based on the number you entered.

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            produce_bar_chart(expenses)
        elif choice == "4":
            search_expenses(expenses)
        elif choice == "5":
            budget_alerts(expenses, budget)
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option, please try again!")
main()
