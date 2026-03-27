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

        
        Label(form_frame, text="Quantity", bg="white").grid(row=5, column=0, pady=5)
        Entry(form_frame, textvariable=self.quantity_var).grid(row=5, column=1)

        # -------- BUTTONS --------
        Button(form_frame, text="Add", bg="green", fg="white",
               command=self.add_data).grid(row=6, column=0, pady=10)

        Button(form_frame, text="Update", bg="blue", fg="white",
               command=self.update_data).grid(row=6, column=1)

        Button(form_frame, text="Delete", bg="red", fg="white",
               command=self.delete_data).grid(row=7, column=0)

        Button(form_frame, text="Clear",
               command=self.clear_fields).grid(row=7, column=1)

        # -------- TABLE FRAME --------
        table_frame = Frame(main_frame)
        table_frame.place(x=350, y=20, width=700, height=380)

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
        con = self.connect_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM perfume")
        rows = cur.fetchall()
        con.close()

        self.perfume_table.delete(*self.perfume_table.get_children())
        for row in rows:
            self.perfume_table.insert("", END, values=row)

    def add_data(self):
        if self.name_var.get() == "" or self.price_var.get() == "":
            messagebox.showerror("Error", "Name and Price required")
            return

        con = self.connect_db()
        cur = con.cursor()

        cur.execute("""
            INSERT INTO perfume (name, price, brand, quantity)
            VALUES (%s,%s,%s,%s)
        """, (
            self.name_var.get(),
            self.brand_var.get(),
            self.quantity_var.get(),
            self.price_var.get()
        ))

        con.commit()
        con.close()

        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Data Added")

    def update_data(self):
        if self.id_var.get() == "":
            messagebox.showerror("Error", "Select data first")
            return

        con = self.connect_db()
        cur = con.cursor()

        cur.execute("""
            UPDATE perfume 
            SET name=%s, price=%s, brand=%s, quantity=%s 
            WHERE perfume_id=%s
        """, (
            self.name_var.get(),
            self.price_var.get(),
            self.brand_var.get(),
            
            self.quantity_var.get(),
            self.id_var.get()
        ))

        con.commit()
        con.close()

        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Data Updated")

    def delete_data(self):
        if self.id_var.get() == "":
            messagebox.showerror("Error", "Select data first")
            return

        con = self.connect_db()
        cur = con.cursor()

        cur.execute("DELETE FROM perfume WHERE id=%s", (self.id_var.get(),))

        con.commit()
        con.close()

        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Data Deleted")

    def clear_fields(self):
        self.id_var.set("")
        self.name_var.set("")
        self.price_var.set("")
        self.brand_var.set("")
        
        self.quantity_var.set("")

    def get_cursor(self, event):
        row = self.perfume_table.focus()
        content = self.perfume_table.item(row)
        data = content["values"]

        if data:
            self.id_var.set(data[0])
            self.name_var.set(data[1])
            self.price_var.set(data[2])
            self.brand_var.set(data[3])
            
            self.quantity_var.set(data[5])


# -------- MAIN --------
if __name__ == "__main__":
    root = Tk()
    obj = addperfume(root)
    root.mainloop()