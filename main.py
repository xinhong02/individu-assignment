# main.py

from function import verify_user, calculate_tax, save_to_csv, read_from_csv

# In-memory registration dictionary
registered_users = {}  # {user_id: ic_number}

def register_user():
    """Registers a new user with ID and IC number."""
    user_id = input("Register a new User ID: ")
    if user_id in registered_users:
        print("This User ID is already registered.\n")
        return None, None

    ic_number = input("Enter your 12-digit IC number: ")
    if len(ic_number) != 12 or not ic_number.isdigit():
        print("Invalid IC number. Must be exactly 12 digits.\n")
        return None, None

    registered_users[user_id] = ic_number
    password = ic_number[-4:]
    print(f"Registration successful. Your password is: {password}\n")
    return user_id, ic_number

def main():
    filename = "tax_data.csv"
    print("Welcome to the Malaysian Tax Input Program\n")

    while True:
        user_id = input("Enter your User ID: ")
        password = input("Enter your password (last 4 digits of your IC): ")

        if user_id in registered_users:
            ic_number = registered_users[user_id]
            if not verify_user(ic_number, password):
                print("Login failed: Incorrect password.\n")
                continue
            else:
                print("Login successful.\n")
        else:
            print("User ID not registered. Proceeding to registration...\n")
            user_id, ic_number = register_user()
            if not user_id or not ic_number:
                continue  # Registration failed
            # After registration, prompt login again
            password = input("Enter your new password to login: ")
            if not verify_user(ic_number, password):
                print("Login failed after registration. Try again.\n")
                continue
            print("Login successful.\n")

        # Proceed with tax input
        try:
            income = float(input("Enter your annual income (RM): "))
            relief = float(input("Enter your total tax relief amount (RM): "))
        except ValueError:
            print("Invalid input. Please enter numbers only.\n")
            continue

        tax = calculate_tax(income, relief)
        print(f"\nYour tax payable: RM {tax:.2f}")

        user_data = {
            "IC Number": ic_number,
            "Income": income,
            "Tax Relief": relief,
            "Tax Payable": tax
        }

        save_to_csv(user_data, filename)
        print("Your data has been saved.\n")

        view = input("Do you want to view all tax records? (yes/no): ").lower()
        if view == "yes":
            df = read_from_csv(filename)
            if df is not None:
                print("\n--- Tax Records ---")
                print(df.to_string(index=False))
            else:
                print("No records found.\n")

        again = input("\nDo you want to process another user? (yes/no): ").lower()
        if again != "yes":
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()
