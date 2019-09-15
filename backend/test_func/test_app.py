from http import HTTPStatus
import json
from flask import url_for
import pytest
from app.extensions import db
from app.models import Text


@pytest.mark.usefixtures("client_class")
class TestEndpointSendTextAPI:
    @pytest.fixture(autouse=True)
    def data_remove_db_test(self):
        db.session.query(Text).delete()

    def test_endpoint_send_text_with_valid_data(self, client):
        data = {"text": "new text to server"}
        rv = client.post(url_for("api.send_text_api"), data=json.dumps(data))

        assert rv.status_code == HTTPStatus.CREATED
        assert rv.get_json()["text"] == data["text"]

        assert rv.get_json().get("id", None) is not None

    def test_endpoint_send_text_without_valid_data(self, client):
        data = {"otherfiled": "new text to server"}
        rv = client.post(url_for("api.send_text_api"), data=json.dumps(data))

        assert rv.status_code == HTTPStatus.BAD_REQUEST

        assert rv.get_json() == {"text": ["Missing data for required field."]}

    def test_check_methods(self, client):
        rv = client.get(url_for("api.send_text_api"))
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        rv = client.put(url_for("api.send_text_api"))
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        rv = client.delete(url_for("api.send_text_api"))
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        rv = client.patch(url_for("api.send_text_api"))
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.usefixtures("client_class")
class TestIsolatedVocabularyAPI:
    @pytest.fixture(autouse=True)
    def data_remove_db_test(self):
        db.session.query(Text).delete()

    def test_check_methods(self, client):
        rv = client.post(url_for("api.isolated_vocabulary_api"))
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        rv = client.put(url_for("api.isolated_vocabulary_api"))
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        rv = client.delete(url_for("api.isolated_vocabulary_api"))
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        rv = client.patch(url_for("api.isolated_vocabulary_api"))
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_get_vocabulary_with_zero_texts(self, client):
        response = client.get(url_for("api.isolated_vocabulary_api"))
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"vocabulary": []}

    def test_get_vocabulary_with_one_text(self, client):
        text = Text()
        text.text = "Just a simple text"
        db.session.add(text)
        db.session.commit()

        response = client.get(url_for("api.isolated_vocabulary_api"))
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"vocabulary": ["just", "simple", "text"]}

    def test_get_vocabulary_with_multiple_text(self, client):
        text = Text()
        text.text = "Um simples teste"
        db.session.add(text)
        db.session.flush()

        text = Text()
        text.text = "Pytest é a melhor biblioteca de testes"
        db.session.add(text)
        db.session.flush()

        text = Text()
        text.text = "Eu estou utilizando Flask framework"
        db.session.add(text)
        db.session.flush()

        db.session.commit()

        response = client.get(url_for("api.isolated_vocabulary_api"))
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {
            "vocabulary": [
                "simples",
                "teste",
                "pytest",
                "melhor",
                "biblioteca",
                "testes",
                "estou",
                "utilizando",
                "flask",
                "framework",
            ]
        }


@pytest.mark.usefixtures("client_class")
class TestIsolatedFrequencyDistributionAPI:
    @pytest.fixture(autouse=True)
    def data_remove_db_test(self):
        db.session.query(Text).delete()

    def test_check_methods(self, client):
        response = client.post(url_for("api.isolated_frequency_distribution_api"))
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        response = client.put(url_for("api.isolated_frequency_distribution_api"))
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        response = client.delete(url_for("api.isolated_frequency_distribution_api"))
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        response = client.patch(url_for("api.isolated_frequency_distribution_api"))
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_get_frequency_distribution_with_zero_texts(self, client):
        response = client.get(url_for("api.isolated_frequency_distribution_api"))
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"frequency": {}}

    def test_get_frequency_distribution_one_texts(self, client):
        text = Text()
        text.text = "Just a simple text"
        db.session.add(text)
        db.session.commit()

        response = client.get(url_for("api.isolated_frequency_distribution_api"))
        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {"frequency": {"text1": [1, 1, 1]}}

    def test_get_frequency_distribution_one_texts(self, client):
        text = Text()
        text.text = "Um simples teste"
        db.session.add(text)
        db.session.flush()

        text = Text()
        text.text = "Pytest Python é a melhor biblioteca de testes do Python"
        db.session.add(text)
        db.session.flush()

        text = Text()
        text.text = "Eu estou utilizando a linguagem Flask framework"
        db.session.add(text)
        db.session.flush()

        db.session.commit()

        response = client.get(url_for("api.isolated_frequency_distribution_api"))

        assert response.status_code == HTTPStatus.OK
        assert response.get_json() == {
            "frequency": {
                "text1": [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "text2": [0, 0, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0],
                "text3": [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            }
        }

