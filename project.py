# PYPOCKET app
from tabulate import tabulate
from pyfiglet import Figlet
import csv
import sys
import re
import os

def main():
    # print the PYPOCKET app name
    print(app_name())

    # Authenticate to get the username from username.csv base on user input
    username = user_authentication(input("Enter your username: "))
    print(f"Welcome {username}")
    
# PYPOCKET title app name
def app_name():
    figlet = Figlet(font="soft")
    return figlet.renderText("PYPOCKET")
    
# Authenticate the username
def user_authentication(username):
    try:
        # open the username.csv file
        with open("username.csv") as file:
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
        print("\nUsername not found, do you want to create new one? \n1. Yes\n2. Maybe later")
        while True:
            try:
                is_make_username = int(input())
                # if user want to create new username then call create_username() 
                if is_make_username == 1:
                    name = create_username()
                    # return the new username
                    return name
                # else if user dont want to create username then exit with sys.exit() 
                elif is_make_username == 2:
                    sys.exit("Have a nice day")
                # if user choose except 1 or 2 then raise the ValueError() and try input again
                else:
                    raise ValueError()
            except ValueError:
                print("Please select between 1 or 2")



def create_username():
    while True:
        try:
            username = input("Create your username: ")
            if re.search(r"^\w+$", username):
                
                if os.path.exists("username.csv"):
                    with open("username.csv") as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if username == row[0]:
                                raise Exception()

                with open("username.csv", "a") as file:
                    writer = csv.writer(file)
                    writer.writerow([username])
                return username
            else:
                print("username must contain alphabetic or number and non-space")
            
        except Exception:
            print("Username exist")

        


if __name__ == "__main__":
    main()