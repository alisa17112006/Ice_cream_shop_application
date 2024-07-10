from tkinter import *
from tkinter import ttk, simpledialog
from datetime import date
import sqlite3


def get_cursor():
    connect = sqlite3.connect('ice_cream.db')
    return connect, connect.cursor()


def all_products():
    text_widget.delete('1.0', END)
    connect, cursor = get_cursor()
    cursor.execute('SELECT name_ice, price FROM ice_cream')
    rows = cursor.fetchall()
    for row in rows:
        text_widget.insert(END, f"Название: {row[0]}, Цена: {row[1]}\n")
    cursor.close()
    connect.close()


def order_icecream():
    text_widget.delete('1.0', END)
    connect, cursor = get_cursor()
    try:
        cursor.execute('SELECT name_ice FROM Ice_cream')
        icecream_names = [row[0] for row in cursor.fetchall()]
        text_widget.insert(END,"Доступные названия мороженного:\n")
        for name in icecream_names:
            text_widget.insert(END, f"{name}\n")

        chosen_icecream = simpledialog.askstring("Заказ мороженного", "Введите название мороженного")
        if chosen_icecream not in icecream_names:
            text_widget.insert(END, 'Такого мороженного нет.\n')
            return

        try:
            quantity = int(simpledialog.askstring("Количество порций", "Введите количество порций"))
        except ValueError:
            text_widget.insert(END, "Количество порций должно быть числом.\n")
            return

        date_today = date.today().isoformat()
        confirm = simpledialog.askstring("Подтверждение заказа",
                                         f"Подтвердите заказ {quantity} порций '{chosen_icecream}' на дату {date_today} (да/нет)")
        if confirm.lower() != 'да':
            text_widget.insert(END, "Заказ отменён.\n")
            return

        cursor.execute('INSERT INTO Orders (name_ice, kolvo, data) VALUES (?, ?, ?)',
                       (chosen_icecream, quantity, date_today))
        connect.commit()
        text_widget.delete('1.0', END)
        text_widget.insert(END, "Заказ успешно добавлен в базу данных.\n")
    finally:
        cursor.close()
        connect.close()


def search_name():
    text_widget.delete('1.0', END)
    connect, cursor = get_cursor()
    name = simpledialog.askstring("Поиск по названию", "Введите название для поиска")
    cursor.execute('SELECT * FROM Ice_cream WHERE name_ice = ?', (name,))
    rows = cursor.fetchall()
    if not rows:
        text_widget.insert(END, "Такого мороженного нет.\n")
    else:
        for row in rows:
            text_widget.insert(END, "Такое мороженное есть!\n")
    cursor.close()
    connect.close()


def sort_price():
    text_widget.delete('1.0', END)
    connect, cursor = get_cursor()
    cursor.execute('SELECT * FROM Ice_cream ORDER BY price')
    for row in cursor.fetchall():
        text_widget.insert(END, f"Название: {row[1]}, Цена: {row[4]}\n")
    cursor.close()
    connect.close()


def viewing_orders():
    text_widget.delete('1.0', END)
    connect, cursor = get_cursor()
    cursor.execute('SELECT * FROM Orders')
    text_widget.insert(END, "| № |  Название  | Кол-во |   Дата  |\n")
    text_widget.insert(END, "-------------------------------------\n")
    for row in cursor.fetchall():
        text_widget.insert(END, "| ")
        for i in row:
            text_widget.insert(END, f"{i} | ")
        text_widget.insert(END, "\n")
    cursor.close()
    connect.close()


root = Tk()

style = ttk.Style()
style.configure('Red.TButton', foreground='red', font=('Monstreat', 10, 'bold'))
style.configure('Orange.TButton', foreground='orange', font=('Monstreat', 10, 'bold'))
style.configure('Yellow.TButton', foreground='yellow', font=('Monstreat', 10, 'bold'))
style.configure('Green.TButton', foreground='green', font=('Monstreat', 10, 'bold'))
style.configure('Purple.TButton', foreground='purple', font=('Monstreat', 10, 'bold'))
style.configure('Pad.TText', padding=10)

root.title("Ice cream shop")
root.geometry("330x500")

icon = PhotoImage(file="ice-cream.png")
root.iconphoto(False, icon)

text_widget = Text(wrap='word', width=37, height=15)
text_widget.grid(row=8, column=0, columnspan=3, pady = 20)

label = Label(text="Menu:")
label.grid(row=1, column=0, columnspan=3)

all_ice = ttk.Button(text="   All products   ", command=all_products, style='Red.TButton')
all_ice.grid(row=2, column=0, columnspan=1)

ord_ice = ttk.Button(text="Order icecream", command=order_icecream, style='Orange.TButton')
ord_ice.grid(row=2, column=1, columnspan=1)

search = ttk.Button(text="  Search name  ", command=search_name, style='Yellow.TButton')
search.grid(row=2, column=2, columnspan=1)

sort = ttk.Button(text="  Sort by price  ", command=sort_price, style='Green.TButton')
sort.grid(row=3, column=0, columnspan=1)

view_orders = ttk.Button(text="Viewing orders", command=viewing_orders, style='Purple.TButton')
view_orders.grid(row=3, column=1, columnspan=1)

# Добавление изображений
image1 = PhotoImage(file="ice_one.png")  # Замените на путь к вашему изображению
image2 = PhotoImage(file="ice-cream-cone.png")  # Замените на путь к вашему изображению
image3 = PhotoImage(file="popsicle.png")  # Замените на путь к вашему изображению

image_label1 = Label(root, image=image1)
image_label1.grid(row=9, column=0, columnspan=1, pady=20)  # Отступ 10 пикселей

image_label2 = Label(root, image=image2)
image_label2.grid(row=9, column=1, columnspan=1, pady=20)  # Отступ 10 пикселей

image_label3 = Label(root, image=image3)
image_label3.grid(row=9, column=2, columnspan=1, pady=20)  # Отступ 10 пикселей

root.mainloop()
