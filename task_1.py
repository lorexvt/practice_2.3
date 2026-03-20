import tkinter as tk
import requests


def check_sites():
    sites = [
        "https://github.com/",
        "https://www.binance.com/en",
        "https://tomtit.tomsk.ru/",
        "https://jsonplaceholder.typicode.com/",
        "https://moodle.tomtit-tomsk.ru/"
    ]

    # Очищаем текстовое поле
    text.delete(1.0, tk.END)
    text.insert(tk.END, "Результаты проверки сайтов:\n")
    text.insert(tk.END, "=" * 50 + "\n")

    for site in sites:
        try:
            response = requests.get(site, timeout=5)
            code = response.status_code

            if code == 200:
                status = "Доступен"
            elif code == 403:
                status = "Вход запрещен"
            elif code == 404:
                status = "Не найден"
            else:
                status = f"Код {code}"

        except:
            status = "Не доступен"
            code = "Ошибка"

        text.insert(tk.END, f"{site} – {status} – {code}\n")

    text.insert(tk.END, "=" * 50 + "\n")



window = tk.Tk()
window.title("Проверка доступности сайтов")
window.geometry("600x400")


btn_check = tk.Button(window, text="Проверить сайты", command=check_sites, bg="lightblue", font=("Arial", 12))
btn_check.pack(pady=10)


text = tk.Text(window, wrap=tk.WORD, font=("Courier", 10))
text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)


window.mainloop()