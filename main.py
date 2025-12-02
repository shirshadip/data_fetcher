import tkinter as tk
from tkinter import messagebox

from pymsgbox import password

import connect
import mysql.connector as m


class DataFetcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Fetcher")
        self.root.geometry("700x700")
        self.root.configure(bg="#f3f4f6")

        # UI colors
        self.primary = "#2563eb"
        self.secondary = "#1e40af"
        self.card_color = "#ffffff"
        self.text = "#1f2937"
        self.border = "#d1d5db"

        # Initialize column entries list
        self.column_entries = []
        self.datatype_entries = []

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

        # Main container with scrollbar
        main_container = tk.Frame(self.root, bg="#f3f4f6")
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))

        # Canvas
        self.canvas = tk.Canvas(main_container, bg="#f3f4f6", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(main_container, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Scrollable frame inside canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f3f4f6")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind canvas resize
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Bind mousewheel
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Card Frame
        self.card_frame = tk.Frame(
            self.scrollable_frame,
            bg=self.card_color,
            bd=1,
            relief=tk.SOLID,
            highlightbackground=self.border,
            highlightthickness=1
        )
        self.card_frame.pack(pady=10, fill=tk.X)

        inner = tk.Frame(self.card_frame, bg=self.card_color)
        inner.pack(padx=25, pady=25, fill=tk.BOTH)

        self.td_f = tk.Frame(
            self.scrollable_frame,
            bg=self.card_color,
            bd=1,
            relief=tk.SOLID,
            highlightbackground=self.border,
            highlightthickness=1
        )

        # Password Label
        tk.Label(
            inner,
            text="Enter your Password",
            font=("Segoe UI", 11),
            bg=self.card_color,
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
            bg=self.card_color,
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

        # Create inner frame for td_f content
        self.td_inner = tk.Frame(self.td_f, bg=self.card_color)
        self.td_inner.pack(padx=25, pady=25, fill=tk.BOTH)

        # Column number input
        col_no_tag = tk.Label(
            self.td_inner,
            text="Enter how many columns you want:",
            font=("Segoe UI", 11),
            bg=self.card_color,
            fg=self.text
        )
        col_no_tag.pack(anchor="w")

        self.col_no = tk.Entry(
            self.td_inner,
            font=("Segoe UI", 12),
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.border,
            highlightcolor=self.primary
        )
        self.col_no.pack(fill=tk.X, ipady=8, pady=(5, 20))

        # Generate button
        self.generate_btn = tk.Button(
            self.td_inner,
            text="Generate Fields",
            command=self.generate_column_fields,
            bg=self.primary,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            activebackground=self.secondary,
            activeforeground="white",
            cursor="hand2"
        )
        self.generate_btn.pack(fill=tk.X, ipady=10, pady=(0, 20))

        self.generate_btn.bind("<Enter>", lambda e: self.generate_btn.config(bg=self.secondary))
        self.generate_btn.bind("<Leave>", lambda e: self.generate_btn.config(bg=self.primary))

        # Frame for dynamic column fields
        self.columns_frame = tk.Frame(self.td_inner, bg=self.card_color)
        self.columns_frame.pack(fill=tk.BOTH, expand=True)

    def generate_column_fields(self):
        """Create dynamic column name + datatype inputs."""

        # Clear previous fields
        for widget in self.columns_frame.winfo_children():
            widget.destroy()
        self.column_entries.clear()
        self.datatype_entries.clear()

        # Get number
        no = self.col_no.get().strip()

        if not no.isdigit():
            messagebox.showerror("Error", "Please enter a valid number")
            return

        no = int(no)

        if no <= 0:
            messagebox.showerror("Error", "Please enter a number greater than 0")
            return

        # Create dynamic entry fields
        for i in range(no):
            # Column name label and entry
            tk.Label(
                self.columns_frame,
                text=f"Column {i + 1} Name:",
                font=("Segoe UI", 11),
                bg=self.card_color,
                fg=self.text
            ).pack(anchor="w", pady=(10 if i > 0 else 0, 5))

            col_entry = tk.Entry(
                self.columns_frame,
                font=("Segoe UI", 12),
                relief=tk.SOLID,
                bd=1,
                highlightthickness=1,
                highlightbackground=self.border,
                highlightcolor=self.primary
            )
            col_entry.pack(fill=tk.X, ipady=8)
            self.column_entries.append(col_entry)

            # Datatype label and entry
            tk.Label(
                self.columns_frame,
                text=f"Column {i + 1} Datatype (e.g., VARCHAR(100), INT, DATE):",
                font=("Segoe UI", 11),
                bg=self.card_color,
                fg=self.text
            ).pack(anchor="w", pady=(10, 5))

            dtype_entry = tk.Entry(
                self.columns_frame,
                font=("Segoe UI", 12),
                relief=tk.SOLID,
                bd=1,
                highlightthickness=1,
                highlightbackground=self.border,
                highlightcolor=self.primary
            )
            dtype_entry.pack(fill=tk.X, ipady=8)
            self.datatype_entries.append(dtype_entry)

        # Submit button
        self.submit_btn = tk.Button(
            self.columns_frame,
            text="Create Table",
            command=self.create_table,
            bg=self.primary,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            activebackground=self.secondary,
            activeforeground="white",
            cursor="hand2"
        )
        self.submit_btn.pack(fill=tk.X, ipady=10, pady=(20, 0))

        self.submit_btn.bind("<Enter>", lambda e: self.submit_btn.config(bg=self.secondary))
        self.submit_btn.bind("<Leave>", lambda e: self.submit_btn.config(bg=self.primary))

    def create_table(self):
        """Process the column data and create table."""
        columns = []

        for col_entry, dtype_entry in zip(self.column_entries, self.datatype_entries):
            col_name = col_entry.get().strip()
            col_type = dtype_entry.get().strip()

            if not col_name or not col_type:
                messagebox.showerror("Error", "All column names and datatypes are required")
                return

            columns.append((col_name, col_type))

        # Here you can process the columns data
        # For now, just show success message
        col_str = "\n".join([f"{name}: {dtype}" for name, dtype in columns])
        messagebox.showinfo("Success", f"Table structure ready:\n\n{col_str}")

        # You can add your table creation logic here
        # For example: create_table_in_db(columns)

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
            # Connect to MySQL WITHOUT selecting a database
            con = m.connect(
                host="localhost",
                user="root",
                password=password
            )
            cur = con.cursor()

            # Create database if not exists
            cur.execute("CREATE DATABASE IF NOT EXISTS data_fetcher;")
            con.commit()
            con.close()

            # Now create the table using your external module
            connect.est(p=password, table_name=table)

            messagebox.showinfo("Success", f"Connected to table '{table}' successfully!")

            # Clear inputs
            self.password_entry.delete(0, tk.END)
            self.table_entry.delete(0, tk.END)

            # Hide the card frame and show table definition frame
            self.card_frame.destroy()
            self.td_f.pack(pady=10, fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """When canvas is resized, resize the inner frame to match"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# Main App
if __name__ == "__main__":
    root = tk.Tk()
    app = DataFetcher(root)

    # App Icon
    try:
        icon = tk.PhotoImage(file="logo.png")
        root.iconphoto(False, icon)
    except:
        pass  # If icon file doesn't exist, continue without it

    root.mainloop()