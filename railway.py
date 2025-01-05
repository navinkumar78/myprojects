import mysql.connector
import random

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="naveen",
    database="atm_project"
)
if mydb.is_connected():
    print("Successfully connected to MySQL database")
mycursor = mydb.cursor()

# Menu function
def railresmenu():
    print('''
###############################################################################################################

*     ######     ######   ###########  #         #          #  ######  #       #
      #     #   #      #       #       #         #          # #      #  #     #
      #      #  #      #       #       #         #          # #      #   #   #
      #     #   #      #       #       #         #          # #      #    # #
      ######    ########       #       #         #    ##    # ########     #
      #     #   #      #       #       #         #   #  #   # #      #     #
      #     #   #      #       #       #         #  #    #  # #      #     #
      #     #   #      #       #       #         # #      # # #      #     #
      #     #   #      #  ##########   ######### ##        ## #      #     #

========*******=======***** ======== WELCOME TO INDIAN RAILWAYS==========*****==========****========

=================   1. TRAIN DETAILS   ===================
==================   2. RESERVATION OF TICKET   ==========
==================   3. CANCELLATION OF TICKET   =========
==================   4. DISPLAY PNR STATUS     ==========
===================   5. HELP        ===================
===================   6. QUIT   ===================
''')
    choice = int(input("Enter your choice: "))
    if choice == 1:
        traindetail()
    elif choice == 2:
        reservation()
    elif choice == 3:
        cancel()
    elif choice == 4:
        displayPNR()
    elif choice == 5:
        Help()
    elif choice == 6:
        exit(0)
    else:
        print("Wrong choice")
        railresmenu()

# Train details
def traindetail():
    print("Train Details")
    while True:
        train = []
        name = input("Enter train name: ")
        train.append(name)
        tnum = int(input("Enter train number: "))
        train.append(tnum)
        ac1 = int(input("Enter number of AC 1 class seats: "))
        train.append(ac1)
        ac2 = int(input("Enter number of AC 2 class seats: "))
        train.append(ac2)
        ac3 = int(input("Enter number of AC 3 class seats: "))
        train.append(ac3)
        slp = int(input("Enter number of sleeper class seats: "))
        train.append(slp)

        sql = "INSERT INTO traindetail (tname, tnum, ac1, ac2, ac3, slp) VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql, tuple(train))
        mydb.commit()
        print("Insertion completed.")

        mycursor.execute("SELECT * FROM traindetail")
        data = mycursor.fetchall()
        for row in data:
            print(row)

        ch = input("Do you want to insert more train details (yes/no)? ")
        if ch.lower() == "no":
            break

    railresmenu()

# Reservation
def reservation():
    mycursor.execute("SELECT * FROM traindetail")
    data = mycursor.fetchall()
    for row in data:
        print(row)

    passenger = []
    pname = input("Enter passenger name: ")
    passenger.append(pname)
    age = int(input("Enter age of passenger: "))
    passenger.append(age)
    trainno = int(input("Enter your train number from the above list: "))
    passenger.append(trainno)
    fr = input("Enter boarding station name: ")
    passenger.append(fr)
    to = input("Enter departure station name: ")
    passenger.append(to)
    np = int(input("Enter number of passengers: "))
    passenger.append(np)

    print("Select a class to travel in:")
    print("1. AC FIRST CLASS")
    print("2. AC SECOND CLASS")
    print("3. AC THIRD CLASS")
    print("4. SLEEPER CLASS")
    cp = int(input("Enter your choice: "))
    if cp == 1:
        amount = np * 1000
        cls = 'ac1'
    elif cp == 2:
        amount = np * 800
        cls = 'ac2'
    elif cp == 3:
        amount = np * 500
        cls = 'ac3'
    else:
        amount = np * 350
        cls = 'slp'

    passenger.extend([cls, amount])
    pnr = random.randint(1000000000, 9999999999)
    print("###### Ticket successfully booked ######")
    print("PNR Number:", pnr)
    print("Status: Confirmed")
    passenger.extend(['confirmed', pnr])

    sql = "INSERT INTO passengers (pname, age, trainno, fr, departure, noofpas, cls, amt, status, pnrno) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, tuple(passenger))
    mydb.commit()

    railresmenu()

# Ticket cancellation
def cancel():
    pnr = input("Enter PNR for cancellation: ")
    sql = "UPDATE passengers SET status='deleted' WHERE pnrno=%s"
    mycursor.execute(sql, (pnr,))
    mydb.commit()
    print("Your train ticket has been canceled.")
    railresmenu()

# Display PNR status
def displayPNR():
    pnr = input("Enter PNR number: ")
    sql = "SELECT * FROM passengers WHERE pnrno=%s"
    mycursor.execute(sql, (pnr,))
    res = mycursor.fetchall()
    print("PNR status:")
    for row in res:
        print(row)
    railresmenu()

# Help
def Help():
    print('''
Indian Railways provides the following enquiry numbers:
1. General Enquiry: 131
2. Train Arrival Information: 1331, 1332, 1333, 1334 (by direction)
3. Reservation Enquiry: 135
''')
    railresmenu()

# Start the application
railresmenu()
