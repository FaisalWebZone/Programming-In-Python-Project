
from tkinter import *
from tkinter import ttk, messagebox
import pymysql


class revenue:
    def __init__(self, root, current_user_email):
        self.root = root
        self.current_user_email = current_user_email

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Revenue")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")

        Label(self.root, text="Revenue Report", font=("Calibri", 22, "bold"), bg="white").place(x=580, y=25)
        Label(self.root, text=f"Login User: {self.current_user_email}", font=("Calibri", 12, "bold"), bg="white").place(x=40, y=30)

        Button(self.root, text="Refresh", font=("Calibri", 14, "bold"), bg="black", fg="white", command=self.load_data).place(x=1080, y=25, width=100, height=40)
        Button(self.root, text="Back Home", font=("Calibri", 14, "bold"), bg="#444444", fg="white", command=self.go_home).place(x=1190, y=25, width=120, height=40)

        self.total_orders_var = StringVar(value="0")
        self.total_items_var = StringVar(value="0")
        self.total_revenue_var = StringVar(value="0.00")
        self.avg_order_var = StringVar(value="0.00")

        self.card("Total Orders", self.total_orders_var, 70)
        self.card("Items Sold", self.total_items_var, 390)
        self.card("Total Revenue", self.total_revenue_var, 710)
        self.card("Average Order", self.avg_order_var, 1030)

        Label(self.root, text="Monthly Revenue Summary", font=("Calibri", 16, "bold"), bg="white").place(x=70, y=220)

        month_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        month_frame.place(x=70, y=260, width=500, height=390)

        month_scroll = Scrollbar(month_frame, orient=VERTICAL)
        self.month_table = ttk.Treeview(
            month_frame,
            columns=("month", "orders", "revenue"),
            yscrollcommand=month_scroll.set
        )
        month_scroll.pack(side=RIGHT, fill=Y)
        month_scroll.config(command=self.month_table.yview)

        self.month_table.heading("month", text="Month")
        self.month_table.heading("orders", text="Orders")
        self.month_table.heading("revenue", text="Revenue")
        self.month_table["show"] = "headings"
        self.month_table.column("month", width=180)
        self.month_table.column("orders", width=100)
        self.month_table.column("revenue", width=160)
        self.month_table.pack(fill=BOTH, expand=1)

        recent_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        recent_frame.place(x=620, y=220, width=670, height=430)

        Label(recent_frame, text="Recent Sales", font=("Calibri", 16, "bold"), bg="white").pack(pady=10)

        recent_scroll = Scrollbar(recent_frame, orient=VERTICAL)
        self.recent_table = ttk.Treeview(
            recent_frame,
            columns=("id", "perfume", "customer", "qty", "total", "date"),
            yscrollcommand=recent_scroll.set
        )
        recent_scroll.pack(side=RIGHT, fill=Y)
        recent_scroll.config(command=self.recent_table.yview)

        for col, txt, width in [
            ("id", "ID", 60),
            ("perfume", "Perfume", 150),
            ("customer", "Customer", 120),
            ("qty", "Qty", 60),
            ("total", "Total", 100),
            ("date", "Date", 120),
        ]:
            self.recent_table.heading(col, text=txt)
            self.recent_table.column(col, width=width)

        self.recent_table["show"] = "headings"
        self.recent_table.pack(fill=BOTH, expand=1, padx=10, pady=10)

        self.load_data()

    def card(self, title, variable, x):
        frame = Frame(self.root, bg="#f3f3f3", bd=2, relief=RIDGE)
        frame.place(x=x, y=90, width=250, height=90)
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

            cur.execute(
                "SELECT COUNT(*), COALESCE(SUM(quantity),0), COALESCE(SUM(total_amount),0), COALESCE(AVG(total_amount),0) FROM orders"
            )
            stats = cur.fetchone()

            self.total_orders_var.set(str(stats[0] or 0))
            self.total_items_var.set(str(stats[1] or 0))
            self.total_revenue_var.set(f"{float(stats[2] or 0):.2f}")
            self.avg_order_var.set(f"{float(stats[3] or 0):.2f}")

            cur.execute(
                """
                SELECT DATE_FORMAT(order_date, '%Y-%m') AS month_name,
                       COUNT(*) AS total_orders,
                       COALESCE(SUM(total_amount),0) AS total_revenue
                FROM orders
                GROUP BY DATE_FORMAT(order_date, '%Y-%m')
                ORDER BY month_name DESC
                """
            )
            month_rows = cur.fetchall()

            cur.execute(
                """
                SELECT id, perfume_name, customer_name, quantity, total_amount, DATE(order_date)
                FROM orders
                ORDER BY id DESC
                LIMIT 50
                """
            )
            recent_rows = cur.fetchall()
            con.close()

            self.month_table.delete(*self.month_table.get_children())
            for row in month_rows:
                self.month_table.insert("", END, values=row)

            self.recent_table.delete(*self.recent_table.get_children())
            for row in recent_rows:
                self.recent_table.insert("", END, values=row)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def go_home(self):
        from Home import home
        home(self.root, self.current_user_email)


if __name__ == "__main__":
    root = Tk()
    obj = revenue(root, "demo@example.com")
    root.mainloop()
