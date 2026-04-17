
from tkinter import *
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime


class order:
    def __init__(self, root, current_user_email):
        self.root = root
        self.current_user_email = current_user_email

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Place Order")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")

        self.perfume_var = StringVar()
        self.customer_var = StringVar()
        self.quantity_var = StringVar()
        self.price_var = StringVar()
        self.total_var = StringVar()

        Label(self.root, text="Order Management", font=("Calibri", 22, "bold"), bg="white").place(x=560, y=30)
        Label(self.root, text=f"Login User: {self.current_user_email}", font=("Calibri", 12, "bold"), bg="white").place(x=40, y=35)

        form = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        form.place(x=120, y=110, width=520, height=440)

        Label(form, text="Select Perfume", font=("Calibri", 14, "bold"), bg="white").place(x=30, y=35)
        self.perfume_combo = ttk.Combobox(form, textvariable=self.perfume_var, state="readonly", font=("Calibri", 12))
        self.perfume_combo.place(x=220, y=35, width=230, height=30)
        self.perfume_combo.bind("<<ComboboxSelected>>", self.fill_price)

        Label(form, text="Customer Name", font=("Calibri", 14, "bold"), bg="white").place(x=30, y=95)
        Entry(form, textvariable=self.customer_var, font=("Calibri", 12)).place(x=220, y=95, width=230, height=30)

        Label(form, text="Available Price", font=("Calibri", 14, "bold"), bg="white").place(x=30, y=155)
        Entry(form, textvariable=self.price_var, font=("Calibri", 12), state="readonly").place(x=220, y=155, width=230, height=30)

        Label(form, text="Order Quantity", font=("Calibri", 14, "bold"), bg="white").place(x=30, y=215)
        qty_entry = Entry(form, textvariable=self.quantity_var, font=("Calibri", 12))
        qty_entry.place(x=220, y=215, width=230, height=30)
        qty_entry.bind("<KeyRelease>", self.calculate_total)

        Label(form, text="Total Amount", font=("Calibri", 14, "bold"), bg="white").place(x=30, y=275)
        Entry(form, textvariable=self.total_var, font=("Calibri", 12), state="readonly").place(x=220, y=275, width=230, height=30)

        Button(form, text="Save Order", font=("Calibri", 14, "bold"), bg="green", fg="white", command=self.save_order).place(x=70, y=345, width=150, height=40)
        Button(form, text="Clear", font=("Calibri", 14, "bold"), bg="orange", command=self.clear).place(x=250, y=345, width=100, height=40)
        Button(form, text="Back Home", font=("Calibri", 14, "bold"), bg="#444444", fg="white", command=self.go_home).place(x=370, y=345, width=110, height=40)

        table_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        table_frame.place(x=700, y=110, width=560, height=540)

        Label(table_frame, text="Recent Orders", font=("Calibri", 16, "bold"), bg="white").pack(pady=10)

        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.order_table = ttk.Treeview(
            table_frame,
            columns=("id", "perfume", "customer", "quantity", "total", "date"),
            yscrollcommand=scroll_y.set
        )
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.order_table.yview)

        for col, txt, width in [
            ("id", "ID", 60),
            ("perfume", "Perfume", 130),
            ("customer", "Customer", 120),
            ("quantity", "Qty", 70),
            ("total", "Total", 90),
            ("date", "Date", 120),
        ]:
            self.order_table.heading(col, text=txt)
            self.order_table.column(col, width=width)

        self.order_table["show"] = "headings"
        self.order_table.pack(fill=BOTH, expand=1, padx=10, pady=10)

        self.perfume_map = {}
        self.load_perfumes()
        self.load_orders()

    def connect_db(self):
        return pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="nafasdatabase"
        )

    def load_perfumes(self):
        try:
            con = self.connect_db()
            cur = con.cursor()
            cur.execute("SELECT id, name, price, quantity FROM perfume ORDER BY name ASC")
            rows = cur.fetchall()
            con.close()

            perfume_names = []
            self.perfume_map.clear()

            for row in rows:
                pid, name, price, quantity = row
                label = f"{name} (Stock: {quantity})"
                perfume_names.append(label)
                self.perfume_map[label] = {
                    "id": pid,
                    "name": name,
                    "price": float(price),
                    "quantity": int(quantity)
                }

            self.perfume_combo["values"] = perfume_names
            if perfume_names:
                self.perfume_combo.current(0)
                self.fill_price()

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def fill_price(self, event=None):
        selected = self.perfume_var.get()
        if selected in self.perfume_map:
            self.price_var.set(str(self.perfume_map[selected]["price"]))
            self.calculate_total()

    def calculate_total(self, event=None):
        try:
            price = float(self.price_var.get() or 0)
            qty = int(self.quantity_var.get() or 0)
            self.total_var.set(f"{price * qty:.2f}")
        except ValueError:
            self.total_var.set("0.00")

    def save_order(self):
        if self.perfume_var.get().strip() == "" or self.customer_var.get().strip() == "" or self.quantity_var.get().strip() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        if self.perfume_var.get() not in self.perfume_map:
            messagebox.showerror("Error", "Please select a valid perfume", parent=self.root)
            return

        try:
            order_qty = int(self.quantity_var.get())
            if order_qty <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0", parent=self.root)
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number", parent=self.root)
            return

        perfume_data = self.perfume_map[self.perfume_var.get()]
        if order_qty > perfume_data["quantity"]:
            messagebox.showerror("Error", "Not enough stock available", parent=self.root)
            return

        try:
            con = self.connect_db()
            cur = con.cursor()

            total_amount = perfume_data["price"] * order_qty

            cur.execute(
                """
                INSERT INTO orders (perfume_id, perfume_name, customer_name, unit_price, quantity, total_amount, sold_by, order_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    perfume_data["id"],
                    perfume_data["name"],
                    self.customer_var.get().strip(),
                    perfume_data["price"],
                    order_qty,
                    total_amount,
                    self.current_user_email,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )

            cur.execute(
                "UPDATE perfume SET quantity = quantity - %s WHERE id = %s",
                (order_qty, perfume_data["id"])
            )

            con.commit()
            con.close()

            messagebox.showinfo("Success", "Order saved successfully", parent=self.root)
            self.clear()
            self.load_perfumes()
            self.load_orders()

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def load_orders(self):
        try:
            con = self.connect_db()
            cur = con.cursor()
            cur.execute(
                """
                SELECT id, perfume_name, customer_name, quantity, total_amount, DATE(order_date)
                FROM orders
                ORDER BY id DESC
                LIMIT 50
                """
            )
            rows = cur.fetchall()
            con.close()

            self.order_table.delete(*self.order_table.get_children())
            for row in rows:
                self.order_table.insert("", END, values=row)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def clear(self):
        self.customer_var.set("")
        self.quantity_var.set("")
        self.total_var.set("")
        self.fill_price()

    def go_home(self):
        from Home import home
        home(self.root, self.current_user_email)


if __name__ == "__main__":
    root = Tk()
    obj = order(root, "demo@example.com")
    root.mainloop()
