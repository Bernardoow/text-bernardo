import pytest
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError
from app.api_v1.schemas import (
    FrequenceDistributionField,
    FrequenceDistributionSchema,
    SendTextSchema,
    VocabularySchema,
)


class TestSendTextSchema:
    @pytest.fixture(autouse=True)
    def setUpAndTearDown(self):
        self.schema = SendTextSchema()

    def test_validate_should_throw_expectio_when_validate_wrong_data(self):
        with pytest.raises(ValidationError):
            data = {"country": "brazil"}
            self.schema.load(data)

    def test_validate_should_create_a_json_when_is_passed_a_valide_data(self):
        data = {"text": "brazil is cool"}
        new_data = self.schema.load(data)
        assert new_data == data

    def test_validate_should_create_a_json_when_is_passed_a_valide_field_and_invalid_field(self):
        data = {"text": "brazil is cool", "another": "cool"}
        new_data = self.schema.load(data)
        del data["another"]
        assert new_data == data

    def test_dump_should_create_a_json_with_id_and_text(self):
        data = {"text": "brazil is cool", "id": 2}
        new_data = self.schema.dump(data)
        assert data == new_data

    def test_dump_should_create_a_json_with_id_and_text_and_another_text(self):
        data = {"text": "brazil is cool", "id": 2, "another": "teste"}
        new_data = self.schema.dump(data)
        del data["another"]
        assert data == new_data


class TestVocabularySchema:
    @pytest.fixture(autouse=True)
    def setUpAndTearDown(self):
        self.schema = VocabularySchema()

    def test_should_be_instace_of_schema(self):
        assert isinstance(self.schema, Schema)

    def test_validate_should_throw_expectio_when_validate_wrong_data(self):
        with pytest.raises(ValidationError):
            data = {"country": "brazil"}
            self.schema.load(data)

    def test_dump_should_create_a_json_with_id_and_text(self):
        data = {"vocabulary": ["aab", "bab", "aa", "ab"]}
        new_data = self.schema.load(data)
        assert data == new_data

    def test_dump_should_create_a_json_with_only_field_represented_in_schema(self):
        data = {"vocabulary": ["aab", "bab", "aa", "ab"], "another": [1, 2, 3, 4]}

        new_data = self.schema.load(data)
        del data["another"]
        assert data == new_data


class TestFrequenceDistributionField:
    @pytest.fixture(autouse=True)
    def setUpAndTearDown(self):
        self.field = FrequenceDistributionField()

    def test_should_be_instace_of_schema(self):
        assert isinstance(self.field, fields.Field)

    def test_should_create_a_dict_empty_when_param_is_dict_empty(self):
        assert self.field.deserialize({}) == {}

    def test_should_check_if_every_value_in_dict_values_is_int(self):
        with pytest.raises(ValidationError):
            assert self.field.deserialize({"frequency": ["aab", "bab", "aa", "ab"]}) == {}

    def test_should_check_if_every_key_is_string(self):
        with pytest.raises(ValidationError):
            data = {1: [1, 2, 3], "text2": [5, 6, 7]}
            assert self.field.deserialize(data) == data

    def test_should_create_dict_with_key_string_and_values_int(self):
        data = {"text1": [1, 2, 3], "text2": [5, 6, 7]}
        assert self.field.deserialize(data) == data


class TestFrequenceDistributionSchemaSchema:
    @pytest.fixture(autouse=True)
    def setUpAndTearDown(self):
        self.schema = FrequenceDistributionSchema()

    def test_should_be_instace_of_schema(self):
        assert isinstance(self.schema, Schema)

    def test_validate_should_throw_exception_when_validate_wrong_data(self):
        with pytest.raises(ValidationError):
            data = {"country": "brazil"}
            self.schema.load(data)

    def test_validate_should_throw_exception_when_invalidate_data_is_in_frequency_field(self):
        with pytest.raises(ValidationError):
            data = {"frequency": ["aab", "bab", "aa", "ab"]}
            new_data = self.schema.load(data)
            assert data == new_data

    def test_load_should_create_a_json_with_validate_data(self):
        data = {"frequency": {"text1": [1, 2, 3], "text2": [5, 6, 7]}}
        new_data = self.schema.load(data)
        assert data == new_data
        data = {
            "frequency": {
                "text1": [1, 2, 3],
                "text2": [5, 6, 7],
                "text3": [5, 6, 7],
                "text4": [5, 6, 7],
            }
        }
        new_data = self.schema.load(data)
        assert data == new_data

    def test_load_should_throw_a_exception_invalid_dict__invalid_values(self):
        with pytest.raises(ValidationError):
            data = {"frequency": {"text1": [1, "2", 3], "text2": [5, 6, 7]}}
            new_data = self.schema.load(data)
            assert data == new_data
