import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
import os

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
FILE_NAME = "save.json"


class CurrencyMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Монитор валют")
        self.root.geometry("600x500")

        self.currencies = {}
        self.groups = {}

        self.load_currencies()
        self.load_groups()

        self.create_widgets()

    def load_currencies(self):
        try:
            response = requests.get(URL)
            data = response.json()
            self.currencies = data["Valute"]
        except:
            messagebox.showerror("Ошибка", "Не удалось загрузить курсы валют")

    def load_groups(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                self.groups = json.load(f)
        else:
            self.groups = {}

    def save_groups(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.groups, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)

        tab_all = ttk.Frame(tab_control)
        tab_control.add(tab_all, text="Все валюты")

        self.all_list = tk.Listbox(tab_all, width=70, height=20)
        self.all_list.pack(padx=10, pady=10)

        for code in self.currencies:
            c = self.currencies[code]
            self.all_list.insert(tk.END, f"{code}: {c['Nominal']} {c['Name']} = {c['Value']} руб.")

        tk.Button(tab_all, text="Найти валюту", command=self.find_currency).pack(pady=5)

        tab_groups = ttk.Frame(tab_control)
        tab_control.add(tab_groups, text="Группы")

        self.groups_list = tk.Listbox(tab_groups, width=70, height=15)
        self.groups_list.pack(padx=10, pady=10)
        self.groups_list.bind('<<ListboxSelect>>', self.show_group_currencies)

        btn_frame = tk.Frame(tab_groups)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Создать группу", command=self.create_group).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Добавить валюту", command=self.add_currency).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить валюту", command=self.remove_currency).pack(side=tk.LEFT, padx=5)

        self.currency_list = tk.Listbox(tab_groups, width=70, height=8)
        self.currency_list.pack(padx=10, pady=10)

        tab_control.pack(expand=1, fill="both")

        self.update_groups_list()

    def find_currency(self):
        code = simpledialog.askstring("Поиск", "Введите код валюты (например USD):")
        if code:
            code = code.upper()
            if code in self.currencies:
                c = self.currencies[code]
                messagebox.showinfo("Валюта", f"{code}: {c['Nominal']} {c['Name']} = {c['Value']} руб.")
            else:
                messagebox.showerror("Ошибка", "Валюта не найдена")

    def create_group(self):
        name = simpledialog.askstring("Создать группу", "Введите название группы:")
        if name and name not in self.groups:
            self.groups[name] = []
            self.save_groups()
            self.update_groups_list()
            messagebox.showinfo("Успех", f"Группа '{name}' создана")
        elif name in self.groups:
            messagebox.showerror("Ошибка", "Такая группа уже есть")

    def add_currency(self):
        selection = self.groups_list.curselection()
        if not selection:
            messagebox.showerror("Ошибка", "Выберите группу")
            return

        group = self.groups_list.get(selection[0])

        code = simpledialog.askstring("Добавить валюту", "Введите код валюты (например USD):")
        if code:
            code = code.upper()
            if code in self.currencies:
                if code not in self.groups[group]:
                    self.groups[group].append(code)
                    self.save_groups()
                    self.show_group_currencies()
                    messagebox.showinfo("Успех", f"{code} добавлен в группу")
                else:
                    messagebox.showerror("Ошибка", "Такая валюта уже есть в группе")
            else:
                messagebox.showerror("Ошибка", "Валюта не найдена")

    def remove_currency(self):
        selection = self.groups_list.curselection()
        if not selection:
            messagebox.showerror("Ошибка", "Выберите группу")
            return

        group = self.groups_list.get(selection[0])

        curr_selection = self.currency_list.curselection()
        if not curr_selection:
            messagebox.showerror("Ошибка", "Выберите валюту из списка")
            return

        code = self.currency_list.get(curr_selection[0]).split(":")[0]

        if code in self.groups[group]:
            self.groups[group].remove(code)
            self.save_groups()
            self.show_group_currencies()
            messagebox.showinfo("Успех", f"{code} удален из группы")

    def update_groups_list(self):
        self.groups_list.delete(0, tk.END)
        for group in self.groups:
            self.groups_list.insert(tk.END, group)

    def show_group_currencies(self, event=None):
        self.currency_list.delete(0, tk.END)

        selection = self.groups_list.curselection()
        if selection:
            group = self.groups_list.get(selection[0])
            for code in self.groups[group]:
                if code in self.currencies:
                    c = self.currencies[code]
                    self.currency_list.insert(tk.END, f"{code}: {c['Value']} руб.")
                else:
                    self.currency_list.insert(tk.END, f"{code}: нет данных")


root = tk.Tk()
app = CurrencyMonitor(root)
root.mainloop()