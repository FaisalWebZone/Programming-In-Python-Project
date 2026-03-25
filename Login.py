from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pymysql

class login:
    def __init__(self,root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1366x768+0+0")

        #==Bg Image==
        self.bg=ImageTk.PhotoImage(file="Images/PMS-01.jpg")
        bg=Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)

        #==Signup Frame==
        title=Label(self.root,text="Login...",font=("Calibri",20,"bold"),bg="white").place(x=650,y=300)

        self.Email=Label(self.root,text="Email",font=("Calibri",16,"bold"),bg="white").place(x=500,y=350)
        self.txt_Email=Entry(self.root,font=("Calibri",15),bg="white",bd="1",relief="solid")
        self.txt_Email.place(x=500,y=380,width=380,height=40)

        Password=Label(self.root,text="Password",font=("Calibri",16,"bold"),bg="white").place(x=500,y=430)
        self.txt_Password=Entry(self.root,font=("Calibri",15),bg="white",bd="1",relief="solid")
        self.txt_Password.place(x=500,y=460,width=380,height=40)

        btn_signup = Button(self.root,text="Login",font=("Calibri", 16, "bold"),bg="#000000",fg="white")            
        btn_signup.place(x=500, y=600, width=380, height=45)

        Login=Label(self.root,text="Create Acccount",font=("Calibri",12),bg="white").place(x=605,y=650)
        btn_login = Button(self.root,text="Signup",font=("Calibri", 12, "bold"),bg="White",bd=0,fg="Black")            
        btn_login.place(x=720, y=652, width=48, height=20)


root=Tk()
obj=login(root)
root.mainloop()