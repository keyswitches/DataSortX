import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from pandastable import Table, TableModel
import warnings

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

    wb = None
    ws = None

    try:
        if selected_file.endswith('.xlsx'):
            import openpyxl
            wb = openpyxl.load_workbook(selected_file, read_only=True)
            ws = wb.active

        elif selected_file.endswith('.csv'):
            columns_to_sort = {}
            df = pd.read_csv(selected_file)

            for col_name in df.columns:
                columns_to_sort[col_name] = tk.IntVar()
                tk.Checkbutton(main_window, text=col_name, variable=columns_to_sort[col_name]).pack(anchor=tk.W)

            show_data_btn = tk.Button(main_window, text="Show Data", command=lambda: show_data(df, columns_to_sort))
            show_data_btn.pack()
            
            sort_btn = tk.Button(main_window, text="Sort", command=lambda: sort_columns(df, columns_to_sort))
            sort_btn.pack()

        else:
            messagebox.showerror("Error", "Unsupported file format.")

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please select a valid file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        if wb:
            wb.close()

def show_data(df, columns_to_sort):
    show_data_window = tk.Toplevel(main_window)
    show_data_window.title("File Data")

    try:
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

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def sort_columns(df, columns_to_sort):
    try:
        selected_columns = [col for col, var in columns_to_sort.items() if var.get() == 1]
        
        if not selected_columns:
            messagebox.showerror("Error", "Please select columns to sort.")
            return

        sorted_df = df[selected_columns].sort_values(by=selected_columns)

        show_sorted_window = tk.Toplevel(main_window)
        show_sorted_window.title("Sorted Data")

        frame_sorted = tk.Frame(show_sorted_window)
        frame_sorted.pack(fill="both", expand=True)

        pt_sorted = Table(frame_sorted, dataframe=sorted_df)
        pt_sorted.show()

        export_button = tk.Button(show_sorted_window, text="Export", command=lambda: export_sorted_data(sorted_df))
        export_button.pack()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def export_sorted_data(sorted_df):
    try:
        export_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if export_file_path:
            sorted_df.to_csv(export_file_path, index=False)
            messagebox.showinfo("Success", "Data exported successfully to CSV.")
        else:
            messagebox.showinfo("Information", "Export canceled.")
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
