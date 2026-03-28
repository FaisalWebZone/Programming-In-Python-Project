from tkinter import *
from tkinter import ttk, messagebox
import pymysql


class invoice:
    def __init__(self, root, current_user_email):  
        self.root = root
        self.root.title("Invoice")
        self.root.geometry("1366x768+0+0")

        self.current_user_email = current_user_email   

        for widget in self.root.winfo_children():   
            widget.destroy()

        title = Label(self.root, text="Invoice...", font=("Calibri", 20, "bold"), bg="white")
        title.place(x=650, y=100)

        session_user = Label(   
            self.root,
            text=f"Login User: {self.current_user_email}",
            font=("Calibri", 12, "bold"),
            bg="white",
            fg="black"
        )
        session_user.place(x=500, y=140)

        Perfume = Label(self.root, text="Perfume", font=("Calibri", 16, "bold"), bg="white")
        Perfume.place(x=500, y=180)

        self.txt_Perfume = Entry(self.root, font=("Calibri", 15), bg="white", bd="1", relief="solid")
        self.txt_Perfume.place(x=500, y=210, width=380, height=40)

        Price = Label(self.root, text="Price", font=("Calibri", 16, "bold"), bg="white")
        Price.place(x=500, y=260)

        self.txt_Price = Entry(self.root, font=("Calibri", 15), bg="white", bd="1", relief="solid")
        self.txt_Price.place(x=500, y=290, width=380, height=40)

        Customer_Name = Label(self.root, text="Customer Name", font=("Calibri", 16, "bold"), bg="white")
        Customer_Name.place(x=500, y=340)

        self.txt_Customer_Name = Entry(self.root, font=("Calibri", 15), bg="white", bd="1", relief="solid")
        self.txt_Customer_Name.place(x=500, y=370, width=380, height=40)

        btn_save = Button(
            self.root,
            text="Save Invoice",
            font=("Calibri", 16, "bold"),
            bg="#000000",
            fg="white",
            command=self.add_invoice
        )
        btn_save.place(x=500, y=460, width=380, height=45)

        btn_back = Button(   # <<< CHANGED
            self.root,
            text="Back Home",
            font=("Calibri", 16, "bold"),
            bg="white",
            fg="black",
            command=self.go_home
        )
        btn_back.place(x=500, y=520, width=380, height=45)

    def clear(self):
        self.txt_Perfume.delete(0, END)
        self.txt_Price.delete(0, END)
        self.txt_Customer_Name.delete(0, END)

    def add_invoice(self):
        if self.txt_Perfume.get() == "" or self.txt_Price.get() == "" or self.txt_Customer_Name.get() == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root)
        else:
            try:
                con = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="NafasDatabase"
                )
                cur = con.cursor()

                cur.execute(
                    "insert into invoice (perfume,price,customer_name,email) values(%s,%s,%s,%s)",   
                    (
                        self.txt_Perfume.get(),
                        self.txt_Price.get(),
                        self.txt_Customer_Name.get(),
                        self.current_user_email   
                    )
                )

                con.commit()
                con.close()

                messagebox.showinfo("Success", "Invoice Added Successfully", parent=self.root)
                self.clear()

            except Exception as es:
                messagebox.showerror("Error", f"Error due to : {str(es)}", parent=self.root)

    def go_home(self):  
        from Home import home
        home(self.root, self.current_user_email)