from demostration_solution.dao.director import DirectorDAO
from demostration_solution.dao.model.director import Director
from demostration_solution.service.director import DirectorService
from demostration_solution.setup_db import db

from unittest.mock import MagicMock
import pytest


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    director1 = Director(id=1, name="Jonh")
    director2 = Director(id=2, name="Kate")
    director3 = Director(id=3, name="Max")

    director_dao.get_one = MagicMock(return_value=director1)
    director_dao.get_all = MagicMock(return_value=[director1, director2, director3])
    director_dao.create = MagicMock(return_value=Director(id=3, name="Ric"))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id == 1

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) == 3
        assert len(directors) > 0

    def test_create(self):
        data = {
            "name": "Ric"
        }
        director = self.director_service.create(data)

        assert director.name == data["name"]

    def test_delete(self):
        del_director = self.director_service.delete(1)

        assert del_director is None

    def test_update(self):
        data = {
            "id": 3,
            "name": "Jack"
        }
        self.director_service.update(data)
