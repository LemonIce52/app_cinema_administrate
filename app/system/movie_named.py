class MovieNamed:
    named_movie = []

    @classmethod
    def get_name_movie(cls) -> list[str]:
        return cls.named_movie

    @classmethod
    def set_named_movie(cls, name_movie: str) -> None:
        cls.named_movie.append(name_movie)

    @classmethod
    def del_named_movie(cls) -> None:
        cls.named_movie = []
