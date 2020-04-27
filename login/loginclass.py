from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox


#might hava to download pillow with pip to load the immages 
#to get in
# username : admin password : password
class login_system:
    def __init__(self, root):
        self.root = root
        self.root.title("User Login")
        self.root.geometry("500x450")
        #self.root.geometry("250x150+300+300")

        #Images ......... //
        self.bg_icon = ImageTk.PhotoImage(file="images/dd.jpg")
        #self.logo_icon = PhotoImage(file="images/bg.png")

        logo = Image.open("images/user.jpg")
        logo = logo.resize((200, 200), Image.ANTIALIAS)
        self.logoimg = ImageTk.PhotoImage(logo)

        logo = Image.open("images/man-user.jpg")
        logo = logo.resize((20, 20), Image.ANTIALIAS)
        self.userimg = ImageTk.PhotoImage(logo)

        logo = Image.open("images/lock.jpg")
        logo = logo.resize((20, 20), Image.ANTIALIAS)
        self.userpass = ImageTk.PhotoImage(logo)

        #self.user_icon = PhotoImage(file="images/user.jpg")
        #self.pass_icon = PhotoImage(file="images/lock.png")
        #******* Variables username & pass

        self.username = StringVar()
        self.password = StringVar()

        bg_image = Label(self.root, image=self.bg_icon).pack()

        title = Label(self.root,
                      text="Login in to your Account",
                      font=("times new roman", 25, "bold"),
                      bg="light blue",
                      fg="Black",
                      bd=5,
                      relief=GROOVE)

        title.place(x=0, y=0, relwidth=1)

        Login_frame = Frame(self.root, bg="White")
        Login_frame.place(x=80, y=80)

        logo = Label(Login_frame, image=self.logoimg, bd=0).grid(
            row=0,
            columnspan=2,
            pady=15,
        )

        lbuser = Label(Login_frame,
                       text="Username",
                       image=self.userimg,
                       compound=LEFT,
                       font=("times new roman", 20, "bold"),
                       bg="white").grid(row=1, column=0, padx=20, pady=10)

        txtuser = Entry(Login_frame,
                        bd=5,
                        textvariable=self.username,
                        relief=GROOVE,
                        font=("", 15)).grid(row=1, column=1, padx=20)

        lbpass = Label(Login_frame,
                       text="Password",
                       image=self.userpass,
                       compound=LEFT,
                       font=("times new roman", 20, "bold"),
                       bg="white").grid(row=2, column=0, padx=20, pady=10)
        passuser = Entry(Login_frame,
                         bd=5,
                         textvariable=self.password,
                         relief=GROOVE,
                         font=("", 15)).grid(row=2, column=1, padx=20)

        login_btn = Button(Login_frame,
                           text="Login",
                           width=15,
                           command=self.login,
                           font=("times new roman", 14, "bold"),
                           bg="light green",
                           fg="light green").grid(row=3, column=1, pady=10)

    def login(self):
        if self.username.get() == "" or self.password == "":
            messagebox.showerror(
                "Error",
                "Invalid info can't leave Username or Password field blank")

        elif self.username.get() == "admin" and self.password.get(
        ) == "password":
            messagebox.showinfo("Suscessful", "Welcome....")
            #I think  lamda async function goes here instead of welcome message

        else:
            messagebox.showerror("Error", "Invalid Username or Password")


root = Tk()
obj = login_system(root)
root.mainloop()
