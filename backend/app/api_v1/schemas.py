from marshmallow import Schema, fields, EXCLUDE


class SendTextSchema(Schema):
    id = fields.Int(dump_only=True)
    text = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE


class IsolatedVocabularySchema(Schema):
    vocabulary = fields.List(fields.String(), required=True)

    class Meta:
        unknown = EXCLUDE


class Gram2VocabularySchema(Schema):
    vocabulary = fields.List(fields.Tuple((fields.String(), fields.String())), required=True)

    class Meta:
        unknown = EXCLUDE


class FrequenceDistributionField(fields.Field):
    default_error_messages = {
        "invalid_type": "Every value inside dict must be int.",
        "invalid_dict": "This field must be a dict.",
    }
    """Field that deserializes dict string with values int
    """

    def _check_if_every_item_is_int(self, dict_string_int):
        if isinstance(dict_string_int, dict):
            for list_value in dict_string_int.values():
                if isinstance(list_value, list):
                    return all(map(lambda v: isinstance(v, int), list_value))
                else:
                    return False
            return True
        else:
            raise self.make_error("invalid_dict")

    def _check_if_every_key_is_string(self, dict_string_int):
        return all(map(lambda key: isinstance(key, str), dict_string_int.keys()))

    def _deserialize(self, value, attr, data, **kwargs):

        if self._check_if_every_item_is_int(value) and self._check_if_every_key_is_string(value):
            return value

        raise self.make_error("invalid_type")


class FrequenceDistributionSchema(Schema):
    frequency = FrequenceDistributionField(attribute="frequency", required=True)

    class Meta:
        unknown = EXCLUDE
