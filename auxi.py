import time

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


def get_name_surfix(filename):
    try:
        pos = filename.rfind('.')
        return filename[:pos], filename[pos+1:]
    except ValueError:
        return filename, ""


def set_count_in_entry(count_entry, count):
    count_entry.configure(state=tk.NORMAL)
    count_entry.delete(0, tk.END)
    count_entry.insert(tk.END, str(count))
    count_entry.configure(state='disabled')

def get_date(sec):
    return time.strftime('%Y-%m-%d', time.localtime((sec)))
