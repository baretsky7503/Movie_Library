import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Файл для хранения фильмов
        self.data_file = "movies.json"
        self.movies = self.load_movies()

        # Создание интерфейса
        self.create_input_frame()
        self.create_table_frame()
        self.create_filter_frame()

        # Обновление таблицы
        self.refresh_table()

    def load_movies(self):
        """Загрузка фильмов из JSON-файла"""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_movies(self):
        """Сохранение фильмов в JSON-файл"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, indent=4, ensure_ascii=False)

    def create_input_frame(self):
        """Форма для добавления фильма"""
        input_frame = tk.LabelFrame(self.root, text="Добавление фильма", font=("Arial", 12, "bold"), padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Название
        tk.Label(input_frame, text="Название:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Жанр
        tk.Label(input_frame, text="Жанр:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.genre_entry = tk.Entry(input_frame, width=20, font=("Arial", 10))
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)

        # Год выпуска
        tk.Label(input_frame, text="Год выпуска:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.year_entry = tk.Entry(input_frame, width=10, font=("Arial", 10))
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)

        # Рейтинг
        tk.Label(input_frame, text="Рейтинг (0-10):", font=("Arial", 10)).grid(row=1, column=2, sticky="w", padx=5,
                                                                               pady=5)
        self.rating_entry = tk.Entry(input_frame, width=10, font=("Arial", 10))
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка добавления
        self.add_btn = tk.Button(input_frame, text="➕ Добавить фильм", command=self.add_movie, bg="#2c3e50", fg="white",
                                 font=("Arial", 10, "bold"))
        self.add_btn.grid(row=0, column=4, rowspan=2, padx=20, pady=5)

    def create_table_frame(self):
        """Таблица для отображения фильмов"""
        table_frame = tk.LabelFrame(self.root, text="Список фильмов", font=("Arial", 12, "bold"), padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создание таблицы (Treeview)
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        # Настройка заголовков
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")

        # Настройка ширины колонок
        self.tree.column("Название", width=300)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=80)
        self.tree.column("Рейтинг", width=80)

        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления (удаление)
        btn_frame = tk.Frame(table_frame)
        btn_frame.pack(fill="x", pady=5)

        self.delete_btn = tk.Button(btn_frame, text="🗑 Удалить выбранный фильм", command=self.delete_movie,
                                    bg="#e74c3c", fg="white", font=("Arial", 10))
        self.delete_btn.pack(side="left", padx=5)

    def create_filter_frame(self):
        """Фильтрация фильмов"""
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", font=("Arial", 12, "bold"), padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по жанру
        tk.Label(filter_frame, text="Фильтр по жанру:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre_entry = tk.Entry(filter_frame, width=20, font=("Arial", 10))
        self.filter_genre_entry.grid(row=0, column=1, padx=5, pady=5)

        self.filter_genre_btn = tk.Button(filter_frame, text="Применить", command=self.filter_movies, bg="#3498db",
                                          fg="white", font=("Arial", 9))
        self.filter_genre_btn.grid(row=0, column=2, padx=5, pady=5)

        # Фильтр по году
        tk.Label(filter_frame, text="Фильтр по году:", font=("Arial", 10)).grid(row=0, column=3, padx=5, pady=5)
        self.filter_year_entry = tk.Entry(filter_frame, width=10, font=("Arial", 10))
        self.filter_year_entry.grid(row=0, column=4, padx=5, pady=5)

        self.filter_year_btn = tk.Button(filter_frame, text="Применить", command=self.filter_movies, bg="#3498db",
                                         fg="white", font=("Arial", 9))
        self.filter_year_btn.grid(row=0, column=5, padx=5, pady=5)

        # Кнопка сброса фильтров
        self.reset_btn = tk.Button(filter_frame, text="🔄 Сбросить фильтры", command=self.reset_filters, bg="#95a5a6",
                                   fg="white", font=("Arial", 9))
        self.reset_btn.grid(row=0, column=6, padx=20, pady=5)

    def validate_movie_data(self, title, genre, year, rating):
        """Проверка корректности ввода"""
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр не могут быть пустыми!")
            return False

        try:
            year_int = int(year)
            if year_int < 1888 or year_int > 2026:  # Первый фильм появился в 1888 году
                messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2026!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть целым числом!")
            return False

        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return False

        return True

    def add_movie(self):
        """Добавление фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        if not self.validate_movie_data(title, genre, year, rating):
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": float(rating)
        }

        self.movies.append(movie)
        self.save_movies()
        self.refresh_table()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", f"Фильм \"{title}\" добавлен!")

    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите фильм для удаления!")
            return

        # Получаем название фильма из выделенной строки
        item = self.tree.item(selected[0])
        title = item['values'][0]

        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", f"Удалить фильм \"{title}\"?"):
            # Удаляем из списка
            self.movies = [m for m in self.movies if m['title'] != title]
            self.save_movies()
            self.refresh_table()
            messagebox.showinfo("Успех", "Фильм удалён!")

    def filter_movies(self):
        """Применение фильтров"""
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter = self.filter_year_entry.get().strip()

        filtered = self.movies.copy()

        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m['genre'].lower()]

        if year_filter:
            try:
                year_int = int(year_filter)
                filtered = [m for m in filtered if m['year'] == year_int]
            except ValueError:
                messagebox.showerror("Ошибка", "Год для фильтрации должен быть числом!")
                return

        self.display_movies(filtered)

    def reset_filters(self):
        """Сброс фильтров"""
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы (без фильтров)"""
        self.display_movies(self.movies)

    def display_movies(self, movies_list):
        """Отображение фильмов в таблице"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Добавление фильмов
        for movie in movies_list:
            self.tree.insert("", "end", values=(
                movie['title'],
                movie['genre'],
                movie['year'],
                movie['rating']
            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()