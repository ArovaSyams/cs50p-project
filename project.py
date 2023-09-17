# PYPOCKET app
from tabulate import tabulate
from pyfiglet import Figlet
from tempfile import NamedTemporaryFile
import csv
import shutil
import csv
import sys
import re
import os

def main():
    # print the PYPOCKET app title
    print(app_name())

    # Authenticate to get the username from database/username.csv base on user input
    username = user_authentication(input("Enter your username: "))

    print(f"\nWelcome {username}")

    balance =  get_balance(username)
    # print user balance total table
    
    dashboard(username, balance)
    
    
    
# PYPOCKET title app title
def app_name():
    figlet = Figlet(font="soft")
    return figlet.renderText("PYPOCKET")
    
# Authenticate the username
def user_authentication(username):
    try:
        # open the database/username.csv file
        with open("database/username.csv") as file:
            # read to implement CSV library
            reader = csv.reader(file)
            # search per row
            for row in reader:
                # if inputed username match with username in CSV file then return the username 
                if row[0] == username: 
                    return row[0]
                # else return for exception 
            raise Exception()
                
    except Exception:
        # print when username not found then ask want to create new one or not
        print("\nUsername not found, do you want to create new one?\n1. No, Try input again \n2. Yes\n3. Maybe later")
        while True:
            try:
                is_make_username = int(input())
                # if user want to input again then call user_authentication()
                if is_make_username == 1:
                    return user_authentication(input("Enter your username: "))
                # if user want to create new username then call create_username() 
                if is_make_username == 2:
                    name = create_username()
                    # return the new username
                    return name
                # else if user dont want to create username then exit with sys.exit() 
                elif is_make_username == 3:
                    sys.exit("Have a nice day")
                # if user choose except 1 or 2 then raise the ValueError() and try input again
                else:
                    raise ValueError()
            except ValueError:
                print("Please select between 1, 2 or 3")

# Create new username
def create_username():
    while True:
        try:
            username = input("Create your username: ")
            if re.search(r"^\w+$", username):
                
                if os.path.exists("database/username.csv"):
                    with open("database/username.csv") as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if username == row[0]:
                                raise Exception()

                with open("database/username.csv", "a") as file:
                    writer = csv.writer(file)
                    writer.writerow([username])
                return username
            else:
                print("username must contain alphabetic or number and non-space")
            
        except Exception:
            print("Username exist")

# dashboard
def dashboard(username, balance):
    print("\n---------------------------------------------------------------\nDASHBOARD\n---------------------------------------------------------------")
    print(tabulate([[f"${balance:.2f}"]], headers=["Your Balance"], tablefmt="rounded_grid"))
    print("\n1. Add balance \n2. Reduce balance \n3. Savings \n4. Exit")
    while True:
        try:
            choice = int(input())
            match choice:
                case 1:
                    while True:
                        try:
                            add_balance_inp = float(input("\nAdd balance: $"))
                            add_balance(username, add_balance_inp)
                        except ValueError:
                            print("Must input a nominal")
                case 2:
                    while True:
                        try:
                            reduce_balance_inp = float(input("\nReduce balance: $"))
                            if balance - reduce_balance_inp < 0.00:
                                print("Lack of balance")
                            else:
                                reduce_balance(username, reduce_balance_inp)
                        except ValueError:
                            print("Must input a nominal")
                            
                case 3:
                    savings(username, balance)
                case 4:
                    sys.exit("Have a nice day")
                case _:
                    raise ValueError()
            break
        except ValueError:
            print("Please select number between 1 to 4")

# show the user balance
def get_balance(username):
    try:
        with open("database/balance.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if username == row["username"]:
                    return float(row['balance'])
            raise ValueError()
        
    except FileNotFoundError:
        with open("database/balance.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "balance"])
            writer.writeheader()
            writer.writerow({"username": username, "balance": float(0.00)})
            return float(0.00)
    
    except ValueError:
        with open("database/balance.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "balance"])
            writer.writerow({"username": username, "balance": float(0.00)})
            return float(0.00)

 
# add balance
def add_balance(username, add_balance):
    tempfile = NamedTemporaryFile("w+t", newline="", delete=False)

    with open("database/balance.csv", "r", newline="") as csv_file, tempfile:
        reader = csv.DictReader(csv_file)
        writer = csv.DictWriter(tempfile, fieldnames=["username", "balance"])
        
        writer.writeheader()
        for row in reader:
            if row["username"] == username:
                added_balance = float(row["balance"]) + add_balance
                row["balance"] = added_balance
            writer.writerow({"username": row["username"], "balance": row["balance"]})
        
    shutil.move(tempfile.name, "database/balance.csv")

    dashboard(username, added_balance)

def reduce_balance(username, reduce_balance):
    tempfile = NamedTemporaryFile("w+t", newline="", delete=False)

    with open("database/balance.csv", "r", newline="") as csv_file, tempfile:
        reader = csv.DictReader(csv_file)
        writer = csv.DictWriter(tempfile, fieldnames=["username", "balance"])
        
        writer.writeheader()
        for row in reader:
            if row["username"] == username:
                reduced_balance = float(row["balance"]) - reduce_balance
                row["balance"] = reduced_balance
            writer.writerow({"username": row["username"], "balance": row["balance"]})
    # copy and archiving new balance.csv file
    shutil.move(tempfile.name, "database/balance.csv")

    dashboard(username, reduced_balance)

# savings dashboard
def savings(username, balance):
    savings = get_savings(username)
    print("\n---------------------------------------------------------------\nSAVINGS\n---------------------------------------------------------------")
    print(tabulate([[f"${savings:.2f}"]], headers=["Your Savings"], tablefmt="rounded_grid"))
    print("\n1. Add savings \n2. Reduce savings \n3. Back to dashboard")
    
    while True:
        try:
            choice = int(input())
            match choice:
                case 1:
                    while True:
                        try:
                            add_savings_inp = float(input("\nAdd savings: $"))
                            add_savings(username, balance, add_savings_inp)
                        except ValueError:
                            print("Must input a nominal")
                case 2:
                    while True:
                        try:
                            reduce_savings_inp = float(input("\nReduce savings: $"))
                            if savings - reduce_savings_inp < 0.00:
                                print("Lack of savings")
                            else:
                                reduce_savings(username, reduce_savings_inp)
                        except ValueError:
                            print("Must input a nominal")
                            
                case 3:
                    dashboard(username, balance)
                case _:
                    raise ValueError()
            break
        except ValueError:
            print("Must select number between 1 to 3")
    


def get_savings(username):
    try:
        with open("database/savings.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if username == row["username"]:
                    return float(row['savings'])
            raise ValueError()
        
    except FileNotFoundError:
        with open("database/savings.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "savings"])
            writer.writeheader()
            writer.writerow({"username": username, "savings": float(0.00)})
            return float(0.00)
    
    except ValueError:
        with open("database/savings.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "savings"])
            writer.writerow({"username": username, "savings": float(0.00)})
            return float(0.00)

def add_savings(username, balance, add_savings):
    # get available balance
    with open("database/balance.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username:
                get_balance = float(row["balance"])

    if get_balance - add_savings < 0:
        print("Error message: Your savings amount input is bigger than your balance")
        savings(username, balance)
    else:
        # make temporary file
        balance_tempfile = NamedTemporaryFile("w+t", newline="", delete=False)

        # reduce balance amount
        with open("database/balance.csv", "r", newline="") as csv_file, balance_tempfile:
            reader = csv.DictReader(csv_file)
            writer = csv.DictWriter(balance_tempfile, fieldnames=["username", "balance"])
            
            writer.writeheader()
            for row in reader:
                if row["username"] == username:
                    reduced_balance = get_balance - add_savings
                    row["balance"] = reduced_balance
                writer.writerow({"username": row["username"], "balance": row["balance"]})

        # copying file and archive for the new one / replace file
        shutil.move(balance_tempfile.name, "database/balance.csv")

        savings_tempfile = NamedTemporaryFile("w+t", newline="", delete=False)
        with open("database/savings.csv", "r", newline="") as csv_file, savings_tempfile:
            reader = csv.DictReader(csv_file)
            writer = csv.DictWriter(savings_tempfile, fieldnames=["username", "savings"])
            
            writer.writeheader()
            for row in reader:
                if row["username"] == username:
                    added_savings = float(row["savings"]) + add_savings
                    row["savings"] = added_savings
                writer.writerow({"username": row["username"], "savings": row["savings"]})

        # copying file and archive for the new one / replace file
        shutil.move(savings_tempfile.name, "database/savings.csv")

        savings(username, reduced_balance)

def reduce_savings(username, reduce_savings):
    # make temporary file
    balance_tempfile = NamedTemporaryFile("w+t", newline="", delete=False)

    # reduce balance amount
    with open("database/balance.csv", "r", newline="") as csv_file, balance_tempfile:
        reader = csv.DictReader(csv_file)
        writer = csv.DictWriter(balance_tempfile, fieldnames=["username", "balance"])
        
        writer.writeheader()
        for row in reader:
            if row["username"] == username:
                added_balance = float(row["balance"]) + reduce_savings
                row["balance"] = added_balance
            writer.writerow({"username": row["username"], "balance": row["balance"]})

    # copying file and archive for the new one / replace file
    shutil.move(balance_tempfile.name, "database/balance.csv")

    savings_tempfile = NamedTemporaryFile("w+t", newline="", delete=False)
    with open("database/savings.csv", "r", newline="") as csv_file, savings_tempfile:
        reader = csv.DictReader(csv_file)
        writer = csv.DictWriter(savings_tempfile, fieldnames=["username", "savings"])
        
        writer.writeheader()
        for row in reader:
            if row["username"] == username:
                reduced_savings = float(row["savings"]) - reduce_savings
                row["savings"] = reduced_savings
            writer.writerow({"username": row["username"], "savings": row["savings"]})

    # copying file and archive for the new one / replace file
    shutil.move(savings_tempfile.name, "database/savings.csv")

    savings(username, added_balance)

if __name__ == "__main__":
    main()