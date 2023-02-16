from demostration_solution.dao.model.movie import Movie
from demostration_solution.dao.movie import MovieDAO
from demostration_solution.service.movie import MovieService
from demostration_solution.setup_db import db

from unittest.mock import MagicMock
import pytest


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    director1 = Movie(
        id=1,
        title="Alice in Wonderland",
        description="test",
        trailer="test",
        year=1997,
        rating=4.5,
        genre_id=1,
        director_id=1
    )
    director2 = Movie(
        id=2,
        title="Groundhog Day",
        description="test",
        trailer="test",
        year=1998,
        rating=4.5,
        genre_id=2,
        director_id=2
    )
    director3 = Movie(
        id=3,
        title="The Adams Family",
        description="test",
        trailer="test",
        year=1999,
        rating=4.5,
        genre_id=3,
        director_id=3
    )

    movie_dao.get_one = MagicMock(return_value=director1)
    movie_dao.get_all = MagicMock(return_value=[director1, director2, director3])
    movie_dao.create = MagicMock(return_value=Movie(
        id=3,
        title="The Adams Family",
        description="test",
        trailer="test",
        year=2000,
        rating=4.5,
        genre_id=3,
        director_id=3
    ))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id == 1
        assert movie.title == "Alice in Wonderland"

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) == 3
        assert len(movies) > 0

    def test_create(self):
        data = {
            "title": "The Adams Family",
            "description": "test",
            "trailer": "test",
            "year": 1999,
            "rating": 4.5,
            "genre_id": 3,
            "director_id": 3
        }
        movie = self.movie_service.create(data)

        assert movie.title == data["title"]

    def test_delete(self):
        del_movie = self.movie_service.delete(1)

        assert del_movie is None

    def test_update(self):
        data = {
            "id": 3,
            "title": "test"
        }
        self.movie_service.update(data)
