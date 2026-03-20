import tkinter as tk
from tkinter import ttk, messagebox
import requests


class GitHubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub API")
        self.root.geometry("700x500")

        tab_control = ttk.Notebook(root)

        tab_profile = ttk.Frame(tab_control)
        tab_control.add(tab_profile, text="Профиль")
        self.create_profile_tab(tab_profile)

        tab_repos = ttk.Frame(tab_control)
        tab_control.add(tab_repos, text="Репозитории")
        self.create_repos_tab(tab_repos)

        tab_search = ttk.Frame(tab_control)
        tab_control.add(tab_search, text="Поиск")
        self.create_search_tab(tab_search)

        tab_control.pack(expand=1, fill="both")

    def create_profile_tab(self, parent):
        tk.Label(parent, text="Имя пользователя:").pack(pady=5)
        self.profile_entry = tk.Entry(parent, width=40)
        self.profile_entry.pack()

        tk.Button(parent, text="Получить информацию",
                  command=self.get_profile).pack(pady=10)

        self.profile_text = tk.Text(parent, height=20, width=70)
        self.profile_text.pack(pady=10)

    def create_repos_tab(self, parent):
        tk.Label(parent, text="Имя пользователя:").pack(pady=5)
        self.repos_entry = tk.Entry(parent, width=40)
        self.repos_entry.pack()

        tk.Button(parent, text="Получить репозитории",
                  command=self.get_repos).pack(pady=10)

        self.repos_text = tk.Text(parent, height=20, width=70)
        self.repos_text.pack(pady=10)

    def create_search_tab(self, parent):
        tk.Label(parent, text="Название репозитория:").pack(pady=5)
        self.search_entry = tk.Entry(parent, width=40)
        self.search_entry.pack()

        tk.Button(parent, text="Поиск",
                  command=self.search_repos).pack(pady=10)

        self.search_text = tk.Text(parent, height=20, width=70)
        self.search_text.pack(pady=10)

    def get_profile(self):
        username = self.profile_entry.get()
        if not username:
            messagebox.showerror("Ошибка", "Введите имя пользователя")
            return

        url = f"https://api.github.com/users/{username}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                user = response.json()

                self.profile_text.delete(1.0, tk.END)
                self.profile_text.insert(tk.END, "=" * 50 + "\n")
                self.profile_text.insert(tk.END, "ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ\n")
                self.profile_text.insert(tk.END, "=" * 50 + "\n")
                self.profile_text.insert(tk.END, f"Имя: {user.get('name', 'Не указано')}\n")
                self.profile_text.insert(tk.END, f"Профиль: {user.get('html_url', 'Нет')}\n")
                self.profile_text.insert(tk.END, f"Репозиториев: {user.get('public_repos', 0)}\n")
                self.profile_text.insert(tk.END, f"Подписчиков: {user.get('followers', 0)}\n")
                self.profile_text.insert(tk.END, f"Подписок: {user.get('following', 0)}\n")
                self.profile_text.insert(tk.END, f"Обсуждений: {user.get('public_gists', 0)}\n")
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден")
        except:
            messagebox.showerror("Ошибка", "Ошибка подключения к API")

    def get_repos(self):
        username = self.repos_entry.get()
        if not username:
            messagebox.showerror("Ошибка", "Введите имя пользователя")
            return

        url = f"https://api.github.com/users/{username}/repos"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                repos = response.json()

                self.repos_text.delete(1.0, tk.END)

                if not repos:
                    self.repos_text.insert(tk.END, "У пользователя нет репозиториев")
                    return

                self.repos_text.insert(tk.END, "=" * 50 + "\n")
                self.repos_text.insert(tk.END, f"РЕПОЗИТОРИИ {username}\n")
                self.repos_text.insert(tk.END, "=" * 50 + "\n")

                for repo in repos:
                    self.repos_text.insert(tk.END, f"\nНазвание: {repo['name']}\n")
                    self.repos_text.insert(tk.END, f"Ссылка: {repo['html_url']}\n")
                    self.repos_text.insert(tk.END, f"Язык: {repo.get('language', 'Не указан')}\n")
                    self.repos_text.insert(tk.END, f"Видимость: {'Приватный' if repo['private'] else 'Публичный'}\n")
                    self.repos_text.insert(tk.END, f"Ветка: {repo['default_branch']}\n")
                    self.repos_text.insert(tk.END, f"Просмотров: {repo.get('watchers_count', 0)}\n")
                    self.repos_text.insert(tk.END, "-" * 30 + "\n")
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден")
        except:
            messagebox.showerror("Ошибка", "Ошибка подключения к API")

    def search_repos(self):
        query = self.search_entry.get()
        if not query:
            messagebox.showerror("Ошибка", "Введите название для поиска")
            return

        url = f"https://api.github.com/search/repositories?q={query}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                repos = data.get('items', [])

                self.search_text.delete(1.0, tk.END)
                self.search_text.insert(tk.END, f"Найдено репозиториев: {data.get('total_count', 0)}\n")
                self.search_text.insert(tk.END, "=" * 50 + "\n")

                for repo in repos[:5]:  # Показываем первые 5
                    self.search_text.insert(tk.END, f"\nНазвание: {repo['name']}\n")
                    self.search_text.insert(tk.END, f"Автор: {repo['owner']['login']}\n")
                    self.search_text.insert(tk.END, f"Ссылка: {repo['html_url']}\n")
                    self.search_text.insert(tk.END, f"Описание: {repo.get('description', 'Нет описания')}\n")
                    self.search_text.insert(tk.END, f"Язык: {repo.get('language', 'Не указан')}\n")
                    self.search_text.insert(tk.END, f"Звёзд: {repo.get('stargazers_count', 0)}\n")
                    self.search_text.insert(tk.END, "-" * 30 + "\n")
            else:
                messagebox.showerror("Ошибка", "Ошибка при поиске")
        except:
            messagebox.showerror("Ошибка", "Ошибка подключения к API")


root = tk.Tk()
app = GitHubApp(root)
root.mainloop()