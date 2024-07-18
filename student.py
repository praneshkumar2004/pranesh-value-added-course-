import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


conn = sqlite3.connect('student_management.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS students
             (register_number TEXT PRIMARY KEY, 
              name TEXT, 
              mark1 INTEGER, 
              mark2 INTEGER, 
              mark3 INTEGER,
              average REAL,
              rank INTEGER)''')
conn.commit()

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        
        self.num_students_label = ttk.Label(root, text="Enter number of students:")
        self.num_students_label.grid(row=0, column=0, padx=10, pady=10)
        self.num_students_entry = ttk.Entry(root)
        self.num_students_entry.grid(row=0, column=1, padx=10, pady=10)
        self.submit_button = ttk.Button(root, text="Submit", command=self.create_student_entries)
        self.submit_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.student_entries_frame = ttk.Frame(root)
        self.student_entries_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        self.show_rank_button = ttk.Button(root, text="Show Ranks", command=self.show_ranks)
        self.show_rank_button.grid(row=2, column=0, padx=10, pady=10)
        self.show_student_button = ttk.Button(root, text="Show Student Details", command=self.show_student_details)
        self.show_student_button.grid(row=2, column=1, padx=10, pady=10)
        
    def create_student_entries(self):
        self.num_students = int(self.num_students_entry.get())
        for widget in self.student_entries_frame.winfo_children():
            widget.destroy()
        
        self.entries = []
        for i in range(self.num_students):
            name_label = ttk.Label(self.student_entries_frame, text=f"Student {i+1} Name:")
            name_label.grid(row=i, column=0, padx=10, pady=10)
            name_entry = ttk.Entry(self.student_entries_frame)
            name_entry.grid(row=i, column=1, padx=10, pady=10)
            
            reg_label = ttk.Label(self.student_entries_frame, text=f"Register Number:")
            reg_label.grid(row=i, column=2, padx=10, pady=10)
            reg_entry = ttk.Entry(self.student_entries_frame)
            reg_entry.grid(row=i, column=3, padx=10, pady=10)
            
            mark1_label = ttk.Label(self.student_entries_frame, text=f"Mark 1:")
            mark1_label.grid(row=i, column=4, padx=10, pady=10)
            mark1_entry = ttk.Entry(self.student_entries_frame)
            mark1_entry.grid(row=i, column=5, padx=10, pady=10)
            
            mark2_label = ttk.Label(self.student_entries_frame, text=f"Mark 2:")
            mark2_label.grid(row=i, column=6, padx=10, pady=10)
            mark2_entry = ttk.Entry(self.student_entries_frame)
            mark2_entry.grid(row=i, column=7, padx=10, pady=10)
            
            mark3_label = ttk.Label(self.student_entries_frame, text=f"Mark 3:")
            mark3_label.grid(row=i, column=8, padx=10, pady=10)
            mark3_entry = ttk.Entry(self.student_entries_frame)
            mark3_entry.grid(row=i, column=9, padx=10, pady=10)
            
            self.entries.append((name_entry, reg_entry, mark1_entry, mark2_entry, mark3_entry))
        
        self.save_button = ttk.Button(self.student_entries_frame, text="Save", command=self.save_students)
        self.save_button.grid(row=self.num_students, column=0, columnspan=10, pady=10)
    
    def save_students(self):
        for entry in self.entries:
            name = entry[0].get()
            reg_no = entry[1].get()
            mark1 = int(entry[2].get())
            mark2 = int(entry[3].get())
            mark3 = int(entry[4].get())
            average = (mark1 + mark2 + mark3) / 3
            c.execute("INSERT OR REPLACE INTO students (register_number, name, mark1, mark2, mark3, average) VALUES (?, ?, ?, ?, ?, ?)", 
                      (reg_no, name, mark1, mark2, mark3, average))
        
        conn.commit()
        self.allocate_ranks()
        messagebox.showinfo("Success", "Students saved successfully!")
    
    def allocate_ranks(self):
        c.execute("SELECT register_number, average FROM students ORDER BY average DESC")
        students = c.fetchall()
        rank = 1
        for student in students:
            c.execute("UPDATE students SET rank = ? WHERE register_number = ?", (rank, student[0]))
            rank += 1
        conn.commit()
    
    def show_ranks(self):
        c.execute("SELECT name, register_number, rank FROM students ORDER BY rank")
        students = c.fetchall()
        rank_str = ""
        for student in students:
            rank_str += f"Name: {student[0]}, Register Number: {student[1]}, Rank: {student[2]}\n"
        
        messagebox.showinfo("Student Ranks", rank_str)
    
    def show_student_details(self):
        reg_no = tk.simpledialog.askstring("Input", "Enter Register Number:")
        c.execute("SELECT name, mark1, mark2, mark3, average, rank FROM students WHERE register_number = ?", (reg_no,))
        student = c.fetchone()
        
        if student:
            fig, ax = plt.subplots()
            subjects = ['Mark 1', 'Mark 2', 'Mark 3']
            marks = [student[1], student[2], student[3]]
            ax.bar(subjects, marks)
            ax.set_title(f"Marks for {student[0]}")
            ax.set_xlabel("Subjects")
            ax.set_ylabel("Marks")
            plt.ylim(0, 100)
            
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, pady=20)
            
            details = f"Name: {student[0]}\nAverage: {student[4]}\nRank: {student[5]}"
            messagebox.showinfo("Student Details", details)
        else:
            messagebox.showerror("Error", "Student not found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()
