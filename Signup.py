from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pymysql

class signup:
    def __init__(self,root):
        self.root=root
        self.root.title("Signup")
        self.root.geometry("1366x768+0+0")

        #==Bg Image==
        self.bg=ImageTk.PhotoImage(file="Images/PMS-01.jpg")
        bg=Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)

        #==Signup Frame==
        title=Label(self.root,text="Signup...",font=("Calibri",20,"bold"),bg="white").place(x=650,y=300)

        self.Email=Label(self.root,text="Email",font=("Calibri",16,"bold"),bg="white").place(x=500,y=350)
        self.txt_Email=Entry(self.root,font=("Calibri",15),bg="white",bd="1",relief="solid")
        self.txt_Email.place(x=500,y=380,width=380,height=40)

        Password=Label(self.root,text="Password",font=("Calibri",16,"bold"),bg="white").place(x=500,y=430)
        self.txt_Password=Entry(self.root,font=("Calibri",15),bg="white",bd="1",relief="solid")
        self.txt_Password.place(x=500,y=460,width=380,height=40)

        Confirm_Password=Label(self.root,text="Confirm Password",font=("Calibri",16,"bold"),bg="white").place(x=500,y=510)
        self.txt_Confirm_Password=Entry(self.root,font=("Calibri",15),bg="white",bd="1",relief="solid")
        self.txt_Confirm_Password.place(x=500,y=540,width=380,height=40)

        btn_signup = Button(self.root,text="Signup",font=("Calibri", 16, "bold"),bg="#000000",fg="white",command=self.register_data)            
        btn_signup.place(x=500, y=600, width=380, height=45)

        Login=Label(self.root,text="Already have an account?",font=("Calibri",12),bg="white").place(x=575,y=650)
        btn_login = Button(self.root,text="Login",font=("Calibri", 12, "bold"),bg="White",bd=0,fg="Black")            
        btn_login.place(x=745, y=652, width=40, height=20)


    def clear(self):
        self.txt_Email.delete(0,END)
        self.txt_Password.delete(0,END)
        self.txt_Confirm_Password.delete(0,END)

    def register_data(self):
        if self.txt_Email.get()=="" or self.txt_Password.get()=="" or self.txt_Confirm_Password.get()=="":
            messagebox.showerror("Error","All Fields Are Required",parent=self.root)
        elif self.txt_Password.get()!= self.txt_Confirm_Password.get():
            messagebox.showerror("Error","Password & Confirm Password should be same",parent=self.root)
        else:
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="NafasDatabase")
                cur=con.cursor()
                cur.execute("select*from user where email=%s",self.txt_Email.get())
                row=cur.fetchone()
                # print(row)
                if row!=None:
                    messagebox.showinfo("Error","User Already Exist,Please try with another email",parent=self.root)  
                else:                
                    cur.execute("insert into user (email,password)values(%s,%s)",
                            (self.txt_Email.get(),
                             self.txt_Password.get()        
                            ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Register Successful",parent=self.root)
                    self.clear()
            except Exception as es:
                messagebox.showerror("Error",f"error due to:{str(es)}",parent=self.root)
               
            # messagebox.showinfo("Success","Register Successful",parent=self.root)


root=Tk()
obj=signup(root)
root.mainloop()

