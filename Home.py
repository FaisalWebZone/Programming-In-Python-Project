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
        self.root.geometry("1200x700+0+0")

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

        # == Add Perfume Button ==
        btn_add_perfume = Button(
            self.root,
            text="Add Perfume",
            font=("Calibri", 16, "bold"),
            bg="white",
            fg="black",
            command=self.add_perfume
        )
        btn_add_perfume.place(x=880, y=20, width=150, height=50)

        # == Invoice Button ==
        btn_invoice = Button(
            self.root,
            text="Invoice",
            font=("Calibri", 16, "bold"),
            bg="white",
            fg="black",
            command=self.invoice
        )
        btn_invoice.place(x=1045, y=20, width=100, height=50)

        # == Logout Button ==
        btn_logout = Button(
            self.root,
            text="Logout",
            font=("Calibri", 16, "bold"),
            bg="black",
            fg="white",
            command=self.logout
        )
        btn_logout.place(x=1160, y=20, width=100, height=50)

        # == Welcome Label ==
        Label(
            self.root,
            text=f"Welcome {self.current_user_email}",
            font=("Calibri", 22, "bold"),
            bg="white"
        ).place(x=50, y=120)

    def go_home(self):
        from Home import home
        home(self.root, self.current_user_email)

    def invoice(self):
        from Invoice import invoice
        invoice(self.root, self.current_user_email)

    def add_perfume(self):
        from AddPerfume import addperfume
        addperfume(self.root, self.current_user_email)   # email pass hocche

    def logout(self):
        from Login import login
        login(self.root)


if __name__ == "__main__":
    root = Tk()
    obj = home(root)
    root.mainloop()