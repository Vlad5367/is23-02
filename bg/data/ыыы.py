import json
import os
import sys

import customtkinter as ctk
from tkinter import simpledialog
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from collections import Counter

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "budget_data.json")


class BudgetTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Трекер бюджета")
        self.geometry(f"1020x850+{-8}+{-5}")
        self.load_data()
        self.configure(bg="#6ADO75")
        self.right_frame = ctk.CTkFrame(self,width=980, height=900, fg_color="#83C350")
        self.right_frame.pack(side="right", fill="y")
        self.plot_expenses()
        self.income_button = ctk.CTkButton(self, text="Доходы", width=420, height=60, fg_color="#439900", font=("roboto", 40),
                                           command=self.add_income_window)
        self.income_button.pack(side="top", anchor="w", padx=20, pady=15)
        self.expense_button = ctk.CTkButton(self, text="Расходы", width=420, height=60, font=("roboto", 40),
                                            command=self.add_expense_window, fg_color="#439900")
        self.expense_button.pack(side="top", anchor="w", padx=20, pady=15)
        self.add_goal_button = ctk.CTkButton(self, text="Добавить цель", width=420, height=60, font=("roboto", 40),
                                             command=self.add_goal_window, fg_color="#439900")
        self.add_goal_button.pack(side="top", anchor="w", padx=20, pady=15)
        self.save_for_goal_button = ctk.CTkButton(self, text="Отложить на цель", width=420, height=60,
                                                  font=("roboto", 40), command=self.save_for_goal_window, fg_color="#439900")
        self.save_for_goal_button.pack(side="top", anchor="w", padx=20, pady=15)
        self.view_goals_button = ctk.CTkButton(self, text="Просмотреть цели", width=420, height=60, font=("roboto", 40),
                                               command=self.view_goals_window, fg_color="#439900")
        self.view_goals_button.pack(side="top", anchor="w", padx=20, pady=15)
        self.view_expenses_button = ctk.CTkButton(self, text="Посмотреть расходы", width=420, height=60,
                                                  font=("roboto", 40), command=self.view_expenses_window, fg_color="#439900")
        self.view_expenses_button.pack(side="top", anchor="w", padx=20, pady=15)
        self.view_incomes_button = ctk.CTkButton(self, text="Просмотреть доходы", width=400, height=60,
                                                 font=("roboto", 40), command=self.view_incomes_window, fg_color="#439900")
        self.view_incomes_button.pack(side="top", anchor="w", padx=20, pady=15)
        self.restart_button = ctk.CTkButton(self, text="Обновить графики", width=420, height=60, font=("roboto", 40), command=self.restart_program, fg_color="#439900")
        self.restart_button.pack(side="top", anchor="w", padx=20, pady=5)
        self.result_label = ctk.CTkLabel(self, text="Общий бюджет: 0", font=("roboto", 20))
        self.result_label.pack(side="top", anchor="w", padx=160, pady=15)
        self.theme_switch = ctk.CTkSwitch(self, text="Смена темы", font=("roboto", 20), command=self.change_mode)
        self.theme_switch.pack(side="top", anchor="w", padx=150, pady=15)
    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
    def plot_incomes(self):
        income_categories = [income_data["category"] for income_data in self.incomes]
        income_category_counts = Counter(income_categories)
        plt.figure(figsize=(5, 5))
        plt.pie(income_category_counts.values(), labels=income_category_counts.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Доходы по категориям')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('incomes_pie_chart.png')
        plt.close()
        incomes_image = Image.open('incomes_pie_chart.png')
        incomes_image = incomes_image.resize((400, 400))
        incomes_image = ImageTk.PhotoImage(incomes_image)
        self.incomes_plot_label = ctk.CTkLabel(self.right_frame, text=" ", image=incomes_image)
        self.incomes_plot_label.image = incomes_image
        self.incomes_plot_label.pack(side="top", padx=20, pady=15)

    def plot_expenses(self):
        category_counts = Counter(self.expenses)
        plt.figure(figsize=(5, 5))
        plt.pie(category_counts.values(), labels=category_counts.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Расходы по категориям')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('expenses_pie_chart.png')
        plt.close()
        expenses_image = Image.open('expenses_pie_chart.png')
        expenses_image = expenses_image.resize((400, 400))
        expenses_image = ImageTk.PhotoImage(expenses_image)
        self.expenses_plot_label = ctk.CTkLabel(self.right_frame, text=" ", image=expenses_image)
        self.expenses_plot_label.image = expenses_image
        self.expenses_plot_label.pack(side="top", padx=20, pady=15)
        self.plot_incomes()

    def change_mode(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def load_data(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                self.total_budget = data.get("total_budget", 0)
                self.goals = data.get("goals", [])
                self.expenses = data.get("expenses", {})
                self.incomes = data.get("incomes", [])
        else:
            self.total_budget = 0
            self.goals = []
            self.expenses = {"Продукты": 0, "Транспорт": 0, "Жилье": 0, "Развлечения": 0, "Здоровье": 0, "Прочее": 0}

    def save_data(self):
        data = {
            "total_budget": self.total_budget,
            "goals": self.goals,
            "expenses": self.expenses,
            "incomes": self.incomes
        }
        with open(DATA_FILE, "w") as file:
            json.dump(data, file)

    def view_incomes_window(self):
        view_incomes_window = ctk.CTk()
        view_incomes_window.title("Просмотр доходов")
        tree = ttk.Treeview(view_incomes_window, columns=("Category", "Amount"))
        tree.heading("#0", text="ID")
        tree.heading("Category", text="Категория")
        tree.heading("Amount", text="Сумма")
        for i, income_data in enumerate(self.incomes):
            category = income_data["category"]
            amount = income_data["amount"]
            tree.insert("", "end", text=str(i + 1), values=(category, amount))
        tree.pack(expand=True, fill="both")
        view_incomes_window.mainloop()

    def add_income_window(self):
        income_window = ctk.CTk()
        income_window.title("Добавить доход")
        category_label = ctk.CTkLabel(income_window, text="Выберите категорию дохода:")
        category_label.grid(row=0, column=0, padx=10, pady=5)
        categories = ["Зарплата", "Инвестиции", "Диведенты","Прочее"]
        category_combobox = ttk.Combobox(income_window, values=categories)
        category_combobox.grid(row=0, column=1, padx=10, pady=5)
        amount_label = ctk.CTkLabel(income_window, text="Введите сумму дохода:")
        amount_label.grid(row=1, column=0, padx=10, pady=5)
        amount_entry = ctk.CTkEntry(income_window)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)

        def add_income():
            category = category_combobox.get()
            amount = amount_entry.get()
            try:
                amount = float(amount)
                self.total_budget += amount
                self.incomes.append({"category": category, "amount": amount})
                self.result_label.configure(text=f"Общий бюджет: {self.total_budget}")
                self.save_data()
                income_window.destroy()
            except ValueError:
                ctk.CTkMessagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение для суммы дохода.")

        add_button = ctk.CTkButton(income_window, text="Добавить", command=add_income)
        add_button.grid(row=2, columnspan=2, padx=10, pady=10)
        income_window.mainloop()

    def add_income(self):
        income = simpledialog.askfloat("Доходы", "Введите сумму дохода:")
        if income is not None:
            self.total_budget += income
            self.incomes.append({"category": "Прочее", "amount": income})
            self.result_label.configure(text=f"Общий бюджет: {self.total_budget}")
            self.save_data()

    def add_income(self):
        income = simpledialog.askfloat("Доходы", "Введите сумму дохода:")
        if income is not None:
            self.total_budget += income
            self.result_label.configure(text=f"Общий бюджет: {self.total_budget}")
            self.save_data()

    def add_expense_window(self):
        expense_window = ctk.CTk()
        expense_window.title("Добавить расход")
        category_label = ctk.CTkLabel(expense_window, text="Выберите категорию расхода:")
        category_label.grid(row=0, column=0, padx=10, pady=5)
        categories = list(self.expenses.keys())
        category_combobox = ttk.Combobox(expense_window, values=categories)
        category_combobox.grid(row=0, column=1, padx=10, pady=5)
        amount_label = ctk.CTkLabel(expense_window, text="Введите сумму расхода:")
        amount_label.grid(row=1, column=0, padx=10, pady=5)
        amount_entry = ctk.CTkEntry(expense_window)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)

        def add_expense():
            category = category_combobox.get()
            amount = amount_entry.get()
            try:
                amount = float(amount)
                if amount <= self.total_budget:
                    self.total_budget -= amount
                    self.expenses[category] += amount
                    self.result_label.configure(text=f"Общий бюджет: {self.total_budget}")
                    self.save_data()
                    expense_window.destroy()
                else:
                    ctk.CTkMessagebox.showerror("Ошибка", "Сумма расхода не может превышать общий бюджет.")
            except ValueError:
                ctk.CTkMessagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение для суммы расхода.")
        add_button = ctk.CTkButton(expense_window, text="Добавить", command=add_expense)
        add_button.grid(row=2, columnspan=2, padx=10, pady=10)
        expense_window.mainloop()
    def add_goal_window(self):
        goal_window = ctk.CTk()
        goal_window.title("Добавить цель")
        name_label = ctk.CTkLabel(goal_window, text="Название цели:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        name_entry = ctk.CTkEntry(goal_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        cost_label = ctk.CTkLabel(goal_window, text="Стоимость цели:")
        cost_label.grid(row=1, column=0, padx=10, pady=5)
        cost_entry = ctk.CTkEntry(goal_window)
        cost_entry.grid(row=1, column=1, padx=10, pady=5)

        def add_goal():
            name = name_entry.get()
            cost = cost_entry.get()
            try:
                cost = float(cost)
                goal = {"name": name, "cost": cost, "saved": 0}
                self.goals.append(goal)
                self.save_data()
                goal_window.destroy()
            except ValueError:
                ctk.CTkMessagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение для стоимости цели.")
        add_button = ctk.CTkButton(goal_window, text="Добавить", command=add_goal)
        add_button.grid(row=2, columnspan=2, padx=10, pady=10)
        goal_window.mainloop()
    def save_for_goal_window(self):
        save_for_goal_window = ctk.CTk()
        save_for_goal_window.title("Отложить на цель")
        goal_label = ctk.CTkLabel(save_for_goal_window, text="Выберите цель:")
        goal_label.grid(row=0, column=0, padx=10, pady=5)
        goals_names = [goal["name"] for goal in self.goals]
        goal_combobox = ttk.Combobox(save_for_goal_window, values=goals_names)
        goal_combobox.grid(row=0, column=1, padx=10, pady=5)
        amount_label = ctk.CTkLabel(save_for_goal_window, text="Введите сумму для отложения:")
        amount_label.grid(row=1, column=0, padx=10, pady=5)
        amount_entry = ctk.CTkEntry(save_for_goal_window)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)
        def save_for_goal():
            goal_name = goal_combobox.get()
            amount = amount_entry.get()
            try:
                amount = float(amount)
                for goal in self.goals:
                    if goal["name"] == goal_name:
                        if amount <= self.total_budget:
                            goal["saved"] += amount
                            self.total_budget -= amount
                            self.result_label.configure(text=f"Общий бюджет: {self.total_budget}")
                            self.save_data()
                            ctk.CTkMessagebox.showinfo("Успех", f"Сумма {amount} успешно отложена на цель '{goal_name}'.")
                            save_for_goal_window.destroy()
                            return
                        else:
                            ctk.CTkMessagebox.showerror("Ошибка", "Сумма для отложения превышает общий бюджет.")
                            return
                ctk.CTkMessagebox.showerror("Ошибка", f"Цель '{goal_name}' не найдена.")
            except ValueError:
                ctk.CTkMessagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение для суммы.")
        save_button = ctk.CTkButton(save_for_goal_window, text="Отложить", command=save_for_goal)
        save_button.grid(row=2, columnspan=2, padx=10, pady=10)
        save_for_goal_window.mainloop()
    def view_goals_window(self):
        view_goals_window = ctk.CTk()
        view_goals_window.title("Просмотр целей")
        tree = ttk.Treeview(view_goals_window, columns=("Name", "Cost", "Saved", "Left to Save"))
        tree.heading("#0", text="ID")
        tree.heading("Name", text="Название")
        tree.heading("Cost", text="Стоимость")
        tree.heading("Saved", text="Отложено")
        tree.heading("Left to Save", text="Осталось отложить")
        for i, goal in enumerate(self.goals):
            name = goal["name"]
            cost = goal["cost"]
            saved = goal["saved"]
            left_to_save = max(cost - saved, 0)
            tree.insert("", "end", text=str(i+1), values=(name, cost, saved, left_to_save))
        tree.pack(expand=True, fill="both")
        view_goals_window.mainloop()
    def view_expenses_window(self):
        view_expenses_window = ctk.CTk()
        view_expenses_window.title("Просмотр расходов по категориям")
        tree = ttk.Treeview(view_expenses_window, columns=("Category", "Amount"))
        tree.heading("#0", text="ID")
        tree.heading("Category", text="Категория")
        tree.heading("Amount", text="Сумма")
        for i, (category, amount) in enumerate(self.expenses.items()):
            tree.insert("", "end", text=str(i+1), values=(category, amount))
        tree.pack(expand=True, fill="both")
        view_expenses_window.mainloop()
if __name__ == "__main__":
    app = BudgetTrackerApp()
    app.mainloop()