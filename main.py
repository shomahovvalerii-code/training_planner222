import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Личная кинотека")
        self.root.geometry("900x650")
        
        self.data_file = "movie_library.json"
        self.movies = []  # список словарей: title, genre, year, rating
        
        # Предопределённые жанры для удобства
        self.genres = [
            "Боевик", "Вестерн", "Детектив", "Документальный",
            "Драма", "Исторический", "Комедия", "Мелодрама",
            "Мюзикл", "Приключения", "Триллер", "Ужасы", "Фантастика", "Фэнтези"
        ]
        
        self.load_data()
        self.create_widgets()
        self.display_movies()
    
    # ------------------ Работа с данными ------------------
    def load_data(self):
        """Загрузка списка фильмов из JSON-файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.movies = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить данные: {e}")
                self.movies = []
    
    def save_data(self):
        """Сохранение списка фильмов в JSON-файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")
    
    # ------------------ GUI ------------------
    def create_widgets(self):
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # --- Блок добавления фильма ---
        add_frame = ttk.LabelFrame(main_frame, text="Добавить фильм", padding=10)
        add_frame.pack(fill="x", pady=5)
        
        # Название
        ttk.Label(add_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = ttk.Entry(add_frame, width=25)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Жанр (комбобокс с возможностью ручного ввода)
        ttk.Label(add_frame, text="Жанр:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.genre_var = tk.StringVar()
        self.genre_combo = ttk.Combobox(add_frame, textvariable=self.genre_var, 
                                        values=self.genres, width=22)
        self.genre_combo.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Год выпуска
        ttk.Label(add_frame, text="Год выпуска:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.year_entry = ttk.Entry(add_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Рейтинг
        ttk.Label(add_frame, text="Рейтинг (0-10):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.rating_entry = ttk.Entry(add_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        # Кнопка добавления
        add_btn = ttk.Button(add_frame, text="Добавить фильм", command=self.add_movie)
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        # --- Блок фильтрации ---
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", pady=5)
        
        # По жанру
        ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.filter_genre_var = tk.StringVar(value="Все")
        self.filter_genre_combo = ttk.Combobox(filter_frame, textvariable=self.filter_genre_var,
                                               values=["Все"] + self.genres, width=22, state="readonly")
        self.filter_genre_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # По году (диапазон)
        ttk.Label(filter_frame, text="Год от:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.filter_year_from = ttk.Entry(filter_frame, width=8)
        self.filter_year_from.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        ttk.Label(filter_frame, text="до:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.filter_year_to = ttk.Entry(filter_frame, width=8)
        self.filter_year_to.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        
        # Кнопки
        filter_btn = ttk.Button(filter_frame, text="Применить", command=self.apply_filters)
        filter_btn.grid(row=0, column=6, padx=10, pady=5)
        
        reset_btn = ttk.Button(filter_frame, text="Сбросить", command=self.reset_filters)
        reset_btn.grid(row=0, column=7, padx=5, pady=5)
        
        # --- Таблица фильмов ---
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=5)
        
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        
        self.tree.column("title", width=300)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=80, anchor="center")
        self.tree.column("rating", width=80, anchor="center")
        
        # Скроллбары
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Кнопки управления записями
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill="x", pady=5)
        
        delete_btn = ttk.Button(control_frame, text="Удалить выбранный фильм", command=self.delete_movie)
        delete_btn.pack(side="left", padx=5)
        
        # Загружаем все фильмы в таблицу
        self.display_movies()
    
    # ------------------ Валидация ------------------
    def validate_input(self, title, genre, year_str, rating_str):
        """Проверка корректности введённых данных"""
        errors = []
        
        if not title.strip():
            errors.append("Название не может быть пустым.")
        if not genre.strip():
            errors.append("Жанр не может быть пустым.")
        
        # Проверка года
        try:
            year = int(year_str)
            if year < 1888 or year > 2100:
                errors.append("Год должен быть в диапазоне 1888–2100.")
        except ValueError:
            errors.append("Год должен быть целым числом.")
        
        # Проверка рейтинга
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                errors.append("Рейтинг должен быть от 0 до 10.")
        except ValueError:
            errors.append("Рейтинг должен быть числом (например, 8.5).")
        
        return errors
    
    # ------------------ Действия ------------------
    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_var.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()
        
        errors = self.validate_input(title, genre, year_str, rating_str)
        if errors:
            messagebox.showerror("Ошибка ввода", "\n".join(errors))
            return
        
        year = int(year_str)
        rating = float(rating_str)
        
        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        
        self.movies.append(movie)
        self.save_data()
        self.display_movies()
        self.clear_add_fields()
        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")
    
    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления.")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        title, genre, year, rating = values[0], values[1], int(values[2]), float(values[3])
        
        # Удаляем из списка
        for i, movie in enumerate(self.movies):
            if (movie['title'] == title and movie['genre'] == genre and 
                movie['year'] == year and movie['rating'] == rating):
                del self.movies[i]
                break
        
        self.save_data()
        self.display_movies()
        messagebox.showinfo("Успех", f"Фильм '{title}' удалён.")
    
    def apply_filters(self):
        """Применение фильтров и обновление таблицы"""
        self.display_movies()
    
    def reset_filters(self):
        """Сброс фильтров и отображение всех фильмов"""
        self.filter_genre_var.set("Все")
        self.filter_year_from.delete(0, tk.END)
        self.filter_year_to.delete(0, tk.END)
        self.display_movies()
    
    def get_filtered_movies(self):
        """Возвращает список фильмов, соответствующих фильтрам"""
        filtered = self.movies.copy()
        
        # Фильтр по жанру
        genre_filter = self.filter_genre_var.get()
        if genre_filter and genre_filter != "Все":
            filtered = [m for m in filtered if m['genre'].lower() == genre_filter.lower()]
        
        # Фильтр по диапазону годов
        from_str = self.filter_year_from.get().strip()
        to_str = self.filter_year_to.get().strip()
        
        if from_str:
            try:
                year_from = int(from_str)
                filtered = [m for m in filtered if m['year'] >= year_from]
            except ValueError:
                pass  # игнорируем некорректный ввод
        
        if to_str:
            try:
                year_to = int(to_str)
                filtered = [m for m in filtered if m['year'] <= year_to]
            except ValueError:
                pass
        
        return filtered
    
    def display_movies(self):
        """Заполнение таблицы отфильтрованными данными"""
        # Очистка
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        movies_to_show = self.get_filtered_movies()
        # Сортировка по году (новые сверху), затем по названию
        movies_to_show.sort(key=lambda x: (-x['year'], x['title']))
        
        for movie in movies_to_show:
            self.tree.insert("", "end", values=(
                movie['title'],
                movie['genre'],
                movie['year'],
                movie['rating']
            ))
    
    def clear_add_fields(self):
        """Очистка полей ввода после добавления"""
        self.title_entry.delete(0, tk.END)
        self.genre_var.set("")
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()