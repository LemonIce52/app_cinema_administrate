from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import ForeignKey, create_engine


engine = create_engine(url='sqlite:///learn/app/database/db.sqlite3')

session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass

class Movies(Base):
    __tablename__ = 'Movie'

    number_movie: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()


class Sessions(Base):
    __tablename__ = 'Session'

    number_session: Mapped[int] = mapped_column(primary_key=True)
    id_movie: Mapped[int] = mapped_column(ForeignKey('Movie.number_movie'))
    count_seat: Mapped[int] = mapped_column(default=100)
    count_ticket: Mapped[int] = mapped_column(default=0)
    time_start: Mapped[str] = mapped_column()
    time_end: Mapped[str] = mapped_column()
    date: Mapped[str] = mapped_column()



def db_main():
    with engine.begin() as conn:
        Base.metadata.create_all(conn)

