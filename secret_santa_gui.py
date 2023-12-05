# Contents of secret_santa_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from secret_santa_generator import read_ss_list, secret_santa, email_participants

def browse_file(entry):
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def generate_pairings():
    file_name = participants_entry.get()
    if not file_name:
        messagebox.showerror("Error", "Please select a participant file.")
        return
    
    people_email_dict = read_ss_list(file_name)
    partners = secret_santa(people_email_dict)

    result_text.delete("1.0", tk.END)
    for pair in partners:
        result_text.insert(tk.END, f"{pair[0]} -> {pair[1]}\n")

def send_emails():
    people_email_dict = read_ss_list(participants_entry.get())
    email_subject = subject_entry.get()

    if not email_subject:
        messagebox.showerror("Error", "Please enter an email subject.")
        return

    email_participants(people_email_dict, secret_santa(people_email_dict), email_subject)
    messagebox.showinfo("Success", "Emails sent successfully!")

# Tkinter GUI
root = tk.Tk()
root.title("Secret Santa Generator")

# Participant file selection
tk.Label(root, text="Participant File:").grid(row=0, column=0, padx=10, pady=10)
participants_entry = tk.Entry(root, width=50)
participants_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: browse_file(participants_entry)).grid(row=0, column=2, padx=10, pady=10)

# Generate pairings
tk.Button(root, text="Generate Pairings", command=generate_pairings).grid(row=1, column=1, padx=10, pady=10)

# Results display
result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Email subject entry
tk.Label(root, text="Email Subject:").grid(row=3, column=0, padx=10, pady=10)
subject_entry = tk.Entry(root, width=50)
subject_entry.grid(row=3, column=1, padx=10, pady=10)

# Send emails
tk.Button(root, text="Send Emails", command=send_emails).grid(row=4, column=1, padx=10, pady=10)

root.mainloop()