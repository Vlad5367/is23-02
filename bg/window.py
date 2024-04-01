from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

root = Tk()
root.title("Авторизация")
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2
h = h // 2
w = w - 480
h = h - 270
root.geometry(f'500x540+{w}+{h}')
root.resizable(width=False, height=False)

root.configure(bg="#27241f")



def show_new_window(title):
    global poi
    new_window = Toplevel(root)
    new_window.title(title)
    new_window.geometry(f"500x540+{w}+{h}")
    new_window.configure(bg="#27241f")

    label1 = Label(new_window, text="Логин", font=("Times New Roman", 16), fg="#D7C8C8", bg="#27241f")
    label1.place(relx=0.28, rely=0.13, anchor=CENTER)

    entry6 = Entry(new_window, font=("Times New Roman", 20), bd=0, bg="#3E3D3D", fg="white", insertbackground="#4d4c48")
    entry6.place(relx=0.5, rely=0.2, anchor=CENTER)

    label2 = Label(new_window, text="Пароль", font=("Times New Roman", 16), fg="#D7C8C8", bg="#27241f")
    label2.place(relx=0.285, rely=0.28, anchor=CENTER)

    entry66 = Entry(new_window, font=("Times New Roman", 20), bd=0, bg="#3E3D3D", fg="white", insertbackground="#4d4c48")
    entry66.place(relx=0.5, rely=0.35, anchor=CENTER)

    def save_credentials():
        new_login = entry6.get()
        new_password = entry66.get()

        if new_login and new_password:
            with open("Polzovatel.txt", "a") as file:
                file.write(f"Логин: {new_login}\n")
                file.write(f"Пароль: {new_password}\n")

            entry6.delete(0, END)
            entry66.delete(0, END)

    def commands():
        save_credentials()
        new_window.destroy()


    poi = Image.open('zar.png')
    poi = poi.resize((136, 32))
    poi = ImageTk.PhotoImage(poi)
    my_butt = Button(new_window, image=poi, command=commands, bd=0, bg="#27241f", activebackground="#27241f")
    my_butt.place(relx=0.5, rely=0.45, anchor=CENTER)

    label12 = Label(new_window, text="Регистрация", font=("Times New Roman", 30), fg="white", bg="#27241f")
    label12.place(relx=0.43, rely=0.06, anchor=CENTER)

def regis():
    show_new_window("Регистрация")


photo_image = Image.open('vp.png')
photo_image = photo_image.resize((300, 40))
photo = ImageTk.PhotoImage(photo_image)

label = Label(root, image=photo, bd=0, bg="#27241f")
label.place(relx=0.50, rely=0.25, anchor=CENTER)

photo_image1 = Image.open('vp.png')
photo_image1 = photo_image1.resize((300, 40))
photo1 = ImageTk.PhotoImage(photo_image1)

label = Label(root, image=photo1, bd=0, bg="#27241f")
label.place(relx=0.50, rely=0.41, anchor=CENTER)


def check_credentials():
    entered_login = entry.get()
    entered_password = entry3.get()

    with open("Polzovatel.txt", "r") as file:
        lines = file.readlines()
        credentials = [line.strip() for line in lines]

    for i in range(0, len(credentials), 2):
        login = credentials[i].split(": ")[1]
        password = credentials[i + 1].split(": ")[1]

        if entered_login == login and entered_password == password:
            messagebox.showinfo("Success", "Вход выполнен успешно!")
            return

    messagebox.showerror("Error", "Ошибка ввода логина или пароля")



po_image = Image.open('Vhod.png')
po_image = po_image.resize((100, 30))
po = ImageTk.PhotoImage(po_image)
my_button = Button(root, image=po, command=check_credentials, bd=0, bg="#27241f", activebackground="#27241f")
my_button.place(relx=0.5, rely=0.55, anchor=CENTER)

poisk_image = Image.open('Regis.png') 
poisk_image = poisk_image.resize((100, 30))
poisk = ImageTk.PhotoImage(poisk_image)
my_button1 = Button(root, image=poisk, command=regis, bd=0, bg="#27241f", activebackground="#27241f")
my_button1.place(relx=0.5, rely=0.61, anchor=CENTER)

entry = Entry(root, font=("Times New Roman", 18), bd=0, bg="#3E3D3D", fg="white", insertbackground="#4d4c48")
entry.insert(0, "")
entry.place(relx=0.46, rely=0.250, anchor=CENTER)

entry3 = Entry(root, show="*", font=("Times New Roman", 18), bd=0, bg="#3E3D3D", fg="white", insertbackground="#4d4c48")
entry3.insert(0, "")
entry3.place(relx=0.46, rely=0.410, anchor=CENTER)

label = Label(root, text="Авторизация", font=("Times New Roman", 30), fg="white", bg="#27241f")
label.place(relx=0.43, rely=0.06, anchor=CENTER)

label1 = Label(root, text="Логин", font=("Times New Roman", 14), fg="#D7C8C8", bg="#27241f")
label1.place(relx=0.26, rely=0.182, anchor=CENTER)

label1 = Label(root, text="Пароль", font=("Times New Roman", 14), fg="#D7C8C8", bg="#27241f")
label1.place(relx=0.2677, rely=0.34, anchor=CENTER)

root.mainloop()
