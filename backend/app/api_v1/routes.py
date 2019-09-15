from flask import request
from flask_restplus import Resource, Api
from marshmallow.exceptions import ValidationError
from app.api_v1.schemas import FrequenceDistributionSchema, SendTextSchema, VocabularySchema
from app.models import Text
from app.extensions import db
from app.text_handler.text_handler import TextHandler
from . import api_bp_v1

api_restfull = Api(api_bp_v1)


@api_restfull.route("/send-text")
class SendTextAPI(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        schema = SendTextSchema()

        try:

            data = schema.load(json_data)

            text = Text()
            text.text = data.get("text")

            db.session.add(text)
            db.session.commit()

            data.update({"id": text.id})

            return schema.dump(data), 201

        except ValidationError as error:
            return error.messages, 400


@api_restfull.route("/isolated-vocabulary")
class IsolatedVocabularyApi(Resource):
    def get(self):
        list_of_texts = [text for text, in db.session.query(Text.text).order_by(Text.id).all()]
        text_handler = TextHandler(list_of_texts)

        vocabulary = {"vocabulary": text_handler.sw_vocabulary()}
        schema = VocabularySchema()

        return schema.load(vocabulary), 200


@api_restfull.route("/isolated-frequency-distribution")
class IsolatedFrequencyDistributionAPI(Resource):
    def get(self):
        list_of_texts = [text for text, in db.session.query(Text.text).order_by(Text.id).all()]
        text_handler = TextHandler(list_of_texts)

        frequency = {"frequency": text_handler.sw_frequency_distribution()}
        schema = FrequenceDistributionSchema()

        return schema.load(frequency), 200
