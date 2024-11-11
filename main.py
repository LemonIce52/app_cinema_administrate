from learn.app.create_app import App
from learn.app.database.database import db_main
from learn.app.windows.movie_administration import MovieAdministration
from learn.app.windows.session_administration import SessionAdministration

if __name__ == "__main__":
    db_main()
    root = App()
    movie = MovieAdministration(root)
    session = SessionAdministration(root)
    root.mainloop()
