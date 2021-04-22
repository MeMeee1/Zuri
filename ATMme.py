from datetime import datetime
import sys
import random
import sqlite3

try:
    connection2 = sqlite3.connect('complaint.sqlite')
    cursor2 = connection2.cursor()
    cursor2.execute('SELECT * FROM Complaints')
    connection2.close()
except:
    connection2 = sqlite3.connect('complaint.sqlite')
    cursor2 = connection2.cursor()
    cursor2.execute('CREATE TABLE Complaints(id INTEGER , complaint TEXT)')
    connection2.commit()
    connection2.close()    
    
try:
    conn = sqlite3.connect('user.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT acctNo,username, balance FROM Users')
    
except:
    conn = sqlite3.connect('user.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE Users( acctNo INTEGER, username TEXT, password TEXT, phone TEXT, balance INTEGER)')
    cur.execute('INSERT INTO Users(acctNo , username , password , phone, balance ) VALUES (?,?,?,?,?)' , (100, 'BAD', 'bad', '231', 200))
    conn.commit()

    
x = datetime.now()
print('*******SYSTEM TIME: %s********'%x)

def init():
    while True:
        haveAccount= (input('Please do you have an account with The Trust Bank?\n 1 (Yes)\n 2 (No)\n')).lower()
        if(haveAccount == '1') or (haveAccount == 'yes'):
            print('Welcome dear valued customer')
            login()
            sys.exit()
        elif(haveAccount == '2') or (haveAccount == 'no'):
            print('Please register, before you can access your funds')
            register()
            sys.exit()
        else:
            print('Please enter a valid option')

def keepUsing():
    var =True
    while var:
        response = input('Would you like to perform another action?\n1.Yes 2.No\n')
        if response == '1':
            init()
            var = False
        elif response == '2':
            print('Thanks for using our service')
            conn.close()
            var = False
        else:
            print('Invalid option\n')
def login():
    print('*******LOGIN**************')
    print('Please log-in to your account')

    while True:
        ok= False
        userName = input("What is your user name? \n")
        userPassword = input("What is your unique password? \n")
        try:    
        
            cur = conn.cursor()
            
            cur.execute('SELECT acctNo , username , password , phone, balance  FROM Users WHERE (username = ? AND password = ?) ', (userName, userPassword))
            userProfile = cur.fetchall()
            
            if userProfile != []:
                ok = True
            
        except:
            pass
        if ok:
            bankOpperate(userProfile)
            break
        if ok == False:
            print('Your entry is invalid.')

            print('Please ensure to enter a valid user name and password. ')
            ok = False
            print('Fail')
def bankOpperate(user):
    print("Welcome user {}".format(user[0][1]))
    print('Available Actions')
    print("1. Withdrawal\n2. Deposit\n3. Account Balance\n4. Transfer\n5. Complaint")
    response = input('What would you like to do today:\n')
    acctBalance = user[0][-1]
    if response == '1':
        print('You selected option %s' %response)  # Withdrawal
        amt = int(input('How much would you like to Withdraw?: \n'))
        if amt <=  acctBalance:
             acctBalance -= amt
             print('You have withdrawn N%g\nCurrent Balance : N%g\nAccount Number : %d' %(amt, acctBalance, user[0][0]))
             cur= conn.cursor()
             cur.execute("UPDATE Users SET balance = (?) WHERE username = (?)", ((acctBalance) ,(user[0][1])))
             conn.commit()
             keepUsing()
        else:
            print('Insufficient Funds')
            keepUsing()
    if response == '2':
        print('You selected option %s' %response) # Deposit
        amt = int(input('How much would you like to Deposit?: \n'))
        acctBalance += amt
        print('You have deposited N%g\nCurrent Balance : N%g \nAccount Number : %d' %(amt, acctBalance, user[0][0]))
        cur= conn.cursor()
        cur.execute("UPDATE Users SET balance = (?) WHERE username = (?)", ((acctBalance) ,(user[0][1])))
        conn.commit()
        keepUsing()
    if response == '3':
        print('You selected option %s' %response) # Check Balance
        print('Account Number: %d\nCurrent Balance : N%g' %(user[0][0], acctBalance))
        keepUsing()

    if response == '4':
        print('You selected option %s' %response) #Transfer
        target = int(input('Enter the account number of the receipient: '))
        amt = int(input('Enter the amount to transfer'))
        try:
            cur= conn.cursor()
            cur.execute("SELECT *  FROM Users WHERE acctNo = (?)" , (target,))
            target = cur.fetchall()
            print(target)
            print(target[0][4])
            a = target[0][-1]
            if amt <=  acctBalance:
                 acctBalance -= amt
                 a += amt
                 print('You have withdrawn N%g\nCurrent Balance : N%g\nAccount Number : %d' %(amt, acctBalance, user[0][0]))
                 cur= conn.cursor()
                 cur.execute("UPDATE Users SET balance = (?) WHERE acctNo = (?)", ((acctBalance) ,(user[0][0]),))
                 cur.execute("UPDATE Users SET balance = (?) WHERE acctNo = (?)", ((a ), (target[0][0]),))
                 conn.commit()
                 keepUsing()
            else:
                print('Insufficient funds')
                keepUsing()
                 
        except:
            print('Receipient user does not exist')
            keepUsing()

    if response == '5':                            # Complaint 
        print('You selected option %s' %response)
        complaint = input('Enter complaint :')
        connection2 = sqlite3.connect('complaint.sqlite')
        cursor2 = connection2.cursor()
        cursor2.execute('INSERT INTO Complaints(id, complaint) VALUES (?, ?)', (user[0][0], complaint))
        connection2.commit()
        connection2.close()
        keepUsing()

def register():
    x = True
    while x:
        name= input('Enter your username:\n')
        userPassword= input('Enter your secret password: ')
        confirm = input("Confirm password:  ")
    
        if userPassword == confirm :
            userPhone = input('Enter phone number:  ')
            cur = conn.cursor()
            cur.execute('INSERT INTO Users(acctNo , username , password , phone, balance) VALUES (?,?,?,?,?)', (acctNoGenerator(), name, userPassword, userPhone, 0 ))
            conn.commit()
            x = False
            keepUsing()
        else:
            print('Passwords do not tally. Try Again.')
    
def acctNoGenerator():
    cur = conn.cursor()
    cur.execute('SELECT acctNo FROM Users')
    acctNumbers = cur.fetchall()
    ex = True
    while ex:
        num = random.randint(1111111111, 9999999999)
        for i,e in enumerate(acctNumbers):
            if num in acctNumbers[i]:
                pass
            else:
                ex = False
    return num


init()
