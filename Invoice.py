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

        # ===== Variables =====
        self.search_by = StringVar()
        self.search_txt = StringVar()

        title = Label(self.root, text="Invoice...", font=("Calibri", 20, "bold"), bg="white")
        title.place(x=650, y=40)

        session_user = Label(
            self.root,
            text=f"Login User: {self.current_user_email}",
            font=("Calibri", 12, "bold"),
            bg="white",
            fg="black"
        )
        session_user.place(x=500, y=80)

        Perfume = Label(self.root, text="Perfume", font=("Calibri", 16, "bold"), bg="white")
        Perfume.place(x=120, y=150)

        self.txt_Perfume = Entry(self.root, font=("Calibri", 15), bg="white", bd="1", relief="solid")
        self.txt_Perfume.place(x=120, y=180, width=380, height=40)

        Price = Label(self.root, text="Price", font=("Calibri", 16, "bold"), bg="white")
        Price.place(x=120, y=240)

        self.txt_Price = Entry(self.root, font=("Calibri", 15), bg="white", bd="1", relief="solid")
        self.txt_Price.place(x=120, y=270, width=380, height=40)

        Customer_Name = Label(self.root, text="Customer Name", font=("Calibri", 16, "bold"), bg="white")
        Customer_Name.place(x=120, y=330)

        self.txt_Customer_Name = Entry(self.root, font=("Calibri", 15), bg="white", bd="1", relief="solid")
        self.txt_Customer_Name.place(x=120, y=360, width=380, height=40)

        btn_save = Button(
            self.root,
            text="Save Invoice",
            font=("Calibri", 16, "bold"),
            bg="#000000",
            fg="white",
            command=self.add_invoice
        )
        btn_save.place(x=120, y=430, width=180, height=45)

        btn_back = Button(
            self.root,
            text="Back Home",
            font=("Calibri", 16, "bold"),
            bg="white",
            fg="black",
            command=self.go_home
        )
        btn_back.place(x=320, y=430, width=180, height=45)

        # ===== Search Frame =====
        search_frame = Frame(self.root, bg="white", bd=1, relief=SOLID)
        search_frame.place(x=580, y=150, width=700, height=60)

        Label(search_frame, text="Search By", font=("Calibri", 12, "bold"), bg="white").grid(row=0, column=0, padx=8, pady=10)

        combo_search = ttk.Combobox(
            search_frame,
            textvariable=self.search_by,
            state="readonly",
            font=("Calibri", 12),
            width=12
        )
        combo_search["values"] = ("perfume", "customer_name", "email")
        combo_search.grid(row=0, column=1, padx=8)
        combo_search.current(0)

        Entry(
            search_frame,
            textvariable=self.search_txt,
            font=("Calibri", 12),
            bd=1,
            relief=SOLID
        ).grid(row=0, column=2, padx=8)

        Button(
            search_frame,
            text="Search",
            font=("Calibri", 12, "bold"),
            bg="orange",
            command=self.search_data
        ).grid(row=0, column=3, padx=8)

        Button(
            search_frame,
            text="Show All",
            font=("Calibri", 12, "bold"),
            bg="black",
            fg="white",
            command=self.fetch_data
        ).grid(row=0, column=4, padx=8)

        # ===== Table =====
        table_frame = Frame(self.root, bd=2, relief=RIDGE)
        table_frame.place(x=580, y=240, width=700, height=350)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.invoice_table = ttk.Treeview(
            table_frame,
            columns=("invoice_id", "perfume", "price", "customer_name", "email"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.invoice_table.xview)
        scroll_y.config(command=self.invoice_table.yview)

        self.invoice_table.heading("invoice_id", text="Invoice ID")
        self.invoice_table.heading("perfume", text="Perfume")
        self.invoice_table.heading("price", text="Price")
        self.invoice_table.heading("customer_name", text="Customer Name")
        self.invoice_table.heading("email", text="Email")

        self.invoice_table["show"] = "headings"

        self.invoice_table.column("invoice_id", width=100)
        self.invoice_table.column("perfume", width=150)
        self.invoice_table.column("price", width=100)
        self.invoice_table.column("customer_name", width=150)
        self.invoice_table.column("email", width=180)

        self.invoice_table.pack(fill=BOTH, expand=1)
        self.invoice_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    def connect_db(self):
        return pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="nafasdatabase"
        )

    def clear(self):
        self.txt_Perfume.delete(0, END)
        self.txt_Price.delete(0, END)
        self.txt_Customer_Name.delete(0, END)

    def add_invoice(self):
        if self.txt_Perfume.get() == "" or self.txt_Price.get() == "" or self.txt_Customer_Name.get() == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root)
        else:
            con = None
            try:
                con = self.connect_db()
                cur = con.cursor()

                perfume_name = self.txt_Perfume.get().strip()
                customer_name = self.txt_Customer_Name.get().strip()
                price = float(self.txt_Price.get())

                cur.execute(
                    "SELECT id, quantity FROM perfume WHERE name=%s",
                    (perfume_name,)
                )
                perfume_row = cur.fetchone()

                if perfume_row is None:
                    messagebox.showerror("Error", "Perfume not found in perfume table", parent=self.root)
                    return

                perfume_id = perfume_row[0]
                available_qty = int(perfume_row[1])

                sold_qty = 1

                if available_qty < sold_qty:
                    messagebox.showerror("Error", "Stock not available", parent=self.root)
                    return

                cur.execute(
                    "INSERT INTO invoice (perfume, price, customer_name, email) VALUES (%s, %s, %s, %s)",
                    (
                        perfume_name,
                        price,
                        customer_name,
                        self.current_user_email
                    )
                )

                cur.execute(
                    """
                    INSERT INTO orders
                    (perfume_id, perfume_name, customer_name, unit_price, quantity, total_amount, sold_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        perfume_id,
                        perfume_name,
                        customer_name,
                        price,
                        sold_qty,
                        price * sold_qty,
                        self.current_user_email
                    )
                )

                cur.execute(
                    "UPDATE perfume SET quantity = quantity - %s WHERE id = %s",
                    (sold_qty, perfume_id)
                )

                con.commit()

                messagebox.showinfo("Success", "Invoice Added Successfully", parent=self.root)
                self.clear()
                self.fetch_data()

            except Exception as es:
                if con:
                    con.rollback()
                messagebox.showerror("Error", f"Error due to : {str(es)}", parent=self.root)

            finally:
                if con:
                    con.close()

    def fetch_data(self):
        try:
            con = self.connect_db()
            cur = con.cursor()
            cur.execute("SELECT invoice_id, perfume, price, customer_name, email FROM invoice")
            rows = cur.fetchall()
            con.close()

            self.invoice_table.delete(*self.invoice_table.get_children())
            for row in rows:
                self.invoice_table.insert("", END, values=row)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to : {str(es)}", parent=self.root)

    def search_data(self):
        if self.search_by.get() == "" or self.search_txt.get() == "":
            messagebox.showerror("Error", "Please select search type and enter keyword", parent=self.root)
            return

        try:
            con = self.connect_db()
            cur = con.cursor()

            query = f"SELECT invoice_id, perfume, price, customer_name, email FROM invoice WHERE {self.search_by.get()} LIKE %s"
            cur.execute(query, ('%' + self.search_txt.get() + '%',))
            rows = cur.fetchall()
            con.close()

            self.invoice_table.delete(*self.invoice_table.get_children())

            if len(rows) == 0:
                messagebox.showinfo("No Result", "No record found", parent=self.root)
            else:
                for row in rows:
                    self.invoice_table.insert("", END, values=row)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to : {str(es)}", parent=self.root)

    def get_cursor(self, event):
        row = self.invoice_table.focus()
        content = self.invoice_table.item(row)
        data = content["values"]

        if data:
            self.txt_Perfume.delete(0, END)
            self.txt_Price.delete(0, END)
            self.txt_Customer_Name.delete(0, END)

            self.txt_Perfume.insert(0, data[1])
            self.txt_Price.insert(0, data[2])
            self.txt_Customer_Name.insert(0, data[3])

    def go_home(self):
        from Home import home
        home(self.root, self.current_user_email)