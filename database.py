import tkinter as tk
from tkinter import font as tkfont
import mysql.connector
db = mysql.connector.connect(
    host="cosc457.cqe6v4npxals.us-east-2.rds.amazonaws.com",
    user="cosc457",
    passwd="Kigkhte6",
    database='Hospital'
)
cursor= db.cursor()


#Main class that handles the frame changes by stacking frames on top of one another
class frame_change(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family = 'Helvetica', size = 12)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        for F in (main_interface, employee_interface, pat_interface, pat_choices):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("main_interface")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

#Main Menu class
class main_interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = "Welcome to Hospital Databse \n Select a which option to search: ", font = controller.title_font)
        label.grid(columnspan = 2, rowspan = 2)
        
        emp_button = tk.Button(self, text = 'Employee', width = 10, command = lambda: controller.show_frame("employee_interface"))
        emp_button.grid(row = 3, column = 0)
        patient_button = tk.Button(self, text = 'Patient', width = 10, command = lambda: controller.show_frame("pat_interface")) 
        patient_button.grid(row = 3, column = 1)       

#Class shows the employee interface
#Provides buttons to provide info on specific employee's
class employee_interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = "Select a type of employee:  ", font = controller.title_font)
        label.grid(columnspan = 2)

        nurse_button = tk.Button(self, text = 'Nurse', width = 10)
        nurse_button.grid(row = 2, column = 0)
        nurse_button = tk.Button(self, text = 'Doctor', width = 10)
        nurse_button.grid(row = 2, column = 1)
        nurse_button = tk.Button(self, text = 'Receptionist', width = 10)
        nurse_button.grid(row = 3, column = 0)
        nurse_button = tk.Button(self, text = 'Janitor', width = 10)
        nurse_button.grid(row = 3, column = 1)
        nurse_button = tk.Button(self, text = 'Technician', width = 10)
        nurse_button.grid(row = 4, column = 0)
        return_button = tk.Button(self, text = 'Return to Main Menu', width = 16, command = lambda: controller.show_frame("main_interface"))
        return_button.grid(row = 5, columnspan = 2)

#Class shows the patient interface
#Provides a list of patients to click from 
class pat_interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = 'Select a patient:', font = controller.title_font)
        label.grid(columnspan = 2)

        cursor.execute('SELECT FNAME, LNAME FROM PATIENT')
        myresult=cursor.fetchall()
        i=0
        k=2

        
        names=[]
        for row in myresult:
            fullname= row[1]+', '+row[0] #what appears on button
            names.append(row[0]) #first name of patients
            tk.Button(self, text = fullname, width = 10, command = lambda i=i: setName(self,parent,controller, names[i])).grid(row = int(k/2)+1, column = k%2)
            k+=1 #deals with column/row spacing of buttons
            i+=1 #deals with list of first names
        
        

        

        # pat1_button = tk.Button(self, text = 'Doe, John', width = 10, command = lambda: setName(self,parent,controller, 'John'))
        # pat1_button.grid(row = 2, column = 0)
        # pat2_button = tk.Button(self, text = 'Long, Jake', width = 10, command = lambda: setName(self,parent,controller, 'Jake'))
        # pat2_button.grid(row = 2, column = 1)
        # pat3_button = tk.Button(self, text = 'Diez, Joe', width = 10, command = lambda: setName(self,parent,controller, 'Joe'))
        # pat3_button.grid(row = 3, column = 0)
        # pat4_button = tk.Button(self, text = 'Smith, Jason', width = 10, command = lambda: setName(self,parent,controller, 'Jason'))
        # pat4_button.grid(row = 3, column = 1)
        # pat5_button = tk.Button(self, text = 'Kazama, Jin', width = 10, command = lambda: setName(self,parent,controller, 'Jin'))
        # pat5_button.grid(row = 4, column = 0)
        return_button = tk.Button(self, text = 'Return to Main Menu', width = 16, command = lambda: controller.show_frame("main_interface"))
        return_button.grid(columnspan = 2)

class pat_choices(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = 'What information do you \n want about this patient:', font = controller.title_font)
        label.grid(columnspan = 2, rowspan = 2)

        info_button = tk.Button(self, text = 'Patient Info.', width = 10,command = lambda: info())
        info_button.grid(row = 2, column = 0)
        acc_button = tk.Button(self, text = 'Account Info.', width = 10,command = lambda: acc())
        acc_button.grid(row = 2, column = 1)
        appt_button = tk.Button(self, text = 'Appointments', width = 10, command = lambda: appt())
        appt_button.grid(row = 3, column = 0)
        bill_button = tk.Button(self, text = 'Bill', width = 10, command = lambda: bill())
        bill_button.grid(row = 3, column = 1)
        rec_button = tk.Button(self, text = 'Records', width = 10, command = lambda: rec())
        rec_button.grid(row = 4, column = 0)
        return_button = tk.Button(self, text = 'Return to select Patient', command = lambda: controller.show_frame("pat_interface"))
        return_button.grid(columnspan = 2)



def setName(self,parent,controller, temp):
    controller.show_frame("pat_choices")
    global name
    name=temp
    # cursor.execute('SELECT * FROM PATIENT WHERE FNAME =\''+name+'\'')
    # myresult=cursor.fetchall()

    #for row in myresult:
        #print(row)

def info():
    cursor.execute('SELECT * FROM PATIENT WHERE FNAME =\''+name+'\'')
    myresult=cursor.fetchall()
    msg=''
    for row in myresult:   
        msg = "Patient ID: "+ row[0]+ "\nFirst Name: "+ row[1]+ "\nLast Name: "+ row[2]+"\nDOB: "+ str(row[3])+"\nAddress: "+row[4]+","+row[5]+","+row[6]
    title= name+"'s Patient Information"
    popupmsg(msg,title)
    #Print in terminal
    # print()
    # print("****Patient Information****")
    # for row in myresult:
    #     print("The Patient Id:", row[0])
    #     print("The First Name: ", row[1])
    #     print("The Last Name: ", row[2])
    #     print("The DOB: ", row[3])
    #     print("The Address: ", row[4],',', row[5],',', row[6])

    
def acc():
    cursor.execute('SELECT * FROM PATIENT_ACCOUNT WHERE PATIENT_ID= (SELECT PATIENT_ID FROM PATIENT WHERE FNAME=\''+name+'\')')
    myresult=cursor.fetchall()
    msg=''
    for row in myresult:   
        msg = "Patient ID: "+ row[0]+ "\nAccount Number: "+ row[1]+ "\nInsurance: "+ row[2]+"\nAccount Password: "+ row[3]
    title= name+"'s Account Information"
    popupmsg(msg,title)
    #Print in terminal
    # print()
    # print("****Account Information****")
    # for row in myresult:
    #     print("The Patient Id:", row[0])
    #     print("Account Number: ", row[1])
    #     print("Insurance: ", row[2])
    #     print("Account Password: ", row[3])

def appt():
    cursor.execute('SELECT * FROM APPOINTMENTS WHERE ACCOUNT_NUM=(SELECT ACCOUNT_NUM FROM PATIENT_ACCOUNT WHERE PATIENT_ID= (SELECT PATIENT_ID FROM PATIENT WHERE FNAME= \''+name+'\'))')
    myresult=cursor.fetchall()
    msg=''
    for row in myresult:   
        msg = "Test: "+ row[0]+ "\nAccount Number: "+ row[1]+ "\nDoctor ID: "+ row[2]+"\nReceipt ID: "+ row[3]
    title= name+"'s Appointments"
    popupmsg(msg,title)
    #Print in terminal
    # print()
    # print("****Appointments****")
    # for row in myresult:
    #     #print(row)
    #     print("Test: ", row[0])
    #     print("Account Number: ", row[1])
    #     print("Doctor ID: ", row[2])
    #     print("Receipt ID: ", row[3])

def bill():
    cursor.execute('SELECT * FROM BILL WHERE ACCOUNT_NUM=(SELECT ACCOUNT_NUM FROM PATIENT_ACCOUNT WHERE PATIENT_ID= (SELECT PATIENT_ID FROM PATIENT WHERE FNAME= \''+name+'\'))')  
    myresult=cursor.fetchall()

    msg=''
    for row in myresult:   
        msg = "Account Number: "+ row[0]+ "\nCopay: $"+ str(row[1])+ "\nAmount: $"+ str(row[2])+"\nDue Date: "+ str(row[3])
    title= name+"'s Bill"
    popupmsg(msg,title)
    #Print in terminal
    # print()
    # print("****Bill****")
    # for row in myresult:
    #     print("Account Number: ", row[0])
    #     print("Copay: $", row[1])
    #     print("Amount: $", row[2])
    #     print("Due Date: ", row[3])

def rec():    
    cursor.execute('SELECT * FROM RECORD WHERE ACCOUNT_NUM=(SELECT ACCOUNT_NUM FROM PATIENT_ACCOUNT WHERE PATIENT_ID= (SELECT PATIENT_ID FROM PATIENT WHERE FNAME= \''+name+'\'))')
    myresult=cursor.fetchall()
    msg=''
    flag=True
    for row in myresult:  
        if(flag): 
            msg = "Account Number: "+ row[0]+ "\nRecords: "+ row[1]
            flag=False
        msg=msg+'\n'+row[1]
    title= name+"'s Record"
    popupmsg(msg,title)
    #Print in terminal
    # print()
    # print("****Records****")
    # flag=True
    # for row in myresult:
    #     if (flag):
    #         print("Account Number:", row[0])
    #         flag=False
    #     print("Record: ", row[1])

Font=("Verdana", 12)

def popupmsg(msg,title):
    popup = tk.Tk()
    popup.wm_title(title)
    label= tk.Label(popup, text=msg, font=Font)
    label.pack(side="top", fill="x", pady=10)
    B1= tk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()



if __name__ == "__main__":
    app = frame_change()
    app.mainloop()

db.close()