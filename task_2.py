import tkinter as tk
import psutil


def update_info():
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    cpu_label.config(text=f"Загрузка CPU: {cpu}%")
    ram_label.config(text=f"Использовано RAM: {memory.percent}%")
    disk_label.config(text=f"Загруженность диска: {disk.percent}%")

    window.after(1000, update_info)


window = tk.Tk()
window.title("Системный монитор")
window.geometry("300x200")

title = tk.Label(window, text="СИСТЕМНЫЙ МОНИТОР", font=("Arial", 14, "bold"))
title.pack(pady=10)

tk.Label(window, text="=" * 30).pack()

cpu_label = tk.Label(window, text="Загрузка CPU: --%", font=("Arial", 12))
cpu_label.pack(pady=5)

ram_label = tk.Label(window, text="Использовано RAM: --%", font=("Arial", 12))
ram_label.pack(pady=5)

disk_label = tk.Label(window, text="Загруженность диска: --%", font=("Arial", 12))
disk_label.pack(pady=5)

tk.Label(window, text="=" * 30).pack()

exit_btn = tk.Button(window, text="Выход", command=window.quit, bg="lightcoral")
exit_btn.pack(pady=10)

update_info()

window.mainloop()