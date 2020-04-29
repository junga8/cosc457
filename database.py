import tkinter as tk
from tkinter import font as tkfont
import mysql.connector
db = mysql.connector.connect(
    host="cosc457.cqe6v4npxals.us-east-2.rds.amazonaws.com",
    user="cosc457",
    passwd="Kigkhte6",
    database='Hospital')
cursor = db.cursor()


#Main class that handles the frame changes by stacking frames on top of one another
class frame_change(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=12)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (login_interface, main_interface, employee_interface, pat_interface,
                  pat_choices, new_pat_interface, new_info, new_acc,
                  new_bill, new_appt, new_rec, create_appt, alt_appt, delete_appt, alt_bill):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        #self.show_frame("login_interface")
        self.show_frame("login_interface")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class login_interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #label = tk.Label(self,text= 'Hospital Database Login',font=controller.title_font)
        userlabel = tk.Label(self,text='Username:',font=controller.title_font)
        userlabel.grid(row=2,column=1, columnspan=2)
        pwlabel = tk.Label(self,text='Password:',font=controller.title_font)
        pwlabel.grid(row=3,column=1, columnspan=2)
        unentry = tk.Entry(self)
        unentry.grid(row=2, column=3)
        pwentry = tk.Entry(self, show="*")
        pwentry.grid(row=3, column=3)
        submit = tk.Button(self,text='Submit',width=10,command=lambda: check(self,parent, controller,unentry.get(), pwentry.get()))
        submit.grid(row=4, column=3)


def check(self,parent, controller,un, pw):
    username="admin"
    password="password"
    
    #controller.show_frame("main_interface")
    if(un==username and pw==password):
        #print("Welcome")
        controller.show_frame("main_interface")
    else:
        print("Incorrect Username or Password")

#Main Menu class
class main_interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(
            self,
            text=
            "Welcome to Hospital Database \n Select a which option to search: ",
            font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        emp_button = tk.Button(
            self,
            text='Employee',
            width=10,
            command=lambda: controller.show_frame("employee_interface"))
        emp_button.grid(row=3, column=0)
        patient_button = tk.Button(
            self,
            text='Patient',
            width=10,
            command=lambda: controller.show_frame("pat_interface"))
        patient_button.grid(row=3, column=1)


#Class shows the employee interface
#Provides buttons to provide info on specific employee's
class employee_interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,
                         text="Select a type of employee:  ",
                         font=controller.title_font)
        label.grid(columnspan=2)

        nurse_button = tk.Button(self,
                                 text='Nurse',
                                 width=10,
                                 command=lambda: nurses())
        nurse_button.grid(row=2, column=0)
        nurse_button = tk.Button(self,
                                 text='Doctor',
                                 width=10,
                                 command=lambda: doctor())
        nurse_button.grid(row=2, column=1)

        nurse_button = tk.Button(self,
                                 text='Receptionist',
                                 width=10,
                                 command=lambda: receptionist())
        nurse_button.grid(row=3, column=0)
        nurse_button = tk.Button(self,
                                 text='Janitor',
                                 width=10,
                                 command=lambda: janitor())
        nurse_button.grid(row=3, column=1)
        nurse_button = tk.Button(self,
                                 text='Technician',
                                 width=10,
                                 command=lambda: tech())
        nurse_button.grid(row=4, column=0)
        return_button = tk.Button(
            self,
            text='Return to Main Menu',
            width=16,
            command=lambda: controller.show_frame("main_interface"))
        return_button.grid(row=5, columnspan=2)


#Class shows the patient interface
#Provides a list of patients to click from
class pat_interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,
                         text='Enter Patient ID:',
                         font=controller.title_font)
        label.grid(columnspan=2)

        entry = tk.Entry(self)
        entry.grid(row=1, column=0)
        cursor.execute('SELECT * FROM PATIENT WHERE PATIENT_ID =\'' +
                       entry.get() + '\'')
        myresult = cursor.fetchall()
        for row in myresult:
            print(row)
        button = tk.Button(
            self,
            text='Enter',
            command=lambda: setPid(self, parent, controller, entry.get()))
        button.grid(row=1, column=1)

        # Use entry.get() to acquire input, does not have to be declared to a variable
        add_button = tk.Button(self,
                               text='List of Patients',
                               width=16,
                               command=lambda: patients())
        add_button.grid(columnspan=2)
        add_button = tk.Button(
            self,
            text='Add new Patient',
            width=16,
            command=lambda: controller.show_frame("new_pat_interface"))
        add_button.grid(columnspan=2)
        add_button = tk.Button(self,
                               text='Alter an Appointment',
                               width=16,
                               command=lambda:controller.show_frame("alt_appt"))
        add_button.grid(columnspan=2)
        add_button = tk.Button(self,
                               text='Change Bill',
                               width=16,
                               command=lambda: controller.show_frame("alt_bill"))
        add_button.grid(columnspan=2)
        return_button = tk.Button(
            self,
            text='Return to Main Menu',
            width=16,
            command=lambda: controller.show_frame("main_interface"))
        return_button.grid(columnspan=2)


class pat_choices(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(
            self,
            text='What information do you \n want about this patient:',
            font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        info_button = tk.Button(self,
                                text='Patient Info.',
                                width=10,
                                command=lambda: info())
        info_button.grid(row=2, column=0)
        acc_button = tk.Button(self,
                               text='Account Info.',
                               width=10,
                               command=lambda: acc())
        acc_button.grid(row=2, column=1)
        appt_button = tk.Button(self,
                                text='Appointments',
                                width=10,
                                command=lambda: appt())
        appt_button.grid(row=3, column=0)
        bill_button = tk.Button(self,
                                text='Bill',
                                width=10,
                                command=lambda: bill())
        bill_button.grid(row=3, column=1)
        rec_button = tk.Button(self,
                               text='Records',
                               width=10,
                               command=lambda: rec())
        rec_button.grid(row=4, column=0)
        return_button = tk.Button(
            self,
            text='Return to select Patient',
            command=lambda: controller.show_frame("pat_interface"))
        return_button.grid(columnspan=2)


class new_pat_interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self,
                         text='New Patient Information',
                         font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        info_button = tk.Button(
            self,
            text='Patient Info.',
            width=10,
            command=lambda: controller.show_frame("new_info"))
        info_button.grid(row=2, column=0)
        acc_button = tk.Button(
            self,
            text='Account Info.',
            width=10,
            command=lambda: controller.show_frame("new_acc"))
        acc_button.grid(row=2, column=1)
        appt_button = tk.Button(
            self,
            text='Appointments',
            width=10,
            command=lambda: controller.show_frame("new_appt"))
        appt_button.grid(row=3, column=0)
        bill_button = tk.Button(
            self,
            text='Bill',
            width=10,
            command=lambda: controller.show_frame("new_bill"))
        bill_button.grid(row=3, column=1)
        rec_button = tk.Button(
            self,
            text='Records',
            width=10,
            command=lambda: controller.show_frame("new_rec"))
        rec_button.grid(row=4, column=0)

        return_button = tk.Button(
            self,
            text='Return to select Patient',
            command=lambda: controller.show_frame("pat_interface"))
        return_button.grid(columnspan=2)


def setPid(self, parent, controller, temp):
    controller.show_frame("pat_choices")
    global pid
    pid = temp


class new_info(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,
                         text='Update Information',
                         font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        tk.Label(self, text="Patient ID").grid(row=2)
        tk.Label(self, text="First Name").grid(row=3)
        tk.Label(self, text="Last Name").grid(row=4)
        tk.Label(self, text="DOB").grid(row=5)
        tk.Label(self, text="Street Address").grid(row=6)
        tk.Label(self, text="Zipcode").grid(row=7)
        tk.Label(self, text="State").grid(row=8)

        patientID_entry = tk.Entry(self)
        fname_entry = tk.Entry(self)
        lname_entry = tk.Entry(self)
        dob_entry = tk.Entry(self)
        street_entry = tk.Entry(self)
        zip_entry = tk.Entry(self)
        state_entry = tk.Entry(self)

        patientID_entry.grid(row=2, column=1)
        fname_entry.grid(row=3, column=1)
        lname_entry.grid(row=4, column=1)
        dob_entry.grid(row=5, column=1)
        street_entry.grid(row=6, column=1)
        zip_entry.grid(row=7, column=1)
        state_entry.grid(row=8, column=1)

        def save():
            print("Updated Patient Info")

            cursor.execute(
                'INSERT INTO PATIENT(PATIENT_ID, FNAME, LNAME, DOB, ST_ADDR, ZIP, STATE) VALUES('
                + patientID_entry.get() + ', \'' + fname_entry.get() +
                '\', \'' + lname_entry.get() + '\', \'' + dob_entry.get() +
                '\', \'' + street_entry.get() + '\', ' + zip_entry.get() +
                ', \'' + state_entry.get() + '\');')

            # cursor.execute('''
            # INSERT INTO PATIENT(PATIENT_ID, FNAME, LNAME, DOB, ST_ADDR, ZIP, STATE)
            # VALUES('1234', 'test', 'testl', '1998-04-13', '123 test', '12345', 'md');
            # ''')
            db.commit()

        tk.Button(self, text='Save', command=lambda: save()).grid(row=9,
                                                                  column=1,
                                                                  sticky=tk.W,
                                                                  pady=4)

        return_button = tk.Button(
            self,
            text='Return to select Patient',
            command=lambda: controller.show_frame("new_pat_interface"))
        return_button.grid(columnspan=2)


class new_acc(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,
                         text='Update Information',
                         font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        tk.Label(self, text="Patient ID").grid(row=2)
        tk.Label(self, text="Account Number").grid(row=3)
        tk.Label(self, text="Insurance").grid(row=4)
        tk.Label(self, text="Account PW").grid(row=5)

        patientID_entry = tk.Entry(self)
        accNum_entry = tk.Entry(self)
        insurance_entry = tk.Entry(self)
        pw_entry = tk.Entry(self)

        patientID_entry.grid(row=2, column=1)
        accNum_entry.grid(row=3, column=1)
        insurance_entry.grid(row=4, column=1)
        pw_entry.grid(row=5, column=1)

        def save():
            print("Updated Account Info")

            cursor.execute(
                'INSERT INTO PATIENT_ACCOUNT(PATIENT_ID, ACCOUNT_NUM, INSURANCE, ACCT_PASSWORD) VALUES('
                + patientID_entry.get() + ', \'' + accNum_entry.get() +
                '\', \'' + insurance_entry.get() + '\', \'' + pw_entry.get() +
                '\');')
            # cursor.execute('''
            # INSERT INTO PATIENT_ACCOUNT(PATIENT_ID, ACCOUNT_NUM, INSURANCE, ACCT_PASSWORD)
            # VALUES(1234, '123456', 'medstar', 'pass');
            #  ''')
            db.commit()

        tk.Button(self, text='Save', command=lambda: save()).grid(row=9,
                                                                  column=1,
                                                                  sticky=tk.W,
                                                                  pady=4)

        return_button = tk.Button(
            self,
            text='Return to select Patient',
            command=lambda: controller.show_frame("new_pat_interface"))
        return_button.grid(columnspan=2)


class new_bill(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,
                         text='Update Information',
                         font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        tk.Label(self, text="Account Number: ").grid(row=2)
        tk.Label(self, text="Copay: $").grid(row=3)
        tk.Label(self, text="Amount: $").grid(row=4)
        tk.Label(self, text="Due Date: ").grid(row=5)
        acct_num_entry = tk.Entry(self)
        copay_entry = tk.Entry(self)
        amount_entry = tk.Entry(self)
        due_entry = tk.Entry(self)

        acct_num_entry.grid(row=2, column=1)
        copay_entry.grid(row=3, column=1)
        amount_entry.grid(row=4, column=1)
        due_entry.grid(row=5, column=1)

        def save():
            print("Updated Bill Info")

            cursor.execute(
                'INSERT INTO BILL(ACCOUNT_NUM, COPAY, AMOUNT, DUE_DATE) VALUES('
                + acct_num_entry.get() + ', \'' + copay_entry.get() +
                '\', \'' + amount_entry.get() + '\', \'' + due_entry.get() +
                '\');')
            # print('INSERT INTO BILL(ACCOUNT_NUM, COPAY, AMOUNT, DUE_DATE) VALUES('+acct_num_entry.get()+', \''+copay_entry.get()+'\', \''+amount_entry.get()+'\', \''+due_entry.get()+'\');')
            # cursor.execute('''
            # INSERT INTO BILL(ACCOUNT_NUM, COPAY, AMOUNT, DUE_DATE)
            # VALUES(123456, '55', '120', '2020-04-25');
            # ''')
            db.commit()

        tk.Button(self, text='Save', command=lambda: save()).grid(row=9,
                                                                  column=1,
                                                                  sticky=tk.W,
                                                                  pady=4)

        return_button = tk.Button(
            self,
            text='Return to select Patient',
            command=lambda: controller.show_frame("new_pat_interface"))
        return_button.grid(columnspan=2)


class new_appt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,
                         text='Update Information',
                         font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        tk.Label(self, text="Test").grid(row=2)
        tk.Label(self, text="Account Number").grid(row=3)
        tk.Label(self, text="Doctor ID").grid(row=4)
        tk.Label(self, text="Receptionist ID").grid(row=5)
        tk.Label(self, text="Appointment Date").grid(row=6)

        test_entry = tk.Entry(self)
        accNum_entry = tk.Entry(self)
        doctor_entry = tk.Entry(self)
        recept_entry = tk.Entry(self)
        appt_entry = tk.Entry(self)

        test_entry.grid(row=2, column=1)
        accNum_entry.grid(row=3, column=1)
        doctor_entry.grid(row=4, column=1)
        recept_entry.grid(row=5, column=1)
        appt_entry.grid(row=6, column=1)

        def save():
            print("Updated Appointment Info")

            cursor.execute(
                 'INSERT INTO APPOINTMENTS(TEST, ACCOUNT_NUM, DOCTOR_ID, RECEPT_ID, appt_date) VALUES('+'\''+test_entry.get()+'\', \''
             +accNum_entry.get()+'\', \''+doctor_entry.get()+'\', \''+recept_entry.get()+'\', \''+appt_entry.get()+'\');')
            
            # print('INSERT INTO APPOINTMENTS(TEST, ACCOUNT_NUM, DOCTOR_ID, RECEPT_ID, appt_date) VALUES('+'\''+test_entry.get()+'\', \''+accNum_entry.get()+'\', \''+doctor_entry.get()+'\', \''+recept_entry.get()+'\', \''+appt_entry.get()+'\');')
            # cursor.execute('''
            # INSERT INTO APPOINTMENTS(TEST, ACCOUNT_NUM, DOCTOR_ID, RECEPT_ID)
            # VALUES('PHYSICAL', '123456', '1', '1R');
            # ''')
            db.commit()

        tk.Button(self, text='Save', command=lambda: save()).grid(row=9,
                                                                  column=1,
                                                                  sticky=tk.W,
                                                                  pady=4)

        return_button = tk.Button(
            self,
            text='Return to select Patient',
            command=lambda: controller.show_frame("new_pat_interface"))
        return_button.grid(columnspan=2)

class create_appt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,
                         text='Create Appointment',
                         font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        tk.Label(self, text="Test").grid(row=2)
        tk.Label(self, text="Account Number").grid(row=3)
        tk.Label(self, text="Doctor ID").grid(row=4)
        tk.Label(self, text="Receptionist ID").grid(row=5)
        tk.Label(self, text="Appointment Date").grid(row=6)


        test_entry = tk.Entry(self)
        accNum_entry = tk.Entry(self)
        doctor_entry = tk.Entry(self)
        recept_entry = tk.Entry(self)
        appt_entry = tk.Entry(self)

        test_entry.grid(row=2, column=1)
        accNum_entry.grid(row=3, column=1)
        doctor_entry.grid(row=4, column=1)
        recept_entry.grid(row=5, column=1)
        appt_entry.grid(row=6, column=1)

        def save():
            print("Updated Appointment Info")

            cursor.execute(
                 'INSERT INTO APPOINTMENTS(TEST, ACCOUNT_NUM, DOCTOR_ID, RECEPT_ID, appt_date) VALUES('+'\''+test_entry.get()+'\', \''
             +accNum_entry.get()+'\', \''+doctor_entry.get()+'\', \''+recept_entry.get()+'\', \''+appt_entry.get()+'\');')
            #print('INSERT INTO APPOINTMENTS(TEST, ACCOUNT_NUM, DOCTOR_ID, RECEPT_ID) VALUES('+test_entry.get()+', \''+accNum_entry.get()+'\', \''+doctor_entry.get()+'\', \''+recept_entry.get()+'\');')
            # cursor.execute('''
            # # INSERT INTO APPOINTMENTS(TEST, ACCOUNT_NUM, DOCTOR_ID, RECEPT_ID)
            # # VALUES('PHYSICAL', '123456', '1', '1R');
            # # ''')
            db.commit()

        tk.Button(self, text='Save', command=lambda: save()).grid(row=9,
                                                                  column=1,
                                                                  sticky=tk.W,
                                                                  pady=4)

        return_button = tk.Button(
            self,
            text='Return',
            command=lambda: controller.show_frame("alt_appt"))
        return_button.grid(columnspan=2)

class delete_appt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,
                         text='Delete an Appointment',
                         font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        tk.Label(self, text="Test").grid(row=2)
        tk.Label(self, text="Account Number").grid(row=3)


        test_entry = tk.Entry(self)
        accNum_entry = tk.Entry(self)


        test_entry.grid(row=2, column=1)
        accNum_entry.grid(row=3, column=1)


        def save():
            print("Appointment Deleted")

            cursor.execute(
                 'DELETE FROM APPOINTMENTS WHERE ACCOUNT_NUM='+'\''+accNum_entry.get()+'\'AND TEST=\''
             +test_entry.get()+'\'')
            #print('DELETE FROM APPOINTMENTS WHERE ACCOUNT_NUM='+'\''+accNum_entry.get()+'\'AND TEST=\''+test_entry.get()+'\'')
            # cursor.execute('''
            # INSERT INTO APPOINTMENTS(TEST, ACCOUNT_NUM, DOCTOR_ID, RECEPT_ID)
            # VALUES('PHYSICAL', '123456', '1', '1R');
            # ''')
            db.commit()

        tk.Button(self, text='Save', command=lambda: save()).grid(row=9,
                                                                  column=1,
                                                                  sticky=tk.W,
                                                                  pady=4)

        return_button = tk.Button(
            self,
            text='Return',
            command=lambda: controller.show_frame("alt_appt"))
        return_button.grid(columnspan=2)

class new_rec(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,
                         text='Update Information',
                         font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        tk.Label(self, text="Account Number").grid(row=2)
        tk.Label(self, text="Document").grid(row=3)

        acct_num_entry = tk.Entry(self)
        doc_entry = tk.Entry(self)

        acct_num_entry.grid(row=2, column=1)
        doc_entry.grid(row=3, column=1)

        def save():
            print("Updated Record Info")

            cursor.execute(
                'INSERT INTO RECORD(ACCOUNT_NUM, DOCUMENT) VALUES(' +
                acct_num_entry.get() + ', \'' + doc_entry.get() + '\');')
            #print('INSERT INTO PATIENT_ACCOUNT(ACCOUNT_NUM, DOCUMENT) VALUES('+acct_num_entry.get()+', \''+doc_entry.get()+'\');')
            # cursor.execute('''
            # INSERT INTO RECORD(ACCOUNT_NUM, DOCUMENT)
            # VALUES(123456, 'test had a surgery done.');
            # ''')
            db.commit()

        tk.Button(self, text='Save', command=lambda: save()).grid(row=9,
                                                                  column=1,
                                                                  sticky=tk.W,
                                                                  pady=4)

        return_button = tk.Button(
            self,
            text='Return to select Patient',
            command=lambda: controller.show_frame("new_pat_interface"))
        return_button.grid(columnspan=2)

class alt_appt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(
            self,
            text=
            "Appointment Management ",
            font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        emp_button = tk.Button(
            self,
            text='Make an Appointment',
            width=20,
            command=lambda: controller.show_frame("create_appt"))
        emp_button.grid(row=3, column=0)
        patient_button = tk.Button(
            self,
            text='Delete an Appointment',
            width=20,
            command=lambda: controller.show_frame("delete_appt"))
        return_button = tk.Button(
            self,
            text='Return',
            command=lambda: controller.show_frame("pat_interface"))
        return_button.grid(columnspan=2)
        patient_button.grid(row=3, column=1)

class alt_bill(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,
                         text='Update Bill',
                         font=controller.title_font)
        label.grid(columnspan=2, rowspan=2)

        tk.Label(self, text="Account Number: ").grid(row=2)
        tk.Label(self, text="New Copay: $").grid(row=3)
        tk.Label(self, text="New Amount: $").grid(row=4)
        tk.Label(self, text="New Due Date: ").grid(row=5)
        acct_num_entry = tk.Entry(self)
        copay_entry = tk.Entry(self)
        amount_entry = tk.Entry(self)
        due_entry = tk.Entry(self)

        acct_num_entry.grid(row=2, column=1)
        copay_entry.grid(row=3, column=1)
        amount_entry.grid(row=4, column=1)
        due_entry.grid(row=5, column=1)

        def save():
            print("Updated Bill Info")
            # cursor.execute('''SET SQL_SAFE_UPDATES=0;''')
            # db.commit()
            cursor.execute(
                 'UPDATE BILL SET COPAY=\'' + copay_entry.get() +
                 '\', AMOUNT=\''+ amount_entry.get() + '\', DUE_DATE=\''+ due_entry.get()+'\'WHERE ACCOUNT_NUM=\''+acct_num_entry.get() + '\';')
            print('UPDATE BILL SET COPAY=\'' + copay_entry.get() +'\', AMOUNT=\''+ amount_entry.get() + '\', DUE_DATE=\''+ due_entry.get()+'\'WHERE ACCOUNT_NUM=\''+amount_entry.get() + '\';')

            db.commit()

        tk.Button(self, text='Save', command=lambda: save()).grid(row=9,
                                                                  column=1,
                                                                  sticky=tk.W,
                                                                  pady=4)

        return_button = tk.Button(
            self,
            text='Return',
            command=lambda: controller.show_frame("pat_interface"))
        return_button.grid(columnspan=2)
     

def patients():
    cursor.execute('SELECT FNAME, LNAME, PATIENT_ID FROM PATIENT')
    myresult = cursor.fetchall()
    msg = ''
    finalmsg = ''
    for row in myresult:
        msg = "First Name: " + row[0] + "\tLast Name: " + row[
            1] + "\tPatient ID: " + row[2] + "\t"
        finalmsg = finalmsg + "\t\n" + msg
    title = "List of Patients"

    popupmsg(finalmsg, title)


def nurses():
    cursor.execute(
        'SELECT FNAME, LNAME,SCHED FROM STAFF, NURSE WHERE STAFF.EMPLOYEE_ID = NURSE.EMPLOYEE_ID '
    )
    myresult = cursor.fetchall()
    msg = ''
    finalmsg = ''
    for row in myresult:
        msg = "First Name:" + row[0] + '\t' + "Last Name:" + row[
            1] + '\t' + "Schedule:" + row[2] + "\n"
        finalmsg = finalmsg + "\n" + msg

    title = " List of Nurses"
    popupmsg(finalmsg, title)


def doctor():
    cursor.execute(
        'SELECT FNAME, LNAME,SCHED, WARD FROM STAFF, DOCTOR WHERE STAFF.EMPLOYEE_ID = DOCTOR.EMPLOYEE_ID '
    )
    myresult = cursor.fetchall()
    msg = ''
    finalmsg = ''
    for row in myresult:
        msg = "First Name:" + row[0] + '\t' + "Last Name:" + row[
            1] + '\t' + "Schedule:" + row[2] + '\t' + "Ward:" + row[3] + "\n"
        finalmsg = finalmsg + "\n" + msg

    title = " List of Doctors"
    popupmsg(finalmsg, title)


def receptionist():
    cursor.execute(
        'SELECT FNAME, LNAME,SCHED, WARD FROM STAFF, RECEPTIONIST WHERE STAFF.EMPLOYEE_ID = RECEPTIONIST.EMPLOYEE_ID '
    )
    myresult = cursor.fetchall()
    msg = ''
    finalmsg = ''
    for row in myresult:
        msg = "First Name:" + row[0] + '\t' + "Last Name:" + row[
            1] + '\t' + "Schedule:" + row[2] + '\t' + "Ward:" + row[3] + "\n"
        finalmsg = finalmsg + "\n" + msg

    title = " List of RECPTIONIST"
    popupmsg(finalmsg, title)


def janitor():
    cursor.execute(
        'SELECT FNAME, LNAME,SCHED, WARD FROM STAFF, JANITOR WHERE JANITOR.EMPLOYEE_ID = STAFF.EMPLOYEE_ID '
    )
    myresult = cursor.fetchall()
    msg = ''
    finalmsg = ''
    for row in myresult:
        msg = "First Name:" + row[0] + '\t' + "Last Name:" + row[
            1] + '\t' + "Schedule:" + row[2] + '\t' + "Ward:" + row[3] + "\n"
        finalmsg = finalmsg + "\n" + msg

    title = " List of Janitors"
    popupmsg(finalmsg, title)


def tech():
    cursor.execute(
        'SELECT FNAME, LNAME,SCHED, AREA_EXP FROM STAFF, TECHNICIAN WHERE STAFF.EMPLOYEE_ID = TECHNICIAN.EMPLOYEE_ID '
    )
    myresult = cursor.fetchall()
    msg = ''
    finalmsg = ''
    for row in myresult:
        msg = "First Name:" + row[0] + '\t' + "Last Name:" + row[
            1] + '\t' + "Schedule:" + row[
                2] + '\t' + "Area of expertie:" + row[3] + "\n"
        finalmsg = finalmsg + "\n" + msg

    title = " List of Technicians "
    popupmsg(finalmsg, title)


def info():
    cursor.execute('SELECT * FROM PATIENT WHERE PATIENT_ID =\'' + pid + '\'')
    myresult = cursor.fetchall()
    msg = ''
    for row in myresult:
        msg = "Patient ID: " + row[0] + "\nFirst Name: " + row[
            1] + "\nLast Name: " + row[2] + "\nDOB: " + str(
                row[3]) + "\nAddress: " + row[4] + "," + row[5] + "," + row[6]
    cursor.execute('SELECT FNAME, LNAME FROM PATIENT WHERE PATIENT_ID =\'' +
                   pid + '\'')
    arr = cursor.fetchall()
    for row in arr:
        name = row[0] + ' ' + row[1]
    title = name + "'s Patient Information"
    popupmsg(msg, title)


def acc():
    cursor.execute('SELECT * FROM PATIENT_ACCOUNT WHERE PATIENT_ID =\'' + pid +
                   '\'')
    myresult = cursor.fetchall()
    msg = ''
    for row in myresult:
        msg = "Patient ID: " + row[0] + "\nAccount Number: " + row[
            1] + "\nInsurance: " + row[2] + "\nAccount Password: " + row[3]
    cursor.execute('SELECT FNAME, LNAME FROM PATIENT WHERE PATIENT_ID =\'' +
                   pid + '\'')
    arr = cursor.fetchall()
    for row in arr:
        name = row[0] + ' ' + row[1]
    title = name + "'s Account Information"
    popupmsg(msg, title)


def appt():
    cursor.execute(
        'SELECT * FROM APPOINTMENTS WHERE ACCOUNT_NUM=(SELECT ACCOUNT_NUM FROM PATIENT_ACCOUNT WHERE PATIENT_ID =\''
        + pid + '\')')
    myresult = cursor.fetchall()
    msg = ''
    temp=[]
    temp1=''
    flag=False
    for row in myresult:
        if (flag):
            temp1='\nTest: '+row[0]+'\nDoctor ID: '+row[2]+ '\nReceptionist ID: '+row[3]+ '\nAppointment Date: '+str(row[4])
        else:
            msg = "Test: " + row[0] + "\nAccount Number: " + row[1] + "\nDoctor ID: " + row[2] + "\nReceptionist ID: " + row[3]+ '\nAppointment Date: '+str(row[4])
        flag=True
        temp.append(temp1)
    msg=msg+'\n'.join(temp)

    cursor.execute('SELECT FNAME, LNAME FROM PATIENT WHERE PATIENT_ID =\'' +
                   pid + '\'')
    arr = cursor.fetchall()
    for row in arr:
        name = row[0] + ' ' + row[1]
    title = name + "'s Appointments"
    popupmsg(msg, title)


def bill():
    cursor.execute(
        'SELECT * FROM BILL WHERE ACCOUNT_NUM=(SELECT ACCOUNT_NUM FROM PATIENT_ACCOUNT WHERE PATIENT_ID=\''
        + pid + '\')')
    myresult = cursor.fetchall()

    msg = ''
    for row in myresult:
        msg = "Account Number: " + row[0] + "\nCopay: $" + str(
            row[1]) + "\nAmount: $" + str(row[2]) + "\nDue Date: " + str(
                row[3])
    cursor.execute('SELECT FNAME, LNAME FROM PATIENT WHERE PATIENT_ID =\'' +
                   pid + '\'')
    arr = cursor.fetchall()
    for row in arr:
        name = row[0] + ' ' + row[1]
    title = name + "'s Bill"
    popupmsg(msg, title)


def rec():
    cursor.execute(
        'SELECT * FROM RECORD WHERE ACCOUNT_NUM=(SELECT ACCOUNT_NUM FROM PATIENT_ACCOUNT WHERE PATIENT_ID =\''
        + pid + '\')')
    myresult = cursor.fetchall()
    msg = ''
    temp=[]
    for row in myresult:
        temp1=row[1]
        temp.append(temp1)
        msg ="Account Number: " + row[0] + "\nRecords: "
    msg=msg+'\n'.join(temp)



    cursor.execute('SELECT FNAME, LNAME FROM PATIENT WHERE PATIENT_ID =\'' +
                   pid + '\'')
    arr = cursor.fetchall()
    for row in arr:
        name = row[0] + ' ' + row[1]
    title = name + "'s Record"
    popupmsg(msg, title)


Font = ("Verdana", 12)


def popupmsg(msg, title):
    popup = tk.Tk()
    popup.wm_title(title)
    label = tk.Label(popup, text=msg, font=Font)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


if __name__ == "__main__":
    app = frame_change()
    app.mainloop()

db.close()