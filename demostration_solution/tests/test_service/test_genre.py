from demostration_solution.dao.genre import GenreDAO
from demostration_solution.dao.model.genre import Genre
from demostration_solution.service.genre import GenreService
from demostration_solution.setup_db import db

from unittest.mock import MagicMock
import pytest


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)

    genre1 = Genre(id=1, name="Comedy")
    genre2 = Genre(id=2, name="Action")
    genre3 = Genre(id=3, name="Drama")

    genre_dao.get_one = MagicMock(return_value=genre1)
    genre_dao.get_all = MagicMock(return_value=[genre1, genre2, genre3])
    genre_dao.create = MagicMock(return_value=Genre(id=3, name="Western"))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def director_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert genre.id == 1

    def test_get_all(self):
        genres = self.genre_service.get_all()

        assert len(genres) == 3
        assert len(genres) > 0

    def test_create(self):
        data = {
            "name": "Western"
        }
        genre = self.genre_service.create(data)

        assert genre.name == data["name"]

    def test_delete(self):
        del_genre = self.genre_service.delete(1)

        assert del_genre is None

    def test_update(self):
        data = {
            "id": 3,
            "name": "Western"
        }
        self.genre_service.update(data)
