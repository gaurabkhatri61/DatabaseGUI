import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")

        self.frame = tk.Frame(self.master)

        tk.Label(self.frame, text="Employee ID:").grid(row=0, column=0, padx=5, pady=5)
        self.employee_id_entry = tk.Entry(self.frame)
        self.employee_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.frame, text="Login", command=self.login).grid(row=2, columnspan=2, padx=5, pady=5)

        self.frame.pack()

    def login(self):
        employee_id = self.employee_id_entry.get()
        password = self.password_entry.get()

        query = "SELECT * FROM users WHERE EmployeeID = %s AND password = %s"
        cursor.execute(query, (employee_id, password))
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.master.destroy()  # Close login window
            operator_dashboard = OperatorDashboard()
            operator_dashboard.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

class OperatorDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Melo Telecom")
        self.geometry("600x400")

        self.label = tk.Label(self, text="Operator Dashboard", font=("times new roman", 14))
        self.label.pack(pady=20)

        # Create a frame to contain buttons on the left side
        left_frame = tk.Frame(self)
        left_frame.pack(side="left", padx=10)

        # Create buttons and pack them in the left frame
        self.view_employee_button = tk.Button(left_frame, text="View Employees", command=self.view_employees)
        self.view_employee_button.pack(pady=5, anchor="w")

        self.view_problem_button = tk.Button(left_frame, text="View Problem Types", command=self.view_problem_types)
        self.view_problem_button.pack(pady=5, anchor="w")

        self.view_software_button = tk.Button(left_frame, text="View Software", command=self.view_software)
        self.view_software_button.pack(pady=5, anchor="w")

        self.view_technician_button = tk.Button(left_frame, text="View Technicians", command=self.view_technicians)
        self.view_technician_button.pack(pady=5, anchor="w")

        self.view_devices_button = tk.Button(left_frame, text="View Company Devices", command=self.view_company_devices)
        self.view_devices_button.pack(pady=5, anchor="w")

        self.view_callers_button = tk.Button(left_frame, text="View Callers", command=self.view_callers)
        self.view_callers_button.pack(pady=5, anchor="w")
        
        self.view_problem_history_button = tk.Button(left_frame, text="View Problem History", command=self.view_problem_history)
        self.view_problem_history_button.pack(pady=5, anchor="w")
        
        # Create a frame to contain the "Add Entry" button at the bottom right
        add_entry_frame = tk.Frame(self)
        add_entry_frame.pack(side="bottom", pady=10, padx=10, anchor="se")

        # Add button to open call record form and place it in the add_entry_frame
        self.add_record_button = tk.Button(add_entry_frame, text="Add Record", command=self.open_call_record_form)
        self.add_record_button.pack(side="right")

        # Connect to the database
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="operator",
            password="9866579513gaurab",
            database="melo"
        )

    def view_employees(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Employee")
        records = cursor.fetchall()
        cursor.close()

        if records:
            self.show_records_in_table(records, "Employee Records")
        else:
            messagebox.showinfo("Employee Records", "No records found.")

    def view_problem_types(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Problem_type")
        records = cursor.fetchall()
        cursor.close()

        if records:
            self.show_records_in_table(records, "Problem Type Records")
        else:
            messagebox.showinfo("Problem Type Records", "No records found.")

    def view_software(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Software")
        records = cursor.fetchall()
        cursor.close()

        if records:
            self.show_records_in_table(records, "Software Records")
        else:
            messagebox.showinfo("Software Records", "No records found.")

    def view_technicians(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Technician")
        records = cursor.fetchall()
        cursor.close()

        if records:
            self.show_records_in_table(records, "Technician Records")
        else:
            messagebox.showinfo("Technician Records", "No records found.")

    def view_company_devices(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Company_Devices")
        records = cursor.fetchall()
        cursor.close()

        if records:
            self.show_records_in_table(records, "Company Devices Records")
        else:
            messagebox.showinfo("Company Devices Records", "No records found.")

    def view_callers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Caller")
        records = cursor.fetchall()
        cursor.close()

        if records:
            self.show_records_in_table(records, "Caller Records")
        else:
            messagebox.showinfo("Caller Records", "No records found.")
            
    def view_problem_history(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Problem_History")
        records = cursor.fetchall()
        cursor.close()

        if records:
            self.show_records_in_table(records, "Problem History Records")
        else:
            messagebox.showinfo("Problem History Records", "No records found.")

    def show_records_in_table(self, records, title):
        record_window = tk.Toplevel(self)
        record_window.title(title)

        tree = ttk.Treeview(record_window)
        tree["columns"] = tuple([f"Column {i+1}" for i in range(len(records[0]))])
        tree["show"] = "headings"

        for i, record in enumerate(records[0]):
            tree.heading(f"Column {i+1}", text=record)

        for record in records:
            tree.insert("", "end", values=record)

        tree.pack(expand=True, fill="both")

    def open_call_record_form(self):
        call_record_form = CallRecordForm(self)
        call_record_form.grab_set()  # Make the form modal
        self.wait_window(call_record_form)

    def create_problem_history_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Problem_History (
                    Problem_id INT AUTO_INCREMENT PRIMARY KEY,
                    Problem_description VARCHAR(255),
                    Solution VARCHAR(255),
                    Solution_durationtime INT,
                    Solution_date DATE,
                    Problem_status ENUM ('Waiting', 'On-progress', 'Solved'),
                    Type_id INT,
                    Call_id INT,
                    FOREIGN KEY (Type_id) REFERENCES Problem_type(Type_id),
                    FOREIGN KEY (Call_id) REFERENCES Call_record(Call_id)
                )
            """)
            messagebox.showinfo("Success", "Problem_History table created successfully!")
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

    def __del__(self):
        self.conn.close()

class CallRecordForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Call Record Form")
        self.geometry("400x300")

        self.master = master

        # Database connection
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="operator",
            password="9866579513gaurab",
            database="melo"
        )
        self.cursor = self.conn.cursor()

        # Create form fields
        tk.Label(self, text="Call Datetime:").grid(row=0, column=0, padx=5, pady=5)
        self.call_datetime_entry = tk.Entry(self)
        self.call_datetime_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Call Duration:").grid(row=1, column=0, padx=5, pady=5)
        self.call_duration_entry = tk.Entry(self)
        self.call_duration_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Call Reason:").grid(row=2, column=0, padx=5, pady=5)
        self.call_reason_var = tk.StringVar()
        self.call_reason_var.set("New")  # Default value
        self.call_reason_option = tk.OptionMenu(self, self.call_reason_var, "New", "Follow-up")
        self.call_reason_option.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Call Queries:").grid(row=3, column=0, padx=5, pady=5)
        self.call_queries_entry = tk.Entry(self)
        self.call_queries_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="Device ID:").grid(row=4, column=0, padx=5, pady=5)
        self.device_id_entry = tk.Entry(self)
        self.device_id_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self, text="Operator ID:").grid(row=5, column=0, padx=5, pady=5)
        self.operator_id_entry = tk.Entry(self)
        self.operator_id_entry.grid(row=5, column=1, padx=5, pady=5)

        # Submit button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=6, columnspan=2, padx=5, pady=10)

    def submit_form(self):
        # Get form data
        call_datetime = self.call_datetime_entry.get()
        call_duration = self.call_duration_entry.get()
        call_reason = self.call_reason_var.get()
        call_queries = self.call_queries_entry.get()
        device_id = self.device_id_entry.get()
        operator_id = self.operator_id_entry.get()

        # Insert data into the database
        query = "INSERT INTO Call_record (Call_datetime, Call_duration, Call_reason, Call_queries, Device_id, Operator_id) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (call_datetime, call_duration, call_reason, call_queries, device_id, operator_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Call Record added successfully!")
            self.destroy()  # Close the form after successful submission
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

    def __del__(self):
        # Close database connection when the window is closed
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="operator",
        password="9866579513gaurab",
        database="melo"
    )
    cursor = conn.cursor()

    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()

    cursor.close()
    conn.close()
