import tkinter as tk
from tkinter import messagebox
import connect
# import database   # your existing module


class DataFetcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Fetcher")
        self.root.geometry("700x700")
        self.root.configure(bg="#f3f4f6")
        # self.root.resizable(False, False)

        self.primary = "#2563eb"
        self.secondary = "#1e40af"
        self.card = "#ffffff"
        self.text = "#1f2937"
        self.border = "#d1d5db"

        self.create_ui()

    def create_ui(self):
        # Title
        tk.Label(
            self.root,
            text="Data Fetcher",
            font=("Segoe UI", 26, "bold"),
            bg="#f3f4f6",
            fg=self.text
        ).pack(pady=(30, 10))

        # Card Frame
        card = tk.Frame(
            self.root,
            bg=self.card,
            bd=1,
            relief=tk.SOLID,
            highlightbackground=self.border,
            highlightthickness=1
        )
        card.pack(padx=30, pady=10, fill=tk.X)

        inner = tk.Frame(card, bg=self.card)
        inner.pack(padx=25, pady=25, fill=tk.BOTH)

        # Password Label
        tk.Label(
            inner,
            text="Enter your Password",
            font=("Segoe UI", 11),
            bg=self.card,
            fg=self.text
        ).pack(anchor="w")

        # Password Entry
        self.password_entry = tk.Entry(
            inner,
            font=("Segoe UI", 12),
            show="●",
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.border,
            highlightcolor=self.primary
        )
        self.password_entry.pack(fill=tk.X, ipady=8, pady=(5, 20))

        # Table Label
        tk.Label(
            inner,
            text="Table Name",
            font=("Segoe UI", 11),
            bg=self.card,
            fg=self.text
        ).pack(anchor="w")

        # Table Entry
        self.table_entry = tk.Entry(
            inner,
            font=("Segoe UI", 12),
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.border,
            highlightcolor=self.primary
        )
        self.table_entry.pack(fill=tk.X, ipady=8, pady=(5, 20))

        # Connect Button
        self.connect_btn = tk.Button(
            inner,
            text="Connect",
            font=("Segoe UI", 12, "bold"),
            bg=self.primary,
            fg="white",
            relief=tk.FLAT,
            activebackground=self.secondary,
            activeforeground="white",
            command=self.connect_to_db,
            cursor="hand2"
        )
        self.connect_btn.pack(fill=tk.X, ipady=10)

        self.connect_btn.bind("<Enter>", lambda e: self.connect_btn.config(bg=self.secondary))
        self.connect_btn.bind("<Leave>", lambda e: self.connect_btn.config(bg=self.primary))

    def connect_to_db(self):
        password = self.password_entry.get().strip()
        table = self.table_entry.get().strip()

        if not password:
            messagebox.showerror("Error", "Password required")
            return
        if not table:
            messagebox.showerror("Error", "Table name required")
            return

        try:
            # No database name needed anymore


            messagebox.showinfo("Success", f"Connected to table '{table}' successfully!")

            self.password_entry.delete(0, tk.END)
            self.table_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))


# Main App
if __name__ == "__main__":
    root = tk.Tk()
    app = DataFetcher(root)
    root.mainloop()
