import json
import tkinter as tk
from tkinter import messagebox,simpledialog
from datetime import date


expenses = []

class ExpenseTracker:
    def __init__(self,filename='expense.json'):
        self.filename = filename
        self.expenses = self.load_expenses()
        
    # LOADING SYSTEM
      
    def load_expenses(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return[]
    
    def save_expenses(self):
        with open(self.filename,"w") as f:
            json.dump(self.expenses,f,indent=4)
            
    # FUNCTIONS
        
    def add_expenses(self,item,amount,category,date):
        self.expenses.append({
            "item":item,
            "amount":amount,
            "category":category,
            "date":date
        })
        self.save_expenses()
        print("Expense added!\n")
    
    def view_expenses(self):
        if not self.expenses:
            print("No expenses yet.\n")
            return
        
        print("\nYour Expenses")
        for i,e in enumerate(self.expenses,start=1):
            print(f"{i}:{e['item']} - {e['amount']} - {e['category']} - {e['date']}")
        print()
        
    def total_expenses(self):
        total = sum(e["amount"] for e in self.expenses)
        print(f"\nTotal spent:{total}\n")
        
        # MENU (GUI)
        
tracker = ExpenseTracker()

# GUI FUNCTIONS

def add_expense_gui():
    item = simpledialog.askstring("Add expense","What did you spend on:")
    if not item:
        return

    try:
        amount = float(simpledialog.askstring("Amount","Enter your amount:"))
        
    except(ValueError,TypeError):
        messagebox.showerror("Error","Invalid input")
        return
        
    category = simpledialog.askstring("Category","In which category:")
    if not category:
            return
        
        
    today_date = str(date.today())
        
    tracker.add_expenses(item,amount,category,today_date)
    messagebox.showinfo("Success","Expense added!")
    
def view_expenses_gui():
    if not tracker.expenses:
        messagebox.showinfo("Expenses","No Expenses yet")
        return
        
    text = "Your Expenses\n\n"
    for i,e in enumerate(tracker.expenses,start=1):
        text += (f"{i}.{e['item']} - {e['amount']} - {e['category']} - {e['date']}\n")  
    messagebox.showinfo("Your Expenses",text)
    
def sum_expenses_gui():
    if not tracker.expenses:
        messagebox.showinfo("Expenses","No Expenses yet")
        return
    total = sum(e["amount"] for e in tracker.expenses)
    messagebox.showinfo("Sum of your expenses",total)
    
def dlt_expenses_gui():
    if not tracker.expenses:
        messagebox.showinfo("Expenses","No expenses yet!")
        return
    try:
        index = int(simpledialog.askstring("Epxense","What you want to delete:"))
        if index < 1 or index > len(tracker.expenses):
            messagebox.showinfo("Error","Expense NOt Found")
            return
    except(ValueError,TypeError):
        return
            
    deleted = tracker.expenses.pop(index-1)
    
    tracker.save_expenses()
    messagebox.showinfo("Expenses",f"Your expense:{deleted['item']} - {deleted['amount']}")
    
def monthly_filter_gui():
    if not tracker.expenses:
        messagebox.showinfo("Monthly Filter","No Expenses yet")
        return
    month = simpledialog.askstring("Monthly Filter","Enter (YYYY - MM):")
    if not month:
        return
    filtered = []
    for e in tracker.expenses:
        if e["date"].startswith(month):
            filtered.append(e)
        
    if not  filtered:
        messagebox.showinfo("Monthly Filter","No Expense Found")
        return
    
    text = f"Filtered for this {month}\n\n"    
    for i,e in enumerate(filtered,start=1):
        text += (f"{i}.{e['item']} - {e['amount']} - {e['category']} - {e['date']}")
        
    messagebox.showinfo("Monthly Filter",text)    
    
    
    

root = tk.Tk()
root.title("Sukha's Expense Tracker")
root.geometry("350x350")

label = tk.Label(root,text="Expense tracker",font=("Arial",16))
label.pack(pady=20)

btn_add=tk.Button(root,text ="Add your expense",width=25,command=add_expense_gui)
btn_add.pack(pady=5)

btn_view=tk.Button(root,text="View Expenses",width=25,command=view_expenses_gui)
btn_view.pack(pady=5)

btn_sum=tk.Button(root,text="Sum Expenses",width=25,command=sum_expenses_gui)
btn_sum.pack(pady=5)

btn_dlt=tk.Button(root,text="Delete Expense",width=25,command=dlt_expenses_gui)
btn_dlt.pack(pady=5)

btn_monthly_filter=tk.Button(root,text="Monthly Filter",width=25,command=monthly_filter_gui)
btn_monthly_filter.pack(pady=5)

root.mainloop()


