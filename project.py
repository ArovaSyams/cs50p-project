# PYPOCKET app
from tabulate import tabulate
from pyfiglet import Figlet
from tempfile import NamedTemporaryFile
from datetime import date
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

    # get the balance amount
    balance =  get_balance(username)
    
    # call the dashboard page
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
            raise ValueError()
                
    except ValueError:
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

            # validate username with regular expresion, cannot add a spacing
            if re.search(r"^\w+$", username):
                
                # if username.csv exist
                if os.path.exists("database/username.csv"):
                    with open("database/username.csv") as file:
                        reader = csv.reader(file)
                        for row in reader:
                            # check if username exist then raise exception
                            if username == row[0]:
                                raise Exception()

                # if username.csv doesn't exist, the system automaticaly decide that username available to use
                with open("database/username.csv", "a") as file:
                    writer = csv.writer(file)
                    writer.writerow([username])
                return username
            
            # if not based on regex than try input again
            else:
                print("username must contain alphabetic or number and non-space")
            
        # exception raised then try input again
        except Exception:
            print("Username exist")

# dashboard
def dashboard(username, balance):
    print("\n---------------------------------------------------------------\nDASHBOARD\n---------------------------------------------------------------")

    # show the balance table with tabulate
    print(tabulate([[f"${balance:.2f}"]], headers=["Your Balance"], tablefmt="rounded_grid"))
    # print the call to action selection
    print("\n1. Add balance \n2. Reduce balance \n3. Savings \n4. Histories \n5. Exit")
    while True:
        try:
            # input the user selection
            choice = int(input())

            # read the user input if select between available selection
            match choice:
                case 1:
                    # if choose 1 then try to input user balance
                    while True:
                        try:
                            add_balance_inp = float(input("\nAdd balance: $"))
                            # call add_balance() func.
                            add_balance(username, add_balance_inp)
                        # if not a float data type
                        except ValueError:
                            print("Must input a nominal")
                case 2:
                    # if choose 2 then try to input how many user want to reduce the amount
                    while True:
                        try:
                            reduce_balance_inp = float(input("\nReduce balance: $"))

                            # if reduce balance input nominal is bigger than available balance
                            if balance - reduce_balance_inp < 0.00:
                                print("Lack of balance")
                            else:
                                # call reduce_balance() func.
                                reduce_balance(username, reduce_balance_inp)
                        except ValueError:
                            print("Must input a nominal")
                            
                case 3:
                    # if choose 3 then direct to savings page
                    savings(username, balance)
                case 4:
                    histories(username, balance)
                case 5:
                    # 5 for exit
                    sys.exit("Have a nice day")
                case _:
                    raise ValueError()
            break
        except ValueError:
            print("Please select number between 1 to 4")

# get the user balance amount
def get_balance(username):
    try:
        # open and read balance.csv then if username is same as username column in balance.csv file then return balance nominal
        with open("database/balance.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if username == row["username"]:
                    return float(row['balance'])
            # if not username found, than raise exception()
            raise ValueError()
        
    # if file not found
    except FileNotFoundError:
        # write the username balance data and add writerheader() then return 0.00 balance automatically
        with open("database/balance.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "balance"])
            writer.writeheader()
            writer.writerow({"username": username, "balance": float(0.00)})
            return float(0.00)
        
    # write the username balance data then return 0.00 balance automatically
    except ValueError:
        with open("database/balance.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "balance"])
            writer.writerow({"username": username, "balance": float(0.00)})
            return float(0.00)

# add balance
def add_balance(username, add_balance):
    # define the temporary name file in variable
    tempfile = NamedTemporaryFile("w+t", newline="", delete=False)

    # open file, read, and replace updated added balance
    with open("database/balance.csv", "r", newline="") as csv_file, tempfile:
        reader = csv.DictReader(csv_file)
        writer = csv.DictWriter(tempfile, fieldnames=["username", "balance"])
        
        writer.writeheader()
        for row in reader:
            # if authed username is same as username col
            if row["username"] == username:
                # add balance
                added_balance = float(row["balance"]) + add_balance
                row["balance"] = added_balance
            # then rewrite the data
            writer.writerow({"username": row["username"], "balance": row["balance"]})

    # copying file and archive the new one / replace balance.csv
    shutil.move(tempfile.name, "database/balance.csv")

    # add to history for adding balance
    with open("database/histories.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "type", "nominal", "date"])

        writer.writerow({
            "username": username,
            "type": "Balance",
            "nominal": f"+ ${add_balance}",
            "date": date.today()
        })

    return dashboard(username, added_balance)

# reduce balance
def reduce_balance(username, reduce_balance):
    # define the temporary file in variable
    tempfile = NamedTemporaryFile("w+t", newline="", delete=False)

    # open file, read, and replace updated reduced balance
    with open("database/balance.csv", "r", newline="") as csv_file, tempfile:
        reader = csv.DictReader(csv_file)
        writer = csv.DictWriter(tempfile, fieldnames=["username", "balance"])
        
        writer.writeheader()
        for row in reader:
            # if username match then reduce the balance
            if row["username"] == username:
                reduced_balance = float(row["balance"]) - reduce_balance
                row["balance"] = reduced_balance
            # rewrite balance.csv file
            writer.writerow({"username": row["username"], "balance": row["balance"]})

    # copying file and archive the new one / replace balance.csv
    shutil.move(tempfile.name, "database/balance.csv")

    # add history for reduce the balance
    with open("database/histories.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "type", "nominal", "date"])

        writer.writerow({
            "username": username,
            "type": "Balance",
            "nominal": f"- ${reduce_balance}",
            "date": date.today()
        })

    return dashboard(username, reduced_balance)

# savings dashboard
def savings(username, balance):
    # call savings and get savings amount
    savings = get_savings(username)
    print("\n---------------------------------------------------------------\nSAVINGS\n---------------------------------------------------------------")
    # print the savings table
    print(tabulate([[f"${savings:.2f}"]], headers=["Your Savings"], tablefmt="rounded_grid"))
    # selection
    print("\n1. Add savings \n2. Reduce savings \n3. Back to dashboard")
    
    while True:
        try:
            # read the user input
            choice = int(input())
            match choice:
                # if user type 1
                case 1:
                    while True:
                        try:
                            add_savings_inp = float(input("\nAdd savings: $"))
                            # call add_savings
                            add_savings(username, balance, add_savings_inp)
                        # if input except float data type
                        except ValueError:
                            print("Must input a nominal")
                case 2:
                    while True:
                        try:
                            reduce_savings_inp = float(input("\nReduce savings: $"))
                            # if reduce savings amount is bigger available savings amount
                            if savings - reduce_savings_inp < 0.00:
                                print("Lack of savings")
                            else:
                                # call reduce_savings()
                                reduce_savings(username, reduce_savings_inp)
                        # if input except float data type   
                        except ValueError:
                            print("Must input a nominal")
                # type 3 to back to dashboard
                case 3:
                    dashboard(username, balance)
                case _:
                    raise ValueError()
            break
        except ValueError:
            print("Must select number between 1 to 3")
    
# show the user savings amount
def get_savings(username):
    # try if savings.csv file is there
    try:
        # open and read savings.csv
        with open("database/savings.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # if username match then return savings amount
                if username == row["username"]:
                    return float(row['savings'])
            # if username not found then raise value error
            raise ValueError()
    # if file not found then write new savings.csv with header and return 0.00 savings amount automatically
    except FileNotFoundError:
        with open("database/savings.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "savings"])
            writer.writeheader()
            writer.writerow({"username": username, "savings": float(0.00)})
            return float(0.00)
    # if username not found then write new username savings data and return 0.00 savings amount automatically
    except ValueError:
        with open("database/savings.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "savings"])
            writer.writerow({"username": username, "savings": float(0.00)})
            return float(0.00)

# add a savings and reduce the balance
def add_savings(username, balance, add_savings):
    # get available balance
    with open("database/balance.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # if username match then get balance amount and place in variable
            if row["username"] == username:
                get_balance = float(row["balance"])

    # if add savings amount bigger than avalable balance
    if get_balance - add_savings < 0:
        print("Error message: Your savings amount input is bigger than your balance")
        savings(username, balance)
    # if not
    else:
        # define the temporary balance name file in variable
        balance_tempfile = NamedTemporaryFile("w+t", newline="", delete=False)

        # reduce balance amount
        with open("database/balance.csv", "r", newline="") as csv_file, balance_tempfile:
            reader = csv.DictReader(csv_file)
            writer = csv.DictWriter(balance_tempfile, fieldnames=["username", "balance"])
            
            writer.writeheader()
            for row in reader:
                # if username match than reduce balance with added savings
                if row["username"] == username:
                    reduced_balance = get_balance - add_savings
                    row["balance"] = reduced_balance
                # rewrite balance.csv data
                writer.writerow({"username": row["username"], "balance": row["balance"]})

        # copying file and archive for the new one / replace balance.csv file
        shutil.move(balance_tempfile.name, "database/balance.csv")

        # define the temporary savings name file in variable
        savings_tempfile = NamedTemporaryFile("w+t", newline="", delete=False)

        # open and add savings 
        with open("database/savings.csv", "r", newline="") as csv_file, savings_tempfile:
            reader = csv.DictReader(csv_file)
            writer = csv.DictWriter(savings_tempfile, fieldnames=["username", "savings"])
            
            writer.writeheader()
            for row in reader:
                # is username match than add existing savings with new added savings
                if row["username"] == username:
                    added_savings = float(row["savings"]) + add_savings
                    row["savings"] = added_savings
                # rewrite savings data
                writer.writerow({"username": row["username"], "savings": row["savings"]})

        # copying file and archive for the new one / replace savings.csv file
        shutil.move(savings_tempfile.name, "database/savings.csv")

        # add history for add the savings
        with open("database/histories.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "type", "nominal", "date"])

            writer.writerow({
                "username": username,
                "type": "Savings",
                "nominal": f"+ ${add_savings}",
                "date": date.today()
            })

        # then return to savings 
        return savings(username, reduced_balance)

# reduce savings and add the balance
def reduce_savings(username, reduce_savings):
    # define the temporary balance name file in variable
    balance_tempfile = NamedTemporaryFile("w+t", newline="", delete=False)

    # add or return balance amount from reduced savings then open and replace file
    with open("database/balance.csv", "r", newline="") as csv_file, balance_tempfile:
        reader = csv.DictReader(csv_file)
        writer = csv.DictWriter(balance_tempfile, fieldnames=["username", "balance"])
        
        writer.writeheader()
        for row in reader:
            # if username match than add the existing balance with reduced savings amount
            if row["username"] == username:
                added_balance = float(row["balance"]) + reduce_savings
                row["balance"] = added_balance
            # rewrite balance data
            writer.writerow({"username": row["username"], "balance": row["balance"]})

    # copying file and archive for the new one / replace balance.csv file
    shutil.move(balance_tempfile.name, "database/balance.csv")

    # define the temporary savings name file in variable
    savings_tempfile = NamedTemporaryFile("w+t", newline="", delete=False)

    # reduce the existing savings amount with reduce savings nominal then open and replace savings.csv data
    with open("database/savings.csv", "r", newline="") as csv_file, savings_tempfile:
        reader = csv.DictReader(csv_file)
        writer = csv.DictWriter(savings_tempfile, fieldnames=["username", "savings"])
        
        writer.writeheader()
        for row in reader:
            # is username match then reduce existing savings amount with inputed reduce savings amount
            if row["username"] == username:
                reduced_savings = float(row["savings"]) - reduce_savings
                row["savings"] = reduced_savings
            # rewrite savings.csv data
            writer.writerow({"username": row["username"], "savings": row["savings"]})

    # copying file and archive for the new one / replace savings.csv file
    shutil.move(savings_tempfile.name, "database/savings.csv")

    # add history for reduce the savings
    with open("database/histories.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "type", "nominal", "date"])

        writer.writerow({
            "username": username,
            "type": "Savings",
            "nominal": f"- ${reduce_savings}",
            "date": date.today()
        })

    # return savings
    return savings(username, added_balance)

# show histories page
def histories(username, balance):
    histories = get_histories(username)

    print("\n---------------------------------------------------------------\nHISTORIES\n---------------------------------------------------------------")

    # show the balance table with tabulate
    print(tabulate(histories, headers=["Type", "Nominal", "Date"], tablefmt="rounded_grid"))

    while True:
        try:
            input_user = int(input("\n1. Back to dashboard\n"))

            if input_user == 1:
                dashboard(username, balance)
            else:
                raise ValueError()
        except ValueError:
            print("Just have 1 choice")

# get user's histories
def get_histories(username):
    histories = []

    with open("database/histories.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if username == row["username"]:
                histories.append([row["type"], row["nominal"], row["date"]])
    
    return histories

if __name__ == "__main__":
    main()