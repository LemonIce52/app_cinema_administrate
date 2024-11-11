import tkinter as tk
from learn.app.create_app import App
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry, Calendar
from datetime import datetime, timedelta

from learn.app.database.requests import Session, Movie
from learn.app.system.movie_named import MovieNamed


class SessionAdministration:

    def __init__(self, root: App) -> None:
        self.session_frame = None
        self.session_table_frame = None
        self.calendar = None
        self.calendar_frame = None
        self.date_combobox = None
        self.session_treeview = None
        self.time_end_dropdown = None
        self.time_start_dropdown = None
        self.movie_dropdown = None
        self.count_seat_session_entry = None

        self.put_frame_session(root)
        self.put_table_session()
        self.put_ui_create_session()

        self.update_session_table()
        self.delite_form_session()

    def put_frame_session(self, root: App) -> None:
        self.session_frame = tk.LabelFrame(root, text="Добавление сеанса", padx=10, pady=10)
        self.session_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.session_table_frame = tk.LabelFrame(root, text="Сеансы", padx=10, pady=10)
        self.session_table_frame.grid(row=1, column=1, padx=10, pady=10)

    def put_ui_create_session(self) -> None:
        session_movie_label = tk.Label(self.session_frame, text="Выберите фильм:")
        session_movie_label.grid(row=0, column=0, sticky="w", pady=5)

        add_session_button = tk.Button(self.session_frame, text="Добавить сеанс", command=self.add_session, width=14)
        add_session_button.grid(row=5, column=0, sticky="nw", padx=5, pady=5)
        delete_movie_button = tk.Button(self.session_frame, text="Удалить сеанс", command=self.delete_session, width=14)
        delete_movie_button.grid(row=6, column=0, sticky="nw", padx=5, pady=5)
        delete_movie_button = tk.Button(self.session_frame, text="Редактировать сеанс", command=self.update_session, width=18)
        delete_movie_button.grid(row=5, column=1, sticky="sw", padx=5, pady=5)
        delete_movie_button = tk.Button(self.session_frame, text="Отменить выбор", command=self.cancel_select_session, width=18)
        delete_movie_button.grid(row=6, column=1, sticky="sw", padx=5, pady=5)

        self.movie_dropdown = ttk.Combobox(self.session_frame, values=MovieNamed.get_name_movie())
        self.movie_dropdown.grid(row=0, column=1, pady=5)

        self.movie_dropdown.bind('<<ComboboxSelected>>', self.on_combobox_select)
        self.movie_dropdown.bind('<Button-1>', self.on_combox_open)

        session_date_label = tk.Label(self.session_frame, text="Дата:")
        session_date_label.grid(row=1, column=0, sticky="w", pady=5)


        self.date_combobox = DateEntry(self.session_frame, date_pattern="y-mm-dd", width=20)
        self.date_combobox.grid(row=1, column=1, pady=5)

        session_time_label = tk.Label(self.session_frame, text="Время:")
        session_time_label.grid(row=2, column=0, sticky="w", pady=5)

        available_times = [
            f"{hour:02d}:{minute:02d}"
            for hour in range(24)
            for minute in (0, 30)
        ]
        self.time_start_dropdown = ttk.Combobox(self.session_frame, values=available_times, state="readonly")
        self.time_start_dropdown.grid(row=2, column=1, pady=5)

        session_end_time_label = tk.Label(self.session_frame, text="Время окончания:")
        session_end_time_label.grid(row=3, column=0, sticky="w", pady=5)

        self.time_end_dropdown = ttk.Combobox(self.session_frame, values=available_times, state="readonly")
        self.time_end_dropdown.grid(row=3, column=1, pady=5)

        count_seat_session_label = tk.Label(self.session_frame, text="Количество мест (число):")
        count_seat_session_label.grid(row=4, column=0, pady=5)
        self.count_seat_session_entry = tk.Entry(self.session_frame, width=23)
        self.count_seat_session_entry.grid(row=4, column=1, pady=5)

    def select_date(self) -> None:
        selected_date = self.calendar.get_date()
        self.date_combobox.set(selected_date)
        self.calendar_frame.place_forget()

    def put_table_session(self) -> None:
        sessions_columns = ["ID", "Фильм", "Дата и время", "Количество мест", "Продано билетов"]

        self.session_treeview = ttk.Treeview(self.session_table_frame, columns=sessions_columns, show="headings")

        for column in sessions_columns:
            self.session_treeview.heading(column, text=column)

        self.session_treeview.pack(fill="both", expand=True)
        self.session_treeview.bind("<<TreeviewSelect>>", self.on_item_selected_session)

    def delete_session(self) -> None:
        selected_item = self.session_treeview.selection()
        if selected_item:
            session_id = self.session_treeview.item(selected_item)['values'][0]
            sessions = Session.get_all_session()
            for session in sessions:
                if session.number_session == session_id:
                    Session.del_session(session_id)
                    self.update_session_table()
        else:
            messagebox.showwarning("Ошибка", "Выберите сессию для удаления")

    def add_session(self) -> None:
        selected_item = self.session_treeview.selection()
        if selected_item:
            messagebox.showwarning("Ошибка", "Вы не можете повторно добавить выбранный фильм")
        else:
            movie_name = self.movie_dropdown.get()
            session_date = self.date_combobox.get()
            session_start_time = self.time_start_dropdown.get()
            session_end_time = self.time_end_dropdown.get()
            session_count_seat = self.count_seat_session_entry.get()

            if movie_name and session_date and session_start_time and session_end_time:
                try:
                    count_seat = int(session_count_seat)
                    start_datetime = datetime.strptime(f"{session_date} {session_start_time}", "%Y-%m-%d %H:%M")
                    end_datetime = datetime.strptime(f"{session_date} {session_end_time}", "%Y-%m-%d %H:%M")

                    if end_datetime <= start_datetime:
                        raise ValueError("Время окончания не может быть меньше или равно времени начала.")

                    if end_datetime - start_datetime <= timedelta(minutes=30):
                        raise ValueError("Время окончания должно быть не менее чем через 30 минут после начала.")

                    data_movie = Movie.get_movie_for_name(movie_name)
                    Session.session_add(data_movie.number_movie, session_date, session_start_time, session_end_time, 0,
                                        count_seat)
                    self.update_session_table()
                    self.delite_form_session()
                except ValueError as e:
                    messagebox.showwarning("Ошибка", str(e))
            else:
                messagebox.showwarning("Ошибка", "Заполните все поля")

    def update_session(self) -> None:
        selected_item = self.session_treeview.selection()
        if selected_item:
            movie_name = self.movie_dropdown.get()
            session_date = self.date_combobox.get()
            session_start_time = self.time_start_dropdown.get()
            session_end_time = self.time_end_dropdown.get()
            session_count_seat = self.count_seat_session_entry.get()

            if movie_name and session_date and session_start_time and session_end_time:
                try:
                    count_seat = int(session_count_seat)
                    start_datetime = datetime.strptime(f"{session_date} {session_start_time}", "%Y-%m-%d %H:%M")
                    end_datetime = datetime.strptime(f"{session_date} {session_end_time}", "%Y-%m-%d %H:%M")

                    if end_datetime <= start_datetime:
                        raise ValueError("Время окончания не может быть меньше или равно времени начала.")

                    session_id = self.session_treeview.item(selected_item)['values'][0]
                    movie = Movie.get_movie_for_name(movie_name)
                    Session.update_session(session_id, movie.number_movie, session_date, session_start_time,
                                           session_end_time, count_seat)
                    self.update_session_table()
                    self.delite_form_session()
                except ValueError as e:
                    messagebox.showwarning("Ошибка", str(e))
            else:
                messagebox.showwarning("Ошибка", "Заполните все поля")
        else:
            messagebox.showwarning("Ошибка", "Вы не можете редактировать не выбранную сессию")

    def update_session_table(self) -> None:
        for row in self.session_treeview.get_children():
            self.session_treeview.delete(row)

        data_sessions = Session.get_all_session()
        self.session_table_insert(data_sessions)

    def on_item_selected_session(self, event) -> None:
        selected_item = self.session_treeview.selection()
        if selected_item:
            self.delite_form_session()

            session_date = self.session_treeview.item(selected_item)['values'][2]
            self.movie_dropdown.insert("", self.session_treeview.item(selected_item)['values'][1])
            self.date_combobox.set(session_date.split(' ')[0])
            time = session_date.split(' ')[1]
            self.time_start_dropdown.set(time.split('-')[0])
            self.time_end_dropdown.set(time.split('-')[1])
            self.count_seat_session_entry.insert(0, self.session_treeview.item(selected_item)['values'][3])

    def on_combobox_select(self, event) -> None:
        selected_movie = self.movie_dropdown.get()
        if selected_movie:
            for row in self.session_treeview.get_children():
                self.session_treeview.delete(row)

            data_movie = Movie.get_movie_for_name(selected_movie)
            data_sessions = Session.get_session_for_movie(data_movie.number_movie)
            self.session_table_insert(data_sessions)

    def session_table_insert(self, data_sessions: list) -> None:
        for session in data_sessions:
            movie_name = Movie.get_movie_name_for_id(session.id_movie)
            session_date_and_time = f"{session.date} {session.time_start}-{session.time_end}"
            self.session_treeview.insert("", "end", values=(session.number_session, movie_name,
                                                       session_date_and_time, session.count_seat, session.count_ticket
                                                       ))

    def cancel_select_session(self) -> None:
        self.delite_form_session()
        self.update_session_table()

    def delite_form_session(self) -> None:
        self.movie_dropdown.delete(0, tk.END)
        self.date_combobox.delete(0, tk.END)
        self.time_start_dropdown.delete(0, tk.END)
        self.time_end_dropdown.delete(0, tk.END)
        self.count_seat_session_entry.delete(0, tk.END)

    def on_combox_open(self, event) -> None:
        self.movie_dropdown['values'] = MovieNamed.get_name_movie()

