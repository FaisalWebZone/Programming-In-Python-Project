
from tkinter import *
from tkinter import ttk, messagebox
import pymysql


class perfumeinfo:
    def __init__(self, root, current_user_email):
        self.root = root
        self.current_user_email = current_user_email

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Perfume Information")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")

        self.search_by = StringVar(value="name")
        self.search_txt = StringVar()

        Label(
            self.root,
            text="Perfume Information",
            font=("Calibri", 22, "bold"),
            bg="white"
        ).place(x=560, y=30)

        Label(
            self.root,
            text=f"Login User: {self.current_user_email}",
            font=("Calibri", 12, "bold"),
            bg="white"
        ).place(x=40, y=35)

        search_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        search_frame.place(x=70, y=100, width=1220, height=80)

        Label(search_frame, text="Search By", font=("Calibri", 14, "bold"), bg="white").place(x=20, y=22)

        combo_search = ttk.Combobox(
            search_frame,
            textvariable=self.search_by,
            state="readonly",
            font=("Calibri", 12),
            width=12
        )
        combo_search["values"] = ("name", "brand", "id")
        combo_search.place(x=120, y=22)
        combo_search.current(0)

        Entry(
            search_frame,
            textvariable=self.search_txt,
            font=("Calibri", 13),
            bd=1,
            relief=SOLID
        ).place(x=280, y=22, width=280, height=30)

        Button(
            search_frame,
            text="Search",
            font=("Calibri", 13, "bold"),
            bg="orange",
            command=self.search_data
        ).place(x=590, y=20, width=110, height=35)

        Button(
            search_frame,
            text="Show All",
            font=("Calibri", 13, "bold"),
            bg="black",
            fg="white",
            command=self.fetch_data
        ).place(x=720, y=20, width=110, height=35)

        Button(
            search_frame,
            text="Back Home",
            font=("Calibri", 13, "bold"),
            bg="#444444",
            fg="white",
            command=self.go_home
        ).place(x=1050, y=20, width=130, height=35)

        table_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=70, y=220, width=1220, height=460)

        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.perfume_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "price", "brand", "quantity", "stock_value"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=self.perfume_table.yview)
        scroll_x.config(command=self.perfume_table.xview)

        for col, txt, width in [
            ("id", "ID", 80),
            ("name", "Name", 220),
            ("price", "Price", 150),
            ("brand", "Brand", 180),
            ("quantity", "Quantity", 140),
            ("stock_value", "Stock Value", 180),
        ]:
            self.perfume_table.heading(col, text=txt)
            self.perfume_table.column(col, width=width)

        self.perfume_table["show"] = "headings"
        self.perfume_table.pack(fill=BOTH, expand=1)

        self.fetch_data()

    def connect_db(self):
        return pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="nafasdatabase"
        )

    def fetch_data(self):
        try:
            con = self.connect_db()
            cur = con.cursor()
            cur.execute(
                """
                SELECT id, name, price, brand, quantity, (price * quantity) AS stock_value
                FROM perfume
                ORDER BY id DESC
                """
            )
            rows = cur.fetchall()
            con.close()

            self.perfume_table.delete(*self.perfume_table.get_children())
            for row in rows:
                self.perfume_table.insert("", END, values=row)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def search_data(self):
        if self.search_txt.get().strip() == "":
            messagebox.showerror("Error", "Please type something to search", parent=self.root)
            return

        try:
            con = self.connect_db()
            cur = con.cursor()

            field = self.search_by.get()
            if field == "id":
                cur.execute(
                    """
                    SELECT id, name, price, brand, quantity, (price * quantity) AS stock_value
                    FROM perfume
                    WHERE CAST(id AS CHAR) LIKE %s
                    ORDER BY id DESC
                    """,
                    ("%" + self.search_txt.get().strip() + "%",)
                )
            else:
                cur.execute(
                    f"""
                    SELECT id, name, price, brand, quantity, (price * quantity) AS stock_value
                    FROM perfume
                    WHERE {field} LIKE %s
                    ORDER BY id DESC
                    """,
                    ("%" + self.search_txt.get().strip() + "%",)
                )

            rows = cur.fetchall()
            con.close()

            self.perfume_table.delete(*self.perfume_table.get_children())
            for row in rows:
                self.perfume_table.insert("", END, values=row)

            if not rows:
                messagebox.showinfo("No Result", "No perfume found", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def go_home(self):
        from Home import home
        home(self.root, self.current_user_email)


if __name__ == "__main__":
    root = Tk()
    obj = perfumeinfo(root, "demo@example.com")
    root.mainloop()
