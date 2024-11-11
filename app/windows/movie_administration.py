import tkinter as tk
from learn.app.create_app import App
from tkinter import LabelFrame, messagebox
from tkinter import ttk

from learn.app.database.requests import Movie
from learn.app.system.movie_named import MovieNamed


class MovieAdministration:

    def __init__(self, root: App) -> None:
        self.movie_frame: LabelFrame = None
        self.movie_name_entry = None
        self.movie_description_text = None
        self.movie_table_frame = None
        self.movie_treeview = None

        self.put_frame_movie(root)
        self.put_ui_movie()
        self.put_table_movie()

        self.update_movie_table()
        self.update_movie_dropdown()
        self.delete_form_movie()

    def put_frame_movie(self, root: App) -> None:
        self.movie_frame = LabelFrame(root, text="Добавление фильма", padx=10, pady=10)
        self.movie_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.movie_table_frame = tk.LabelFrame(root, text="Фильмы", padx=10, pady=10)
        self.movie_table_frame.grid(row=1, column=0, padx=10, pady=10)


    def put_ui_movie(self) -> None:
        movie_name_label = tk.Label(self.movie_frame, text="Название фильма:")
        movie_name_label.grid(row=0, column=0, sticky="w")
        self.movie_name_entry = tk.Entry(self.movie_frame, width=67)
        self.movie_name_entry.grid(row=0, column=1)

        movie_description_label = tk.Label(self.movie_frame, text="Описание фильма:")
        movie_description_label.grid(row=1, column=0, sticky="w")
        self.movie_description_text = tk.Text(self.movie_frame, height=5, width=50)
        self.movie_description_text.grid(row=1, column=1, pady=5)

        add_movie_button = tk.Button(self.movie_frame, text="Добавить фильм", command=self.add_movie, width=14)
        add_movie_button.grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        update_movie_button = tk.Button(self.movie_frame, text="Редактировать фильм", command=self.update_movie, width=18)
        update_movie_button.grid(row=2, column=1, sticky="nw", padx=5, pady=5)
        deleted_movie_button = tk.Button(self.movie_frame, text="Удалить фильм", command=self.delete_movie, width=14)
        deleted_movie_button.grid(row=3, column=0, sticky="sw", padx=5, pady=5)
        update_movie_button = tk.Button(self.movie_frame, text="Отменить выбор", command=self.canceled_select_movie, width=18)
        update_movie_button.grid(row=3, column=1, sticky="sw", padx=5, pady=5)

    def put_table_movie(self) -> None:
        movie_columns = ["ID", "Название фильма", "Описание фильма"]

        self.movie_treeview = ttk.Treeview(self.movie_table_frame, columns=movie_columns, show="headings")
        self.movie_treeview.bind("<<TreeviewSelect>>", self.on_item_select_movie)

        for movie_column in movie_columns:
            self.movie_treeview.heading(movie_column, text=movie_column)

        self.movie_treeview.pack(fill="both", expand=True)


    def add_movie(self) -> None:
        select_item = self.movie_treeview.selection()
        if select_item:
            messagebox.showwarning("Ошибка", "Вы не можете добавить данный фильм повторно")
        else:
            movie_name = self.movie_name_entry.get()
            movie_description = self.movie_description_text.get("1.0", tk.END).strip()  # Получаем описание
            if movie_name:
                Movie.add_movie(movie_name, movie_description)
                self.update_movie_table()
                self.update_movie_dropdown()
                self.delete_form_movie()
            else:
                messagebox.showwarning("Ошибка", "Введите название фильма")

    def update_movie(self) -> None:
        selected_item = self.movie_treeview.selection()
        if selected_item:
            movie_id = self.movie_treeview.item(selected_item)['values'][0]
            movie_name = self.movie_name_entry.get()
            movie_description = self.movie_description_text.get("1.0", tk.END).strip()

            if movie_name and movie_description:
                Movie.update_movie(movie_id, movie_name, movie_description)
                self.update_movie_table()
                self.update_movie_dropdown()
                self.delete_form_movie()
            else:
                messagebox.showwarning("Ошибка", "Заполните все поля")
        else:
            messagebox.showwarning("Ошибка", "Вы не можете редактировать не выбранный фильм")

    def delete_movie(self) -> None:
        selected_item =self. movie_treeview.selection()
        if selected_item:
            movie_id = self.movie_treeview.item(selected_item)['values'][0]
            movie_name = self.movie_treeview.item(selected_item)['values'][1]
            movies = Movie.get_all_movie()
            for movie in movies:
                if movie.name == movie_name and movie.number_movie == movie_id:
                    Movie.del_movie(movie_name, movie_id)
            self.update_movie_table()
            self.update_movie_dropdown()
        else:
            messagebox.showwarning("Ошибка", "Выберите фильм для удаления")

    def canceled_select_movie(self) -> None:
        self.delete_form_movie()
        self.update_movie_table()

    def delete_form_movie(self) -> None:
        self.movie_name_entry.delete(0, tk.END)
        self.movie_description_text.delete("1.0", tk.END)

    def update_movie_table(self) -> None:
        movies = Movie.get_all_movie()
        for row in self.movie_treeview.get_children():
            self.movie_treeview.delete(row)
        for movie in movies:
            self.movie_treeview.insert("", "end", values=(movie.number_movie, movie.name, movie.description))

    def on_item_select_movie(self, event) -> None:
        select_item = self.movie_treeview.selection()
        if select_item:
            self.delete_form_movie()

            self.movie_name_entry.insert(0, self.movie_treeview.item(select_item)['values'][1])
            self.movie_description_text.insert("1.0", self.movie_treeview.item(select_item)['values'][2])

    @staticmethod
    def update_movie_dropdown() -> None:
        MovieNamed.del_named_movie()
        movies = Movie.get_all_movie()
        for movie in movies:
            MovieNamed.set_named_movie(movie.name)
