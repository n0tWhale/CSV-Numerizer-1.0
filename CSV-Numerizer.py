import pandas as pd
from numerizer import numerize
import tkinter as tk
from tkinter import filedialog, messagebox

#Функция по формотированию числительных
def execute_code():
    path = file_entry.get()
    global df
    df = pd.read_csv(path)
    if any(df.select_dtypes(include=["object"]).apply(lambda x: x.str.contains("\d")).sum()):
        for col in df.select_dtypes(include=["object"]):
            df[col] = df[col].apply(lambda x: numerize(x))
        if messagebox.askyesno(title="Сохранить изменения", message="Числительные были переведены в цифровую форму. Хотите сохранить изменения в действующем файле? \n(В ином случае выбирите путь для копии)"):
            df.to_csv(path, index=False)
        else:
            save_copy(path)
    else:
        messagebox.showinfo(title="", message="Файл не содержит числительных в словесной форме.")

# Главное окно
root = tk.Tk()
root.title("CSV-Numerizer 1.0")
root.resizable(width=False, height=False)

#Открывает окно для выбора файла, получает путь к выбранному файлу и устанавливает его в поле для ввода пути
def select_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Выберите файл", filetype=(("CSV files", ".csv"), ("All Files", ".*")))
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

# Элементы интерфейса
file_label = tk.Label(root, text="Выберите csv-файл:")
file_entry = tk.Entry(root)
file_button = tk.Button(root, text="···", command=select_file)
execute_button = tk.Button(root, text="Выполнить", command=execute_code)

# Расположение элементов на форме
file_label.grid(row=0, column=0, padx=10, pady=10)
file_entry.grid(row=0, column=1, padx=10, pady=10)
file_button.grid(row=0, column=2, padx=10, pady=10)
execute_button.grid(row=1, column=1, padx=10, pady=10)

#Открывает диалоговое окно для сохранения файла, вызывается при необходимости сохранения изменений
def save_copy(path):
    new_path = filedialog.asksaveasfilename(initialdir="/", title="Сохранить копию файла", defaultextension=".csv", filetypes=(("CSV files", "*.csv"),))
    if new_path:
        df.to_csv(new_path, index=False)
        messagebox.showinfo(title="Успех", message=f"Файл успешно сохранен по пути:\n{new_path}")

# Цикл, чтоб интерфейс работал
root.mainloop()
