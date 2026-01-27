import tkinter as tk
from tkinter import messagebox,simpledialog
from datetime import date
import sqlite3




def init_db():
        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            amount REAL,
            category TEXT,
            date TEXT
        )
        """)
        conn.commit()
        conn.close()
class ExpenseTracker:        
            
    # def __init__(self,filename='expense.json'):
    #     self.filename = filename
    #     self.expenses = self.load_expenses()
        
    # LOADING SYSTEM
      
    def load_expenses(self):
        try:
            conn = sqlite3.connect("expenses.db")
            cur = conn.cursor()
            
            cur.execute("SELECT id, item, amount, category, date FROM expenses")
            row = cur.fetchall()
            conn.commit()
            return [
                {
                    "id": r[0],
                    "item": r[1],
                    "amount": r[2],
                    "category": r[3],
                    "date": r[4]
                }
                for r in row
            ]          
        except FileNotFoundError:
            return[]
    
    # def save_expenses(self):
    #     with open(self.filename,"w") as f:
    #         json.dump(self.expenses,f,indent=4)
            
    # FUNCTIONS
        
    def add_expenses(self,item,amount,category,date):
        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO expenses (item, amount, category, date) VALUES (?, ?, ?, ?)",
            (item, amount, category, date)
            )
        conn.commit()
        conn.close()
        
        print("Expense added!\n")
    
    def view_expenses(self):
        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        
        cur.execute("SELECT id, item, amount, category, date FROM expenses")
        rows = cur.fetchall()
        conn.close()
        return rows
    

    def total_expenses(self):
        expenses = tracker.view_expenses()
        total = sum(e[2] for e in expenses)
        print(f"\nTotal spent:{total}\n")
        
    def dlt_expenses(self,expense_id):
        conn=sqlite3.connect("expenses.db")
        cur=conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id=?",(expense_id))
        conn.commit()
        conn.close()
        
        # MENU (GUI)
        
tracker = ExpenseTracker()
init_db()

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
    expenses = tracker.view_expenses()
    if not expenses:
        messagebox.showinfo("Expenses","No Expenses yet")
        return
        
    text = "Your Expenses\n\n"
    for i,e in enumerate(expenses,start=1):
        text += (f"{i}.{e[1]} - {e[2]} - {e[3]} - {e[4]}\n")  
    messagebox.showinfo("Your Expenses",text)
    
def sum_expenses_gui():
    expenses = tracker.view_expenses()
    if not expenses:
        messagebox.showinfo("Expenses","No Expenses yet")
        return
    total = sum(e[2] for e in expenses)
    messagebox.showinfo("Sum of your expenses",total)
    
def dlt_expenses_gui():
    expense_id = simpledialog.askstring("DELETE MENU","What you want to delete")
    if not expense_id:
        return
    
    tracker.dlt_expenses(expense_id)    
    
    messagebox.showinfo("Expenses",f"Your expense with id {expense_id} deleted")
    
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


