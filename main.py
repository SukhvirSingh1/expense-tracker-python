import json
import tkinter as tk
from tkinter import messagebox,simpledialog

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
        
    def add_expenses(self,item,amount):
        self.expenses.append({
            "item":item,
            "amount":amount
        })
        self.save_expenses()
        print("Expense added!\n")
    
    def view_expenses(self):
        if not self.expenses:
            print("No expenses yet.\n")
            return
        
        print("\nYour Expenses")
        for i,e in enumerate(self.expenses,start=1):
            print(f"{i}:{e['item']} - {e['amount']}")
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
        
    tracker.add_expenses(item,amount)
    messagebox.showinfo("Success","Expense added!")
    
def view_expenses_gui():
    if not tracker.expenses:
        messagebox.showinfo("Expenses","No Expenses yet")
        return
        
    text = "Your Expenses\n\n"
    for i,e in enumerate(tracker.expenses,start=1):
        text += (f"{i}.{e['item']} - {e['amount']}\n")  
    messagebox.showinfo("Your Expenses",f"Total expense:{text}")
    
def sum_expenses_gui():
    if not tracker.expenses:
        messagebox.showinfo("Expenses","No Expenses yet")
        return
    total = sum(e["amount"] for e in tracker.expenses)
    messagebox.showinfo("Sum of your expenses",total)
    
    

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

root.mainloop()


