from tkinter import Tk

class App(Tk):
    def __init__(self):
        super().__init__()
        super().title("Кинотеатр: Управление фильмами и сеансами")
        super().resizable(height=False, width=False)