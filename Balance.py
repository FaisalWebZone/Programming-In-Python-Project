
from tkinter import *
from tkinter import ttk, messagebox
import pymysql


class balance:
    def __init__(self, root, current_user_email):
        self.root = root
        self.current_user_email = current_user_email

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Balance")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")

        Label(
            self.root,
            text="Balance / Stock Summary",
            font=("Calibri", 22, "bold"),
            bg="white"
        ).place(x=520, y=30)

        Label(
            self.root,
            text=f"Login User: {self.current_user_email}",
            font=("Calibri", 12, "bold"),
            bg="white"
        ).place(x=40, y=35)

        Button(
            self.root,
            text="Refresh",
            font=("Calibri", 14, "bold"),
            bg="black",
            fg="white",
            command=self.load_data
        ).place(x=1080, y=30, width=100, height=40)

        Button(
            self.root,
            text="Back Home",
            font=("Calibri", 14, "bold"),
            bg="#444444",
            fg="white",
            command=self.go_home
        ).place(x=1190, y=30, width=120, height=40)

        self.total_perfumes_var = StringVar(value="0")
        self.total_stock_var = StringVar(value="0")
        self.inventory_value_var = StringVar(value="0.00")
        self.low_stock_var = StringVar(value="0")

        self.summary_card("Total Perfumes", self.total_perfumes_var, 70)
        self.summary_card("Total Stock Qty", self.total_stock_var, 390)
        self.summary_card("Inventory Value", self.inventory_value_var, 710)
        self.summary_card("Low Stock Items", self.low_stock_var, 1030)

        Label(
            self.root,
            text="Low Stock Products (Quantity <= 5)",
            font=("Calibri", 16, "bold"),
            bg="white"
        ).place(x=70, y=230)

        table_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=70, y=270, width=1220, height=420)

        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.balance_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "brand", "price", "quantity", "stock_value"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=self.balance_table.yview)
        scroll_x.config(command=self.balance_table.xview)

        self.balance_table.heading("id", text="ID")
        self.balance_table.heading("name", text="Name")
        self.balance_table.heading("brand", text="Brand")
        self.balance_table.heading("price", text="Price")
        self.balance_table.heading("quantity", text="Quantity")
        self.balance_table.heading("stock_value", text="Stock Value")

        self.balance_table["show"] = "headings"
        self.balance_table.column("id", width=80)
        self.balance_table.column("name", width=220)
        self.balance_table.column("brand", width=180)
        self.balance_table.column("price", width=150)
        self.balance_table.column("quantity", width=150)
        self.balance_table.column("stock_value", width=180)
        self.balance_table.pack(fill=BOTH, expand=1)

        self.load_data()

    def summary_card(self, title, variable, x):
        frame = Frame(self.root, bg="#f3f3f3", bd=2, relief=RIDGE)
        frame.place(x=x, y=100, width=250, height=90)

        Label(frame, text=title, font=("Calibri", 15, "bold"), bg="#f3f3f3").pack(pady=(10, 5))
        Label(frame, textvariable=variable, font=("Calibri", 18, "bold"), bg="#f3f3f3", fg="#0b5d1e").pack()

    def connect_db(self):
        return pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="nafasdatabase"
        )

    def load_data(self):
        try:
            con = self.connect_db()
            cur = con.cursor()

            cur.execute("SELECT COUNT(*), COALESCE(SUM(quantity),0), COALESCE(SUM(price * quantity),0) FROM perfume")
            stats = cur.fetchone()

            total_perfumes = stats[0] or 0
            total_stock = stats[1] or 0
            inventory_value = float(stats[2] or 0)

            cur.execute("SELECT COUNT(*) FROM perfume WHERE quantity <= 5")
            low_stock_count = cur.fetchone()[0]

            cur.execute(
                """
                SELECT id, name, brand, price, quantity, (price * quantity) AS stock_value
                FROM perfume
                WHERE quantity <= 5
                ORDER BY quantity ASC, name ASC
                """
            )
            rows = cur.fetchall()
            con.close()

            self.total_perfumes_var.set(str(total_perfumes))
            self.total_stock_var.set(str(total_stock))
            self.inventory_value_var.set(f"{inventory_value:.2f}")
            self.low_stock_var.set(str(low_stock_count))

            self.balance_table.delete(*self.balance_table.get_children())
            for row in rows:
                self.balance_table.insert("", END, values=row)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def go_home(self):
        from Home import home
        home(self.root, self.current_user_email)


if __name__ == "__main__":
    root = Tk()
    obj = balance(root, "demo@example.com")
    root.mainloop()
