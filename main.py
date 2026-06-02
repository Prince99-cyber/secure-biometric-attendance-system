import os

ADMIN_PASSWORD = "1234"

while True:

    print("\nBiometric Authentication System")
    print("1. Admin Setup")
    print("2. Face Login")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        password = input("Enter admin password: ")

        if password == ADMIN_PASSWORD:
            

            print("\nAdmin Menu")
            print("1. Register Face")
            print("2. Train Model")

            admin_choice = input("Enter option: ")

            if admin_choice == "1":
                os.system("python start.py")

            elif admin_choice == "2":
                os.system("python start.py")

        else:
            print("Wrong password")

    elif choice == "2":

        os.system("python recognize.py")

    elif choice == "3":
        print("Exiting system...")
        break

    else:
        print("Invalid choice")