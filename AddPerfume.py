from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pymysql


class addperfume:
    def __init__(self, root, current_user_email):
        self.root = root
        self.root.title("Perfume Management System")
        self.root.geometry("1200x700+0+0")

        self.current_user_email = current_user_email

        for widget in self.root.winfo_children():
            widget.destroy()

        # == Search Variable ==
        self.search_by = StringVar()
        self.search_txt = StringVar()

        # -------- BACKGROUND IMAGE --------
        self.bg = ImageTk.PhotoImage(file="Images/PMS-02.jpg")
        bg = Label(self.root, image=self.bg)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        # -------- TOP IMAGE --------
        self.top_img = Image.open("Images/PMS-03.jpg")
        self.top_img = self.top_img.resize((1200, 150))
        self.top_img = ImageTk.PhotoImage(self.top_img)

        top_label = Label(self.root, image=self.top_img)
        top_label.place(x=0, y=0, width=1200, height=150)

        # -------- CURRENT USER SHOW --------
        Label(
            self.root,
            text=f"Current User: {self.current_user_email}",
            font=("Calibri", 16, "bold"),
            bg="white",
            fg="black"
        ).place(x=20, y=160)

        # -------- HOME BUTTON --------
        Button(
            self.root,
            text="Home",
            font=("Calibri", 14, "bold"),
            bg="black",
            fg="white",
            cursor="hand2",
            command=self.go_home
        ).place(x=1040, y=160, width=100, height=35)

        # -------- VARIABLES --------
        self.id_var = StringVar()
        self.name_var = StringVar()
        self.price_var = StringVar()
        self.brand_var = StringVar()
        self.quantity_var = StringVar()

        # -------- MAIN FRAME --------
        main_frame = Frame(self.root, bg="white")
        main_frame.place(x=50, y=210, width=1100, height=450)

        # -------- FORM FRAME --------
        form_frame = Frame(main_frame, bg="white")
        form_frame.place(x=20, y=20, width=300, height=380)

        Label(form_frame, text="Perfume ID", bg="white").grid(row=0, column=0, pady=5)
        Entry(form_frame, textvariable=self.id_var).grid(row=0, column=1)

        Label(form_frame, text="Name", bg="white").grid(row=1, column=0, pady=5)
        Entry(form_frame, textvariable=self.name_var).grid(row=1, column=1)

        Label(form_frame, text="Price", bg="white").grid(row=2, column=0, pady=5)
        Entry(form_frame, textvariable=self.price_var).grid(row=2, column=1)

        Label(form_frame, text="Brand", bg="white").grid(row=3, column=0, pady=5)
        Entry(form_frame, textvariable=self.brand_var).grid(row=3, column=1)

        Label(form_frame, text="Quantity", bg="white").grid(row=4, column=0, pady=5)
        Entry(form_frame, textvariable=self.quantity_var).grid(row=4, column=1)

        # -------- BUTTONS --------
        Button(form_frame, text="Add", bg="green", fg="white",
               command=self.add_data).grid(row=6, column=0, pady=10)

        Button(form_frame, text="Update", bg="blue", fg="white",
               command=self.update_data).grid(row=6, column=1)

        Button(form_frame, text="Delete", bg="red", fg="white",
               command=self.delete_data).grid(row=7, column=0)

        Button(form_frame, text="Clear",
               command=self.clear_fields).grid(row=7, column=1)

        # -------- SEARCH FRAME --------
        search_frame = Frame(main_frame, bg="white")
        search_frame.place(x=350, y=0, width=700, height=50)

        Label(search_frame, text="Search By", bg="white",
              font=("Calibri", 12, "bold")).grid(row=0, column=0, padx=5)

        combo_search = ttk.Combobox(
            search_frame,
            textvariable=self.search_by,
            state="readonly",
            width=10,
            font=("Calibri", 12)
        )
        combo_search["values"] = ("name", "brand")
        combo_search.grid(row=0, column=1, padx=5)
        combo_search.current(0)

        Entry(
            search_frame,
            textvariable=self.search_txt,
            width=25,
            font=("Calibri", 12)
        ).grid(row=0, column=2, padx=5)

        Button(
            search_frame,
            text="Search",
            bg="orange",
            fg="black",
            font=("Calibri", 12, "bold"),
            command=self.search_data
        ).grid(row=0, column=3, padx=5)

        Button(
            search_frame,
            text="Show All",
            font=("Calibri", 12, "bold"),
            command=self.fetch_data
        ).grid(row=0, column=4, padx=5)

        # -------- TABLE FRAME --------
        table_frame = Frame(main_frame)
        table_frame.place(x=350, y=60, width=700, height=340)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.perfume_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "price", "brand", "quantity"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.perfume_table.xview)
        scroll_y.config(command=self.perfume_table.yview)

        self.perfume_table.heading("id", text="ID")
        self.perfume_table.heading("name", text="Name")
        self.perfume_table.heading("price", text="Price")
        self.perfume_table.heading("brand", text="Brand")
        self.perfume_table.heading("quantity", text="Quantity")

        self.perfume_table["show"] = "headings"
        self.perfume_table.pack(fill=BOTH, expand=1)

        self.perfume_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    # -------- GO HOME --------
    def go_home(self):
        from Home import home
        home(self.root, self.current_user_email)

    # -------- DATABASE --------
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
            cur.execute("SELECT id, name, price, brand, quantity FROM perfume")
            rows = cur.fetchall()
            con.close()

            self.perfume_table.delete(*self.perfume_table.get_children())
            for row in rows:
                self.perfume_table.insert("", END, values=row)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def search_data(self):
        if self.search_by.get() == "" or self.search_txt.get() == "":
            messagebox.showerror("Error", "Please select search type and enter keyword", parent=self.root)
            return

        try:
            con = self.connect_db()
            cur = con.cursor()

            query = f"SELECT id, name, price, brand, quantity FROM perfume WHERE {self.search_by.get()} LIKE %s"
            cur.execute(query, ('%' + self.search_txt.get().strip() + '%',))

            rows = cur.fetchall()
            con.close()

            self.perfume_table.delete(*self.perfume_table.get_children())

            if len(rows) == 0:
                messagebox.showinfo("No Result", "No record found", parent=self.root)
            else:
                for row in rows:
                    self.perfume_table.insert("", END, values=row)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def add_data(self):
        if self.name_var.get() == "" or self.price_var.get() == "":
            messagebox.showerror("Error", "Name and Price required", parent=self.root)
            return

        try:
            price = float(self.price_var.get())
            quantity = int(self.quantity_var.get() or 0)

            con = self.connect_db()
            cur = con.cursor()

            cur.execute("""
                INSERT INTO perfume (name, price, brand, quantity)
                VALUES (%s, %s, %s, %s)
            """, (
                self.name_var.get().strip(),
                price,
                self.brand_var.get().strip(),
                quantity
            ))

            con.commit()
            con.close()

            self.fetch_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Data Added", parent=self.root)

        except ValueError:
            messagebox.showerror("Error", "Price must be number and Quantity must be integer", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def update_data(self):
        if self.id_var.get() == "":
            messagebox.showerror("Error", "Select data first", parent=self.root)
            return

        try:
            price = float(self.price_var.get())
            quantity = int(self.quantity_var.get() or 0)

            con = self.connect_db()
            cur = con.cursor()

            cur.execute("""
                UPDATE perfume
                SET name=%s, price=%s, brand=%s, quantity=%s
                WHERE id=%s
            """, (
                self.name_var.get().strip(),
                price,
                self.brand_var.get().strip(),
                quantity,
                self.id_var.get()
            ))

            con.commit()
            con.close()

            self.fetch_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Data Updated", parent=self.root)

        except ValueError:
            messagebox.showerror("Error", "Price must be number and Quantity must be integer", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def delete_data(self):
        if self.id_var.get() == "":
            messagebox.showerror("Error", "Select data first", parent=self.root)
            return

        try:
            con = self.connect_db()
            cur = con.cursor()

            cur.execute("DELETE FROM perfume WHERE id=%s", (self.id_var.get(),))

            con.commit()
            con.close()

            self.fetch_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Data Deleted", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

    def clear_fields(self):
        self.id_var.set("")
        self.name_var.set("")
        self.price_var.set("")
        self.brand_var.set("")
        self.quantity_var.set("")
        self.search_txt.set("")

    def get_cursor(self, event):
        row = self.perfume_table.focus()
        content = self.perfume_table.item(row)
        data = content["values"]

        if data:
            self.id_var.set(data[0])
            self.name_var.set(data[1])
            self.price_var.set(data[2])
            self.brand_var.set(data[3])
            self.quantity_var.set(data[4])


if __name__ == "__main__":
    root = Tk()
    obj = addperfume(root, "demo@example.com")
    root.mainloop()