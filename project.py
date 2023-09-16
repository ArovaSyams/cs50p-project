# PYPOCKET app
from tabulate import tabulate
from pyfiglet import Figlet
from tempfile import NamedTemporaryFile
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

    balance =  show_balance(username)
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

# show the user balance
def show_balance(username):
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
        
    shutil.move(tempfile.name, "database/balance.csv")

    dashboard(username, reduced_balance)

def dashboard(username, balance):
    print(tabulate([[f"${balance:.2f}"]], headers=["Your Balance"], tablefmt="rounded_grid"))
    print("\n1. Add balance \n2. Reduce balance \n3. Savings \n4. Bills \n5. History \n6. Exit")
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
                            if balance - reduce_balance_inp < 0:
                                print("lack of balance")
                            else:
                                reduce_balance(username, reduce_balance_inp)
                        except ValueError:
                            print("Must input a nominal")
                            
                case 3:
                    savings()
                case 4:
                    bills()
                case 5:
                    history()
                case 6:
                    sys.exit("Have a nice day")
                case _:
                    raise ValueError()
            break
        except ValueError:
            print("Must select number between 1 to 6")


if __name__ == "__main__":
    main()