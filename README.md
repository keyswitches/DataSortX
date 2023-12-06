# File Data Viewer

This Python application, built with Tkinter and Pandas, offers a user-friendly interface to visualize data from Excel (.xlsx) and CSV files. It enables users to:

- Browse and select a file from their system
- Load columns dynamically from the selected file
- Display data in a table format for easy viewing
- Sort columns based on user selection

## Features:

- **File Selection:** Browse and select Excel or CSV files.
- **Dynamic Column Loading:** Automatically loads columns from selected files for sorting.
- **Data Visualization:** Presents data in a table format using the PandasTable library.
- **Column Sorting:** Sorts columns based on user-defined selections.

## How to Use:

1. **Select File:** Click the "Browse" button to choose an Excel or CSV file.
2. **Load Columns:** Automatically loads columns from the selected file for sorting.
3. **Show Data:** Displays the selected data in a user-friendly table view.
4. **Sort:** Sorts columns based on user selection.

## Installation:

To run this program, you'll need to install the following libraries:

- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Pandas](https://pandas.pydata.org/)
- [PandasTable](https://github.com/dmnfarrell/pandastable)

You can install these libraries using `pip`:

```bash
pip install pandas pandastable
