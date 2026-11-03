from datetime import date, timedelta

Appointments = []
Customers = []

Time_Slots = [
    "9:00 AM", "10:00 AM", "11:00 AM",
    "1:00 PM", "2:00 PM", "3:00 PM",
    "4:00 PM", "5:00 PM", "6:00 PM"
]


# PRINT TABLE

def Print_Table(Headers, Rows):

    if not Rows:
        print("No records to display.")
        return

    Widths = [
        max(len(str(Header)), *(len(str(Row[i])) for Row in Rows))
        for i, Header in enumerate(Headers)
    ]

    Border = "+-" + "-+-".join("-" * Width for Width in Widths) + "-+"

    print(Border)
    print("| " + " | ".join(
        str(Header).ljust(Widths[i])
        for i, Header in enumerate(Headers)
    ) + " |")
    print(Border)

    for Row in Rows:
        print("| " + " | ".join(
            str(Value).ljust(Widths[i])
            for i, Value in enumerate(Row)
        ) + " |")

    print(Border)


# VALIDATE CUSTOMER NAME

def Validate_Name(Name):

    Name = Name.strip()

    if not Name:
        return False

    Allowed_Characters = " ,.-"

    for Character in Name:
        if not Character.isalpha() and Character not in Allowed_Characters:
            return False

    Clean_Name = (
        Name.replace(",", " ")
            .replace(".", " ")
            .replace("-", " ")
    )

    Name_Parts = Clean_Name.split()

    if len(Name_Parts) < 2:
        return False

    return True


# VALIDATE PHILIPPINE CELLPHONE NUMBER

def Validate_Phone_Number(Phone):

    Phone = Phone.strip().replace(" ", "").replace("-", "")

    # International format: +639171234567
    if Phone.startswith("+63"):

        Number = Phone[3:]

        if (
            len(Number) == 10
            and Number.isdigit()
            and Number.startswith("9")
        ):
            return "+63" + Number

    # Local format: 09171234567
    elif Phone.startswith("09"):

        if len(Phone) == 11 and Phone.isdigit():
            return "+63" + Phone[1:]

    # Format without country code: 9171234567
    elif Phone.startswith("9"):

        if len(Phone) == 10 and Phone.isdigit():
            return "+63" + Phone

    return None


# DISPLAY TIME SLOTS AND AVAILABILITY

def Display_Time_Slots(
    Selected_Date,
    Customer_Cellphone=None,
    Selected_Appointment=None
):

    Available_Slots = []
    Slot_Rows = []

    for Time in Time_Slots:

        Status = "Available"

        for Existing in Appointments:

            if (
                Existing["Date"] == Selected_Date
                and Existing["Time"] == Time
            ):

                if (
                    Existing is Selected_Appointment
                    or (
                        Customer_Cellphone is not None
                        and Existing["Cellphone"] == Customer_Cellphone
                    )
                ):
                    Status = "Your Appointment"
                else:
                    Status = "Taken"

                break

        if Status == "Available":
            Available_Slots.append(Time)
            Slot_Number = len(Available_Slots)
        else:
            Slot_Number = "-"

        Slot_Rows.append([Slot_Number, Time, Status])

    print("\n===== TIME SLOT AVAILABILITY =====")

    Print_Table(
        ["No.", "Time Slot", "Availability"],
        Slot_Rows
    )

    return Available_Slots


# APPOINTMENT RECORDS

def Appointment_Records():

    print("\n===== APPOINTMENT RECORDS =====")

    if not Appointments:
        print("No appointment records found.")
        return

    Rows = []

    for i, Appointment in enumerate(Appointments, 1):

        Rows.append([
            i,
            Appointment["Name"],
            Appointment["Cellphone"],
            Appointment["Date"].strftime("%B %d, %Y"),
            Appointment["Day"],
            Appointment["Time"],
            Appointment["Status"]
        ])

    print("Total Appointment Records:", len(Appointments))

    Print_Table(
        [
            "No.",
            "Customer Name",
            "Cellphone",
            "Date",
            "Day",
            "Time",
            "Status"
        ],
        Rows
    )

# MAIN INTERFACE

def Main_Interface():

    while True:
        print("\n====================================================")
        print("|           MARKYS BARBER SHOP APPOINTMENT         |")
        print("====================================================")
        print("|                  MAIN INTERFACE                  |")
        print("----------------------------------------------------")
        print("|                [1] Admin Login                   |")
        print("|                [2] Customer Register             |")         
        print("|                [3] Customer Login                |") 
        print("|                [4] Exit                          |")
        print("----------------------------------------------------")

        Choice = input("Enter The Number Of Your Choice [1] [2] [3] [4]: ")

        if Choice == "1":
            Admin_Login()

        elif Choice == "2":
            Customer_Register()

        elif Choice == "3":
            Customer_Login()

        elif Choice == "4":
            print("\nThank you for using Markys Barber Shop!")
            break

        else:
            print("\nInvalid Choice. Please choose 1-4.")


# ADMIN LOGIN

def Admin_Login():

    print("\n===== ADMIN LOGIN =====")

    Name = input("Enter Name: ").strip()

    if not Name or not Name.replace(" ", ""):
        print("\nInvalid name. Use letters only.")
        return

    Password = input("Enter Password: ")

    if not Password:
        print("\nInvalid password. Use numbers only.")
        return

    if Name == "Admin" and Password == "1234":
        print("\nLogin Successful!")
        print("Welcome, Admin")
        Admin_Menu()

    else:
        print("\nInvalid Name or Password.")

# ADMIN MENU

def Admin_Menu():

    while True:
        print("\n==============================================")
        print("|       ADMIN / OWNER-BARBER                 |")
        print("==============================================")
        print("|        [1] View Appointments               |")
        print("|        [2] Approve Appointment             |")
        print("|        [3] View Registered Accounts        |")
        print("|        [4] Create Appointment              |")
        print("|        [5] Cancel/Update Appointment       |")
        print("|        [6] Appointment Records             |")
        print("|        [7] Log Out                         |")
        print("==============================================")

        try:
            Choice = int(input("Enter Your Choice: "))

        except ValueError:
            print("\nInvalid input. Please enter a number.")
            continue

        if Choice == 1:
            View_Appointments()

        elif Choice == 2:
            Approve_Appointment()

        elif Choice == 3:
            View_Registered_Accounts()

        elif Choice == 4:

            if not Customers:
                print("\nNo registered customer accounts found.")
                continue

            View_Registered_Accounts()

            try:
                Customer_Choice = int(
                    input("\nChoose a customer number: ")
                )

            except ValueError:
                print("\nInvalid input. Please enter a number.")
                continue

            if 1 <= Customer_Choice <= len(Customers):
                Create_Appointment(
                    Customers[Customer_Choice - 1],
                    Admin_Created=True
                )

            else:
                print("\nInvalid customer number.")

        elif Choice == 5:
            Appointment_Actions()

        elif Choice == 6:
            Appointment_Records()

        elif Choice == 7:
            print("\nLogging Out...")
            break

        else:
            print("\nInvalid Choice. Please choose 1-7.")


# CUSTOMER REGISTER

def Customer_Register():

    print("\n===== CUSTOMER REGISTER =====")

    Name = input("Enter your full name: ").strip()

    if not Validate_Name(Name):
        print("\nInvalid name format.")
        print("Enter at least your first name and surname.")
        return

    Cellphone_Input = input("Enter your Cellphone Number: ")

    Cellphone = Validate_Phone_Number(Cellphone_Input)

    if Cellphone is None:
        print("\nInvalid CP number.")
        return

    Password = input("Enter your password: ")

    if not Password:
        print("\nPassword cannot be empty.")
        return

    for Customer in Customers:

        if Customer["Cellphone"] == Cellphone:
            print("\nCellphone number is already registered.")
            return

    Customers.append({
        "Name": Name,
        "Cellphone": Cellphone,
        "Password": Password
    })

    print("\nRegistration Successful!")

    Print_Table(
        ["Customer Name", "Cellphone Number"],
        [[Name, Cellphone]]
    )

    print("\nYou can now login using your cellphone number and password.")


# VIEW REGISTERED ACCOUNTS

def View_Registered_Accounts():

    print    ("\n===== REGISTERED CUSTOMER ACCOUNTS =====")

    if not Customers:
        print (" No registered customer accounts found. ")
        return

    Rows = [
        [i, Customer["Name"], Customer["Cellphone"]]
        for i, Customer in enumerate(Customers, 1)
    ]

    print("Total Registered Accounts:", len(Customers))

    Print_Table(
        ["No.", "Customer Name", "Cellphone Number"],
        Rows
    )


# CUSTOMER LOGIN

def Customer_Login():

    print("\n===== CUSTOMER LOGIN =====")

    Cellphone_Input = input("Enter your Cellphone Number: ")

    Cellphone = Validate_Phone_Number(Cellphone_Input)

    if Cellphone is None:
        print("\nInvalid CP number.")
        return

    Password = input("Enter your password: ")

    if not Password:
        print("\nPassword cannot be empty.")
        return

    for Customer in Customers:

        if (
            Customer["Cellphone"] == Cellphone
            and Customer["Password"] == Password
        ):
            print("\nLogin Successful!")
            print("Welcome,", Customer["Name"])
            Customer_Menu(Customer)
            return

    print("\nInvalid cellphone number or password.")


# CUSTOMER MENU

def Customer_Menu(Customer):

    while True:
        print("\n==================================================")
        print("|                CUSTOMER MENU                   |")
        print("==================================================")
        print("|          [1] Create Appointment                |")
        print("|          [2] Check My Appointment              |")
        print("|          [3] Cancel/Update Appointment         |")
        print("|          [4] Log Out                           |")
        print("==================================================")

        Choice = input("Enter Your Choice: ")

        if Choice == "1":
            Create_Appointment(Customer)

        elif Choice == "2":
            Check_My_Appointment(Customer)

        elif Choice == "3":
            Appointment_Actions(Customer["Cellphone"])

        elif Choice == "4":
            print("\nLogging Out...")
            break

        else:
            print("\nInvalid Choice. Please choose 1-4.")


# CREATE APPOINTMENT

def Create_Appointment(Customer, Admin_Created=False):

    print("\n===== CREATE APPOINTMENT =====")

    Name = Customer["Name"]
    Cellphone = Customer["Cellphone"]

    print("Customer Name:", Name)
    print("Cellphone Number:", Cellphone)

    Today = date.today()
    print("\nToday's Date:", Today.strftime("%B %d, %Y"))

    Available_Days = []
    Current_Date = Today

    while len(Available_Days) < 6:

        if Current_Date.weekday() != 6:
            Available_Days.append(Current_Date)

        Current_Date += timedelta(days=1)

    Day_Rows = [
        [
            i,
            Appointment_Date.strftime("%A"),
            Appointment_Date.strftime("%B %d, %Y")
        ]
        for i, Appointment_Date in enumerate(Available_Days, 1)
    ]

    print("\n===== AVAILABLE DAYS =====")

    Print_Table(
        ["No.", "Day", "Date"],
        Day_Rows
    )

    try:
        Day_Choice = int(input("\nChoose a day: "))

    except ValueError:
        print("\nInvalid input. Please enter a number.")
        return

    if not 1 <= Day_Choice <= len(Available_Days):
        print("\nInvalid day.")
        return

    Appointment_Date = Available_Days[Day_Choice - 1]
    Day = Appointment_Date.strftime("%A")

    # PREVENT MULTIPLE APPOINTMENTS FOR THE SAME CUSTOMER ON THE SAME DATE

    for Existing in Appointments:

        if (
            Existing["Cellphone"] == Cellphone
            and Existing["Date"] == Appointment_Date
        ):
            print("\nYou already have an appointment on this date.")
            print("Please cancel or update your existing appointment.")
            return

    Available_Slots = Display_Time_Slots(Appointment_Date)

    if not Available_Slots:
        print("\nNo available time slots for this day.")
        return

    try:
        Time_Choice = int(
            input("\nChoose an available time slot number: ")
        )

    except ValueError:
        print("\nInvalid input. Please enter a number.")
        return

    if not 1 <= Time_Choice <= len(Available_Slots):
        print("\nInvalid time slot.")
        return

    Time = Available_Slots[Time_Choice - 1]

    # CHECK AVAILABILITY AGAIN BEFORE SAVING

    for Existing in Appointments:

        if (
            Existing["Date"] == Appointment_Date
            and Existing["Time"] == Time
        ):
            print("\nSorry, this time slot has already been taken.")
            return

    Status = "Approved" if Admin_Created else "Pending"

    Appointment = {
        "Name": Name,
        "Cellphone": Cellphone,
        "Date": Appointment_Date,
        "Day": Day,
        "Time": Time,
        "Status": Status
    }

    Appointments.append(Appointment)

    print("\n===== APPOINTMENT CREATED =====")

    Print_Table(
        ["Customer", "Cellphone", "Date", "Day", "Time", "Status"],
        [[
            Name,
            Cellphone,
            Appointment_Date.strftime("%B %d, %Y"),
            Day,
            Time,
            Status
        ]]
    )

    if Admin_Created:
        print("\nAppointment automatically approved by Admin.")

    else:
        print("\nAppointment is waiting for Admin approval.")


# GET APPOINTMENTS

def Get_Appointment_List(Cellphone=None):

    if Cellphone is None:
        return Appointments.copy()

    return [
        Appointment for Appointment in Appointments
        if Appointment["Cellphone"] == Cellphone
    ]


# DISPLAY APPOINTMENTS

def Display_Appointment_List(Selected_Appointments):

    Rows = []

    for i, Appointment in enumerate(Selected_Appointments, 1):

        Rows.append([
            i,
            Appointment["Name"],
            Appointment["Cellphone"],
            Appointment["Date"].strftime("%B %d, %Y"),
            Appointment["Day"],
            Appointment["Time"],
            Appointment["Status"]
        ])

    Print_Table(
        ["No.", "Customer", "Cellphone", "Date", "Day", "Time", "Status"],
        Rows
    )


# CHECK MY APPOINTMENT

def Check_My_Appointment(Customer):

    print("\n===== MY APPOINTMENTS =====")

    Selected = Get_Appointment_List(Customer["Cellphone"])

    if not Selected:
        print("You don't have an appointment.")
        return

    Rows = [
        [
            i,
            A["Date"].strftime("%B %d, %Y"),
            A["Day"],
            A["Time"],
            A["Status"]
        ]
        for i, A in enumerate(Selected, 1)
    ]

    Print_Table(
        ["No.", "Date", "Day", "Time", "Status"],
        Rows
    )


# CANCEL / UPDATE APPOINTMENT MENU

def Appointment_Actions(Cellphone=None):

    while True:
        print("\n===== CANCEL / UPDATE APPOINTMENT ======")
        print("|         [1] Cancel Appointment         |")
        print("|         [2] Update Appointment         |")
        print("|         [3] Back                       |")
        print("==========================================")
        Choice = input("Enter Your Choice [1] [2] [3]: ")

        if Choice == "1":
            Cancel_Appointment(Cellphone)

        elif Choice == "2":
            Update_Appointment(Cellphone)

        elif Choice == "3":
            break

        else:
            print("\nInvalid choice. Please choose 1-3.")


# CANCEL APPOINTMENT

def Cancel_Appointment(Cellphone=None):

    print("\n===== CANCEL APPOINTMENT =====")

    Selected = Get_Appointment_List(Cellphone)

    if not Selected:
        print("No appointments found.")
        return

    Display_Appointment_List(Selected)

    try:
        Choice = int(input("\nEnter appointment number to cancel: "))

    except ValueError:
        print("\nInvalid input. Please enter a number.")
        return

    if not 1 <= Choice <= len(Selected):
        print("\nInvalid appointment number.")
        return

    Appointment = Selected[Choice - 1]

    Confirm = input(
        "\nCancel this appointment? (Y/N): "
    ).strip().upper()

    if Confirm == "Y":
        Appointments.remove(Appointment)
        print("\nAppointment Cancelled Successfully!")

    elif Confirm == "N":
        print("\nCancellation cancelled.")

    else:
        print("\nInvalid choice. Please enter Y or N.")


# UPDATE APPOINTMENT

def Update_Appointment(Cellphone=None):

    print("\n===== UPDATE APPOINTMENT =====")

    Selected = Get_Appointment_List(Cellphone)

    if not Selected:
        print("No appointments found.")
        return

    Display_Appointment_List(Selected)

    try:
        Choice = int(input("\nEnter appointment number to update: "))

    except ValueError:
        print("\nInvalid input. Please enter a number.")
        return

    if not 1 <= Choice <= len(Selected):
        print("\nInvalid appointment number.")
        return

    Appointment = Selected[Choice - 1]

    Available_Days = []
    Current_Date = date.today()

    while len(Available_Days) < 6:

        if Current_Date.weekday() != 6:
            Available_Days.append(Current_Date)

        Current_Date += timedelta(days=1)

    Day_Rows = [
        [
            i,
            D.strftime("%A"),
            D.strftime("%B %d, %Y")
        ]
        for i, D in enumerate(Available_Days, 1)
    ]

    print("\n===== AVAILABLE DAYS =====")

    Print_Table(
        ["No.", "Day", "Date"],
        Day_Rows
    )

    try:
        Day_Choice = int(input("\nChoose a new day: "))

    except ValueError:
        print("\nInvalid input. Please enter a number.")
        return

    if not 1 <= Day_Choice <= len(Available_Days):
        print("\nInvalid day.")
        return

    New_Date = Available_Days[Day_Choice - 1]

    # PREVENT TWO APPOINTMENTS FOR THIS CUSTOMER ON THE SAME DATE

    for Existing in Appointments:

        if (
            Existing is not Appointment
            and Existing["Cellphone"] == Appointment["Cellphone"]
            and Existing["Date"] == New_Date
        ):
            print("\nYou already have another appointment on this date.")
            print("Please choose a different date.")
            return

    # DISPLAY SLOTS, EXCLUDING THIS APPOINTMENT FROM CONFLICT CHECKS

    Available_Slots = []
    Slot_Rows = []

    for Time in Time_Slots:

        Taken = any(
            Existing is not Appointment
            and Existing["Date"] == New_Date
            and Existing["Time"] == Time
            for Existing in Appointments
        )

        if not Taken:
            Available_Slots.append(Time)
            Slot_Number = len(Available_Slots)

            if (
                New_Date == Appointment["Date"]
                and Time == Appointment["Time"]
            ):
                Status = "Current Appointment"

            else:
                Status = "Available"

        else:
            Slot_Number = "-"
            Status = "Taken"

        Slot_Rows.append([Slot_Number, Time, Status])

    print("\n===== TIME SLOT AVAILABILITY =====")

    Print_Table(
        ["No.", "Time Slot", "Availability"],
        Slot_Rows
    )

    if not Available_Slots:
        print("\nNo available time slots for this day.")
        return

    try:
        Time_Choice = int(
            input("\nChoose an available time slot number: ")
        )

    except ValueError:
        print("\nInvalid input. Please enter a number.")
        return

    if not 1 <= Time_Choice <= len(Available_Slots):
        print("\nInvalid time slot.")
        return

    New_Time = Available_Slots[Time_Choice - 1]

    # FINAL AVAILABILITY CHECK

    for Existing in Appointments:

        if Existing is Appointment:
            continue

        if (
            Existing["Date"] == New_Date
            and Existing["Time"] == New_Time
        ):
            print("\nSorry, this time slot has already been taken.")
            return

    Confirm = input(
        "\nSave these appointment changes? (Y/N): "
    ).strip().upper()

    if Confirm == "Y":

        Appointment["Date"] = New_Date
        Appointment["Day"] = New_Date.strftime("%A")
        Appointment["Time"] = New_Time
        Appointment["Status"] = "Pending"

        print("\nAppointment Updated Successfully!")
        print("Approval status reset to Pending.")

        Print_Table(
            ["Customer", "Date", "Day", "Time", "Status"],
            [[
                Appointment["Name"],
                New_Date.strftime("%B %d, %Y"),
                Appointment["Day"],
                New_Time,
                Appointment["Status"]
            ]]
        )

    elif Confirm == "N":
        print("\nUpdate cancelled.")

    else:
        print("\nInvalid choice. Please enter Y or N.")


# VIEW ALL APPOINTMENTS

def View_Appointments():

    print("\n===== ALL APPOINTMENTS =====")

    if not Appointments:
        print("No appointments found.")
        return

    Display_Appointment_List(Appointments)


# APPROVE APPOINTMENT

def Approve_Appointment():

    print("\n===== APPROVE APPOINTMENT =====")

    Pending = [
        Appointment for Appointment in Appointments
        if Appointment["Status"] == "Pending"
    ]

    if not Pending:
        print("No pending appointments found.")
        return

    Display_Appointment_List(Pending)

    try:
        Choice = int(input("\nEnter appointment number to approve: "))

    except ValueError:
        print("\nInvalid input. Please enter a number.")
        return

    if not 1 <= Choice <= len(Pending):
        print("\nInvalid appointment number.")
        return

    Appointment = Pending[Choice - 1]

    Confirm = input(
        "\nApprove this appointment? (Y/N): "
    ).strip().upper()

    if Confirm == "Y":
        Appointment["Status"] = "Approved"
        print("\nAppointment Approved Successfully!")

    elif Confirm == "N":
        print("\nApproval cancelled.")

    else:
        print("\nInvalid choice. Please enter Y or N.")

# RUN PROGRAM

Main_Interface()
