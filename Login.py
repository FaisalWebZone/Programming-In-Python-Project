from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import pymysql
import hashlib


class login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1366x768+0+0")
        self.root.resizable(False, False)

        self.show_password = False

        self.login_page()

    def login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # == Bg Image ==
        self.bg = ImageTk.PhotoImage(file="Images/PMS-01.jpg")
        bg = Label(self.root, image=self.bg)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        # == Login Title ==
        title = Label(self.root, text="Login...", font=("Calibri", 20, "bold"), bg="white")
        title.place(x=650, y=300)

        self.Email = Label(self.root, text="Email", font=("Calibri", 16, "bold"), bg="white")
        self.Email.place(x=500, y=350)

        self.txt_Email = Entry(self.root, font=("Calibri", 15), bg="white", bd=1, relief="solid")
        self.txt_Email.place(x=500, y=380, width=380, height=40)

        Password = Label(self.root, text="Password", font=("Calibri", 16, "bold"), bg="white")
        Password.place(x=500, y=430)

        self.txt_Password = Entry(
            self.root,
            font=("Calibri", 15),
            bg="white",
            bd=1,
            relief="solid",
            show="*"
        )
        self.txt_Password.place(x=500, y=460, width=380, height=40)

        btn_eye = Button(
            self.root,
            text="👁",
            font=("Calibri", 12),
            bg="white",
            bd=0,
            command=self.toggle_password
        )
        btn_eye.place(x=840, y=463, width=36, height=36)

        btn_login = Button(
            self.root,
            text="Login",
            font=("Calibri", 16, "bold"),
            bg="#000000",
            fg="white",
            command=self.login_data
        )
        btn_login.place(x=500, y=600, width=380, height=45)

    def toggle_password(self):
        if self.show_password:
            self.txt_Password.config(show="*")
            self.show_password = False
        else:
            self.txt_Password.config(show="")
            self.show_password = True

    def hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def login_data(self):
        if self.txt_Email.get() == "" or self.txt_Password.get() == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root)
            return

        con = None
        try:
            con = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="NafasDatabase"
            )
            cur = con.cursor()

            hashed_password = self.hash_password(self.txt_Password.get())

            cur.execute(
                "SELECT email FROM `user` WHERE email=%s AND password=%s",   
                (self.txt_Email.get().strip(), hashed_password)
            )
            row = cur.fetchone()

            if row is not None:
                current_user_email = row[0]   

                messagebox.showinfo("Success", "Login Successful", parent=self.root)

                from Home import home  
                home(self.root, current_user_email)   

            else:
                messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

        finally:
            if con:
                con.close()


if __name__ == "__main__":
    root = Tk()
    obj = login(root)
    root.mainloop()