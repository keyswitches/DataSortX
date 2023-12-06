import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from pandastable import Table, TableModel

def choose_file():
    file_path = filedialog.askopenfilename()

    if file_path:
        file_name = os.path.basename(file_path)
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_name)

def load_columns():
    selected_file = file_entry.get()

    if not selected_file:
        messagebox.showerror("Error", "Please select a file.")
        return

    try:
        import openpyxl
    except ImportError:
        messagebox.showerror("Error", "Please install openpyxl library to proceed.")
        return

    wb = openpyxl.load_workbook(selected_file, read_only=True)
    ws = wb.active

    columns_to_sort = {}

    for row in ws.iter_rows(min_row=1, max_row=1, values_only=True):
        for col_idx, col_name in enumerate(row):
            col_name = col_name or f"Column_{col_idx + 1}"
            columns_to_sort[col_name] = tk.IntVar()
            tk.Checkbutton(main_window, text=col_name, variable=columns_to_sort[col_name]).pack(anchor=tk.W)

    show_data_btn = tk.Button(main_window, text="Show Data", command=lambda: show_data(selected_file, columns_to_sort))
    show_data_btn.pack()
    
    sort_btn = tk.Button(main_window, text="Sort", command=lambda: sort_columns(selected_file, columns_to_sort))
    sort_btn.pack()

def show_data(selected_file, columns_to_sort):
    show_data_window = tk.Toplevel(main_window)
    show_data_window.title("File Data")

    if selected_file.endswith('.xlsx'):
        df = pd.read_excel(selected_file)
    elif selected_file.endswith('.csv'):
        df = pd.read_csv(selected_file)
    else:
        messagebox.showerror("Error", "Unsupported file format.")
        return

    frame = tk.Frame(show_data_window)
    frame.pack(fill="both", expand=True)

    pt = Table(frame, dataframe=df)
    pt.show()

    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    window_width = 1200
    window_height = 600
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2

    show_data_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    pt._table_widget.config(width=window_width)
    
def sort_columns(selected_file, columns_to_sort):
    if not selected_file:
        messagebox.showerror("Error", "Please select a file.")
        return

    try:
        if selected_file.endswith('.xlsx'):
            df = pd.read_excel(selected_file)
        elif selected_file.endswith('.csv'):
            df = pd.read_csv(selected_file)
        else:
            messagebox.showerror("Error", "Unsupported file format.")
            return

        selected_columns = [col for col, var in columns_to_sort.items() if var.get() == 1]
        
        if not selected_columns:
            messagebox.showerror("Error", "Please select columns to sort.")
            return

        sorted_df = df.sort_values(by=selected_columns)
        
        show_sorted_window = tk.Toplevel(main_window)
        show_sorted_window.title("Sorted Data")

        frame_sorted = tk.Frame(show_sorted_window)
        frame_sorted.pack(fill="both", expand=True)

        pt_sorted = Table(frame_sorted, dataframe=sorted_df)
        pt_sorted.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("File Selection")

    file_label = tk.Label(main_window, text="Select a file:")
    file_label.pack()

    file_entry = tk.Entry(main_window, width=50)
    file_entry.pack()

    file_button = tk.Button(main_window, text="Browse", command=choose_file)
    file_button.pack()

    load_button = tk.Button(main_window, text="Load Columns", command=load_columns)
    load_button.pack()

    main_window.mainloop()
