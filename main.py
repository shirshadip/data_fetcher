import tkinter as tk
from tkinter import ttk, messagebox
import database

class DataFetcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Fetcher")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Color scheme
        self.bg_color = "#f5f5f5"
        self.primary_color = "#2563eb"
        self.secondary_color = "#1e40af"
        self.card_color = "#ffffff"
        self.text_color = "#1f2937"
        self.border_color = "#e5e7eb"

        self.root.configure(bg=self.bg_color)

        self.setup_ui()

    def setup_ui(self):
        # Create a canvas and scrollbar
        canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        
        # Create a frame inside the canvas
        self.scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        # Configure the canvas to work with the scrollbar
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.scrollable_frame.bind("<Configure>", on_frame_configure)
        
        # Create a window in the canvas for the frame
        canvas_frame = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        
        # Center the content horizontally
        def on_canvas_configure(event):
            canvas_width = event.width
            frame_width = self.scrollable_frame.winfo_reqwidth()
            if frame_width < canvas_width:
                x_position = (canvas_width - frame_width) // 2
            else:
                x_position = 0
            canvas.coords(canvas_frame, x_position, 0)
        
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Main container (now inside scrollable_frame)
        main_container = tk.Frame(self.scrollable_frame, bg=self.bg_color, width=600)
        main_container.pack(fill=tk.BOTH, padx=40, pady=40)
        
        # Title
        title = tk.Label(
            main_container,
            text="Data Fetcher",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(pady=(0, 30))
        
        # Options card
        options_card = tk.Frame(
            main_container,
            bg=self.card_color,
            relief=tk.FLAT,
            bd=0
        )
        options_card.pack(fill=tk.X)
        
        # Add shadow effect with border
        options_card.config(highlightbackground=self.border_color, highlightthickness=1)
        
        # Card content
        card_content = tk.Frame(options_card, bg=self.card_color)
        card_content.pack(padx=30, pady=30, fill=tk.X)
        
        # Option label
        option_label = tk.Label(
            card_content,
            text="Select an option",
            font=("Segoe UI", 12),
            bg=self.card_color,
            fg=self.text_color
        )
        option_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Custom styled dropdown
        self.selected = tk.StringVar(value="Create a new database")
        self.options = ["Create a new database", "Work with existing database"]
        
        dropdown_frame = tk.Frame(card_content, bg=self.card_color)
        dropdown_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Style for OptionMenu
        self.dropdown = tk.OptionMenu(
            dropdown_frame,
            self.selected,
            *self.options,
            command=self.on_option_change
        )
        self.dropdown.config(
            font=("Segoe UI", 11),
            bg=self.card_color,
            fg=self.text_color,
            activebackground=self.primary_color,
            activeforeground="white",
            relief=tk.SOLID,
            bd=1,
            highlightthickness=0,
            width=30
        )
        self.dropdown.pack(fill=tk.X)
        
        # Database creation form
        self.form_frame = tk.Frame(card_content, bg=self.card_color)
        
        # Database name
        db_label = tk.Label(
            self.form_frame,
            text="Database Name",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color
        )
        db_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.db_name = tk.Entry(
            self.form_frame,
            font=("Segoe UI", 11),
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground=self.border_color
        )
        self.db_name.pack(fill=tk.X, ipady=8)
        
        # Password
        pas_label = tk.Label(
            self.form_frame,
            text="Password",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color
        )
        pas_label.pack(anchor=tk.W, pady=(15, 5))
        
        self.pas = tk.Entry(
            self.form_frame,
            font=("Segoe UI", 11),
            show="●",
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground=self.border_color
        )
        self.pas.pack(fill=tk.X, ipady=8)
        
        # Connect button
        self.db_btn = tk.Button(
            self.form_frame,
            text="Create Database",
            font=("Segoe UI", 11, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground=self.secondary_color,
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.create_database
        )
        self.db_btn.pack(fill=tk.X, pady=(20, 0), ipady=10)
        
        # Bind hover effects
        self.db_btn.bind("<Enter>", lambda e: self.db_btn.config(bg=self.secondary_color))
        self.db_btn.bind("<Leave>", lambda e: self.db_btn.config(bg=self.primary_color))
        
        # Connection frame (for "Work with existing database")
        self.con_frame = tk.Frame(card_content, bg=self.card_color)
        
        con_label = tk.Label(
            self.con_frame,
            text="Connect to existing database",
            font=("Segoe UI", 11),
            bg=self.card_color,
            fg=self.text_color
        )
        con_label.pack(pady=20)
        
        # Show initial state
        self.on_option_change(self.selected.get())
    
    def on_option_change(self, choice):
        # Hide both frames
        self.form_frame.pack_forget()
        self.con_frame.pack_forget()
        
        # Show the appropriate frame
        if self.selected.get() == "Create a new database":
            self.form_frame.pack(fill=tk.X)
        else:
            self.con_frame.pack(fill=tk.X)
    
    def create_database(self):
        db = self.db_name.get().strip()
        password = self.pas.get()
        
        # Validation
        if not db:
            messagebox.showerror("Error", "Please enter a database name")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        
        try:
            database.database(password, db)
            messagebox.showinfo("Success", f"Connected to database: {db}")
            # Clear fields after success
            self.db_name.delete(0, tk.END)
            self.pas.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    icon = tk.PhotoImage(file="logo.png")
    root.iconphoto(False, icon)
    app = DataFetcher(root)
    root.mainloop()