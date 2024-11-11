from sqlalchemy import select, update

from .database import session, Movies, Sessions


class Movie:

    @classmethod
    def add_movie(cls, name: str, description: str) -> None:
        with session() as db:
            db.add(Movies(
                name=name,
                description=description
            ))

            db.commit()

    @classmethod
    def del_movie(cls, name: str, movie_id: int) -> None:
        with session() as db:
            delete_movie = db.scalar(select(Movies).where(Movies.name == name and Movies.number_movie == movie_id))

            if delete_movie:
                db.delete(delete_movie)
                db.commit()

    @classmethod
    def get_movie_for_name(cls, name: str) -> Movies:
        with session() as db:
            data = db.scalar(select(Movies).where(Movies.name == name))
            return data

    @classmethod
    def get_movie_name_for_id(cls, movie_id: int) -> Movies:
        with session() as db:
            data = db.scalar(select(Movies.name).where(Movies.number_movie == movie_id))
            return data

    @classmethod
    def get_all_movie(cls) -> list[Movies]:
        with session() as db:
            data_movie = db.scalars(select(Movies)).all()
            return data_movie

    @classmethod
    def update_movie(cls, movie_id: int, name: str, description: str) -> None:
        with session() as db:
            db.execute(update(Movies).where(Movies.number_movie == movie_id).values(name=name, description=description))
            db.commit()


class Session:

    @classmethod
    def session_add(cls, movie_id: int, date: str, time_start: str, time_end: str, count_ticket: int,
                    count_seat: int) -> None:
        with session() as db:
            db.add(Sessions(
                id_movie=movie_id,
                date=date,
                time_start=time_start,
                time_end=time_end,
                count_ticket=count_ticket,
                count_seat=count_seat
            ))
            db.commit()

    @classmethod
    def get_all_session(cls) -> list[Sessions]:
        with session() as db:
            data_session = db.scalars(select(Sessions)).all()
            return data_session

    @classmethod
    def del_session(cls, session_id: int) -> None:
        with session() as db:
            del_session = db.scalar(select(Sessions).where(Sessions.number_session == session_id))

            if del_session:
                db.delete(del_session)
                db.commit()

    @classmethod
    def get_session_for_movie(cls, movie_id: int) -> list[Sessions]:
        with session() as db:
            session_data = db.scalars(select(Sessions).where(Sessions.id_movie == movie_id)).all()
            return session_data

    @classmethod
    def update_session(cls, session_id: int, movie_id: int, date: str, time_start: str, time_end: str,
                       count_seat: int) -> None:
        with session() as db:
            db.execute(update(Sessions).where(Sessions.number_session == session_id).values(id_movie=movie_id,
                                                                                            date=date,
                                                                                            time_start=time_start,
                                                                                            time_end=time_end,
                                                                                            count_seat=count_seat))
            db.commit()
