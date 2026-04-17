from tkinter import *
from PIL import Image, ImageTk


class home:
    def __init__(self, root, current_user_email):
        self.root = root
        self.current_user_email = current_user_email

        # clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.config(bg="white")
        self.root.title("Perfume Management System")
        self.root.geometry("1366x768+0+0")

        # == Bg Image ==
        self.bg = ImageTk.PhotoImage(file="Images/PMS-02.jpg")
        bg = Label(self.root, image=self.bg)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        # == Logo Button ==
        self.logo_img = ImageTk.PhotoImage(file="Images/PMS-03.jpg")
        btn_logo = Button(
            self.root,
            image=self.logo_img,
            command=self.go_home,
            bd=0,
            bg="white",
            cursor="hand2"
        )
        btn_logo.place(x=20, y=20, width=120, height=60)

        # == Welcome Label ==
        Label(
            self.root,
            text=f"Welcome {self.current_user_email}",
            font=("Calibri", 22, "bold"),
            bg="white"
        ).place(x=50, y=120)

        # == Existing Image Buttons ==
        self.allperfume_img = ImageTk.PhotoImage(file="Images/Allperfumes.jpg")
        btn_add_perfume = Button(
            self.root,
            image=self.allperfume_img,
            bd=0,
            bg="white",
            cursor="hand2",
            command=self.add_perfume
        )
        btn_add_perfume.place(x=160, y=200, width=200, height=240)

        self.invoice_img = ImageTk.PhotoImage(file="Images/Invoice.jpg")
        btn_invoice = Button(
            self.root,
            image=self.invoice_img,
            bd=0,
            bg="white",
            cursor="hand2",
            command=self.invoice
        )
        btn_invoice.place(x=410, y=200, width=200, height=240)

        # == New Buttons same style ==
        self.create_card_button("Perfume Info", 660, 200, self.perfume_info)
        self.create_card_button("Order", 910, 200, self.order_page)
        self.create_card_button("Revenue", 285, 480, self.revenue_page)
        self.create_card_button("Balance", 535, 480, self.balance_page)

        # == Logout Button ==
        btn_logout = Button(
            self.root,
            text="Logout",
            font=("Calibri", 16, "bold"),
            bg="black",
            fg="white",
            cursor="hand2",
            command=self.logout
        )
        btn_logout.place(x=1160, y=20, width=100, height=50)

    def create_card_button(self, text, x, y, command):
        # outer frame
        frame = Frame(self.root, bg="white", bd=1, relief="solid", cursor="hand2")
        frame.place(x=x, y=y, width=200, height=240)

        # top icon area
        icon_area = Frame(frame, bg="white")
        icon_area.place(x=0, y=0, width=200, height=180)

        # emoji/icon
        icon_map = {
            "Perfume Info": "🌸",
            "Order": "🛒",
            "Revenue": "💰",
            "Balance": "📦"
        }

        btn_top = Button(
            icon_area,
            text=icon_map.get(text, "•"),
            font=("Arial", 58),
            bg="white",
            bd=0,
            activebackground="white",
            cursor="hand2",
            command=command
        )
        btn_top.place(relx=0.5, rely=0.45, anchor=CENTER)

        # bottom black text bar
        btn_bottom = Button(
            frame,
            text=text,
            font=("Calibri", 18, "bold"),
            bg="black",
            fg="white",
            bd=0,
            activebackground="black",
            activeforeground="white",
            cursor="hand2",
            command=command
        )
        btn_bottom.place(x=0, y=180, width=200, height=60)

        # click anywhere on frame
        frame.bind("<Button-1>", lambda e: command())
        icon_area.bind("<Button-1>", lambda e: command())

    def go_home(self):
        from Home import home
        home(self.root, self.current_user_email)

    def invoice(self):
        from Invoice import invoice
        invoice(self.root, self.current_user_email)

    def add_perfume(self):
        from AddPerfume import addperfume
        addperfume(self.root, self.current_user_email)

    def perfume_info(self):
        from PerfumeInfo import perfumeinfo
        perfumeinfo(self.root, self.current_user_email)

    def order_page(self):
        from Order import order
        order(self.root, self.current_user_email)

    def revenue_page(self):
        from Revenue import revenue
        revenue(self.root, self.current_user_email)

    def balance_page(self):
        from Balance import balance
        balance(self.root, self.current_user_email)

    def logout(self):
        from Login import login
        login(self.root)


if __name__ == "__main__":
    root = Tk()
    obj = home(root, "demo@example.com")
    root.mainloop()